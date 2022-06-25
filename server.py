import json
import flask
from flask import Flask
from flask import request
import drawPlot
import pickle
import numpy as np
from markupsafe import escape
import os.path
import nn

app = Flask(__name__)


def save_object(object, path):
    with open(path, 'wb+') as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_object(path):
    with open(path, 'rb+') as f:
        object = pickle.load(f)
    return object


def save_dataset(dataset_train, labels_train, dataset_test, labels_test, param_dict):
    save_object(dataset_train, './static/config/dataset_train.bin')
    save_object(dataset_test, './static/config/dataset_test.bin')
    save_object(labels_train, './static/config/labels_train.bin')
    save_object(labels_test, './static/config/labels_test.bin')
    save_object(param_dict, './static/config/input_dataset_params.bin')


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template('index.html')


@app.route('/guide')
def load_guide_page():
    return flask.render_template('guide.html')


@app.route('/guide/<int:step>')
def load_guide_step(step):
    if 0 <= step <= 5:
        if step == 0:
            page_name = 'guide.html'
        else:
            page_name = f'guide_{step}.html'
        return flask.render_template(page_name)


@app.route('/graph')
def load_graph():
    return flask.render_template('graph.html')


@app.route('/plot/<string:plot_name>')
def load_perceptron_and_plot(plot_name):
    template_name = plot_name + '.html'
    return flask.render_template(template_name)


@app.route('/default_dataset/<string:dataset_name>')
def load_default_dataset(dataset_name):
    fig, dataset_train, labels_train, dataset_test, labels_test, param_dict = drawPlot.draw_plot(dataset_name)
    return {'fig': fig.to_html(full_html=False, div_id='dataset-plot-div'), 'params': param_dict}


@app.route('/custom_dataset', methods=['POST'])
def load_custom_dataset():
    fig, dataset_train, labels_train, dataset_test, labels_test, param_dict = drawPlot.draw_custom_plot(
        request.form['dataset_name'], request.form)
    return {'fig': fig.to_html(full_html=False, div_id='dataset-plot-div'), 'params': param_dict}


@app.route('/retrieve_dataset')
def retrieve_dataset():
    dataset_train = load_object('./static/config/dataset_train.bin')
    dataset_test = load_object('./static/config/dataset_test.bin')
    labels_train = load_object('./static/config/labels_train.bin')
    labels_test = load_object('./static/config/labels_test.bin')
    return drawPlot.draw_dataset(dataset_train, dataset_test, labels_train, labels_test)


@app.route('/confirm_dataset', methods=['POST'])
def confirm_dataset():
    dataset_name = request.form['dataset_name']
    fig, dataset_train, labels_train, dataset_test, labels_test, param_dict = drawPlot.draw_custom_plot(dataset_name,
                                                                                                        request.form)
    save_dataset(dataset_train, labels_train, dataset_test, labels_test, param_dict)
    if os.path.exists('./static/config/network_architecture.bin'):
        network_architecture = load_object('./static/config/network_architecture.bin')
        if param_dict['n_colors'] == 2:
            network_architecture['output_layer_size'] = 1
        else:
            network_architecture['output_layer_size'] = param_dict['n_colors']
        save_object(network_architecture, './static/config/network_architecture.bin')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/retrieve_dataset_params')
def retrieve_dataset_params():
    with open('./static/config/input_dataset_params.bin', 'rb+') as f:
        param_dict = pickle.load(f)
    return param_dict


@app.route('/confirm_network_architecture', methods=['POST'])
def confirm_network_architecture():
    if os.path.exists('./static/config/network_architecture.bin'):
        network_architecture = retrieve_network_architecture()
        network_architecture['nr_hidden_layers'] = int(request.form['nr_hidden_layers'])
        network_architecture['hidden_layer_size_list'] = np.array(
            request.form.getlist('hidden_layer_size_list[]')).astype('int').tolist()
        network_architecture['output_layer_size'] = int(request.form['output_layer_size'])
    else:
        network_architecture = {
            'nr_hidden_layers': int(request.form['nr_hidden_layers']),
            'hidden_layer_size_list': np.array(request.form.getlist('hidden_layer_size_list[]')).astype('int').tolist(),
            'output_layer_size': int(request.form['output_layer_size'])
        }
    print(network_architecture)
    save_object(network_architecture, './static/config/network_architecture.bin')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/retrieve_network_architecture')
def retrieve_network_architecture():
    with open('./static/config/network_architecture.bin', 'rb+') as f:
        network_architecture = pickle.load(f)
    return network_architecture


@app.route('/confirm_network_activations', methods=['POST'])
def confirm_network_activations():
    with open('./static/config/network_architecture.bin', 'rb+') as f:
        network_architecture = pickle.load(f)
    network_architecture['hidden_layer_activation_list'] = request.form.getlist('hidden_layer_activation_list[]')
    network_architecture['output_layer_activation'] = request.form['output_layer_activation']
    print(network_architecture['hidden_layer_activation_list'])
    print(network_architecture['output_layer_activation'])
    save_object(network_architecture, './static/config/network_architecture.bin')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/confirm_network_loss', methods=['POST'])
def confirm_network_loss():
    with open('./static/config/network_architecture.bin', 'rb+') as f:
        network_architecture = pickle.load(f)
    network_architecture['loss_function'] = request.form['loss_function']
    save_object(network_architecture, './static/config/network_architecture.bin')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/confirm_optimizer', methods=['POST'])
def confirm_optimizer():
    with open('./static/config/network_architecture.bin', 'rb+') as f:
        network_architecture = pickle.load(f)
    network_architecture['learning_rate'] = request.form['learning_rate']
    network_architecture['batch_size'] = request.form['batch_size']
    network_architecture['epochs'] = request.form['epochs']
    save_object(network_architecture, './static/config/network_architecture.bin')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/confirm_loss_and_lr', methods=['POST'])
def confirm_loss_and_lr():
    with open('./static/config/network_architecture.bin', 'rb+') as f:
        network_architecture = pickle.load(f)
    network_architecture['learning_rate'] = request.form['learning_rate']
    network_architecture['loss_function'] = request.form['loss_function']
    print(network_architecture)
    save_object(network_architecture, './static/config/network_architecture.bin')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/train', methods=['GET'])
def load_train_page():
    return flask.render_template('train_page.html')


@app.route('/train/change_input')
def load_change_input_page():
    return flask.render_template('change_input.html')


@app.route('/train/change_architecture')
def change_architecture():
    return flask.render_template('change_architecture.html')


@app.route('/train/create_nn', methods=['POST'])
def create_nn():
    network_architecture = retrieve_network_architecture()
    n_hidden_layers = network_architecture['nr_hidden_layers']
    hidden_layer_size_list = network_architecture['hidden_layer_size_list']
    hidden_layer_activation_list = network_architecture['hidden_layer_activation_list']
    output_layer_size = network_architecture['output_layer_size']
    output_layer_activation = network_architecture['output_layer_activation']
    loss_function = network_architecture['loss_function']
    learning_rate = float(network_architecture['learning_rate'])
    model = nn.create_nn(n_hidden_layers, hidden_layer_size_list, output_layer_size, hidden_layer_activation_list,
                         output_layer_activation, learning_rate, loss_function)
    nn.save_model(model, './static/config/model')
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


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


@app.route('/train/get_loss')
def get_loss_plot():
    history = load_object('./static/config/history.bin')
    return drawPlot.plot_loss(history, 'loss')


@app.route('/train/get_val_loss')
def get_val_loss():
    history = load_object('./static/config/history.bin')
    return drawPlot.plot_loss(history, 'val_loss')


@app.route('/train/get_decision_surface')
def get_decision_surface():
    dataset_train = load_object('./static/config/dataset_train.bin')
    labels_train = load_object('./static/config/labels_train.bin')
    model = nn.load_model('./static/config/model')
    dataset_params = load_object('./static/config/input_dataset_params.bin')
    n_labels = int(dataset_params['n_colors'])
    if n_labels > 2:
        one_hot_labels = nn.convert_to_one_hot(labels_train)
        fig = drawPlot.plot_decision_boundary(dataset_train, one_hot_labels, dataset_params['n_colors'], model, steps=300)
    else:
        fig = drawPlot.plot_decision_boundary(dataset_train, labels_train, dataset_params['n_colors'], model, steps=300)
    return fig


if __name__ == '__main__':
    app.run()
