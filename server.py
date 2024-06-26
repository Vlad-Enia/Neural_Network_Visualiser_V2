import json
import flask
from flask import Flask, session
from flask import request
import drawPlot
import pickle
import numpy as np
from markupsafe import escape
import os.path
import nn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['TEMPLATES_AUTO_RELOAD'] = True

def save_object(object, path):
    with open(path, 'wb+') as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_object(path):
    with open(path, 'rb+') as f:
        object = pickle.load(f)
    return object


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template('index.html')


@app.route('/guide')
def load_guide_page():
    return flask.render_template('guide.html')


@app.route('/guide/<int:step>/<scenario>')
def set_train_scenario(step, scenario):
    url = '/guide/'
    if step == 1:
        if scenario == 'class' or scenario == 'seg':
            session['train_task'] = scenario
        elif scenario == 'pointnet' or scenario == 'gcn':
            session['train_net'] = scenario
            step += 1
        url = url + str(step)
    return flask.redirect(url)



@app.route('/guide/<int:step>')
def load_guide_step(step):
    if 0 <= step <= 5:
        if step == 0:
            page_name = 'guide.html'
        else:
            if step == 1 or step == 2:
                if session['train_task']:
                    page_name = f'guide_{step}_{session['train_task']}.html'
                else:
                    page_name = 'guide.html'
            else:
                page_name = f'guide_{step}.html'
        return flask.render_template(page_name)

@app.route('/plot')
def load_perceptron_and_plot():
    fig_loss, fig_acc = drawPlot.draw_plot()
    with open('static/data/plots/act.html', 'r', encoding='utf-8') as f:
        fig_act = f.read()
    with open('static/data/plots/pred.html', 'r', encoding='utf-8') as f:
        fig_pred = f.read()
    return {'fig_loss': fig_loss, 'fig_acc': fig_acc, 'fig_act': fig_act, 'fig_pred': fig_pred}

@app.route('/default_dataset/<string:obj_name>')
def load_default_dataset(obj_name):
    if session['train_task'] == 'class':
        seg = False
    else:
        seg = True
    if session['train_net'] == 'pointnet':
        graph = False
        n_pts = 5000
    else:
        graph = True
        n_pts = 1000
    sel_graph_alg = 'knn'
    k = 15
    r = 0.05
    noise = 0

    session['n_pts'] = n_pts
    session['sel_graph_alg'] = sel_graph_alg
    session['k'] = k
    session['r'] = r
    session['noise'] = noise

    fig, meta_dict, param_dict = drawPlot.visualise_graph(obj_name, noise=0, graph=graph, seg=seg, n_pts=n_pts, sel_graph_alg=sel_graph_alg, k=k, r=r)
    return {'fig': fig, 'params': param_dict, 'meta': meta_dict}
    # fig, dataset_train, labels_train, dataset_test, labels_test, param_dict = drawPlot.draw_plot(dataset_name)
    # return {'fig': fig.to_html(full_html=False, div_id='dataset-plot-div'), 'params': param_dict}


@app.route('/custom_dataset', methods=['POST'])
def load_custom_dataset():
    print(request.form)
    obj_name = request.form['obj_name']
    if session['train_task'] == 'class':
        seg = False
    else:
        seg = True
    if session['train_net'] == 'pointnet':
        graph = False
        n_pts = int(request.form.get('n_pts'))
        noise = float(request.form.get('noise'))
        sel_graph_alg = 'knn'
        k = 15
        r = 0.05
    else:
        graph = True
        n_pts = 1000
        noise = 0
        sel_graph_alg = request.form.get('sel_graph_alg')
        k = int(request.form.get('sel_k'))
        r = float(request.form.get('sel_r'))

    session['n_pts'] = n_pts
    session['sel_graph_alg'] = sel_graph_alg
    session['k'] = k
    session['r'] = r
    session['noise'] = noise

    fig, meta_dict, param_dict = drawPlot.visualise_graph(obj_name, noise=noise, graph=graph, seg=seg, n_pts=n_pts, sel_graph_alg=sel_graph_alg, k=k, r=r)
    return {'fig': fig, 'params': param_dict, 'meta': meta_dict}


@app.route('/retrieve_dataset')
def retrieve_dataset():
    dataset_train = load_object('./static/config/dataset_train.bin')
    dataset_test = load_object('./static/config/dataset_test.bin')
    labels_train = load_object('./static/config/labels_train.bin')
    labels_test = load_object('./static/config/labels_test.bin')
    return drawPlot.draw_dataset(dataset_train, dataset_test, labels_train, labels_test)


@app.route('/confirm_dataset', methods=['POST'])
def confirm_dataset():
    session['obj_name'] = request.form.get('obj_name')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@app.route('/retrieve_dataset_params')
def retrieve_dataset_params():
    with open('./static/config/input_dataset_params.bin', 'rb+') as f:
        param_dict = pickle.load(f)
    return param_dict


@app.route('/retrieve_train_data')
def retrieve_train_data():
    train_data = {
        'task': session['train_task'],
        'net': session['train_net']
    }

    return train_data


@app.route('/train', methods=['GET'])
def load_train_page():
    return flask.render_template('train_page.html')


@app.route('/train/change_input')
def load_change_input_page():
    return flask.render_template('change_input.html')


@app.route('/train/change_architecture')
def change_architecture():
    return flask.render_template('change_architecture.html')

@app.route('/train/train_nn', methods=['POST'])
def train_nn():
    model = nn.load_model('./static/config/model')
    epochs = int(request.form['epochs'])
    batch_size = int(request.form['batch_size'])
    dataset_train = load_object('./static/config/dataset_train.bin')
    dataset_test = load_object('./static/config/dataset_test.bin')
    labels_train = load_object('./static/config/labels_train.bin')
    labels_test = load_object('./static/config/labels_test.bin')
    dataset_params = load_object('./static/config/input_dataset_params.bin')
    n_labels = dataset_params['n_colors']
    history = nn.train_nn(model, dataset_train, labels_train, dataset_test, labels_test, n_labels, epochs, batch_size)
    model.save('./static/config/model')
    save_object(history.history, './static/config/history.bin')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


if __name__ == '__main__':
    # print(app.config)
    app.run(port=8000)
