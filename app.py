import flask
from flask import Flask
from flask import request
import drawPlot
import pickle
import numpy as np
from markupsafe import escape

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return flask.render_template('index.html')


@app.route('/guide')
def load_guide_page():
    return flask.render_template('guide.html')


@app.route('/guide/<int:step>')
def load_guide_step(step):
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
    print(plot_name)
    return flask.render_template(template_name)


@app.route('/default_dataset/<string:dataset_name>')
def load_default_dataset(dataset_name):
    fig, dataset, labels, param_dict = drawPlot.draw_plot(dataset_name)
    return {'fig': fig.to_html(full_html=False, div_id='dataset-plot-div'), 'params': param_dict}


@app.route('/custom_dataset', methods=['POST'])
def load_custom_dataset():
    fig, dataset, labels, param_dict = drawPlot.draw_custom_plot(request.form['dataset_name'], request.form)
    return {'fig': fig.to_html(full_html=False, div_id='dataset-plot-div'), 'params': param_dict}


def save_object(object, path):
    with open(path, 'wb+') as f:
        pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)


def save_dataset(dataset, labels, param_dict):
    save_object(dataset, './static/config/input_dataset.bin')
    save_object(labels, './static/config/input_labels.bin')
    save_object(param_dict, './static/config/input_dataset_params.bin')


@app.route('/confirm_dataset', methods=['POST'])
def confirm_dataset():
    fig, dataset, labels, param_dict = drawPlot.draw_custom_plot(request.form['dataset_name'], request.form)
    save_dataset(dataset, labels, param_dict)
    return 'bv', 200


@app.route('/confirm_network_architecture', methods=['POST'])
def confirm_network_architecture():
    network_architecture = {
        'nr_hidden_layers': int(request.form['nrHiddenLayers']),
        'hidden_layer_size_list': np.array(request.form.getlist('hiddenLayerSizeList[]')).astype('int').tolist(),
        'hidden_layer_activation_list': [],
        'output_layer_activation': ''
    }
    save_object(network_architecture, './static/config/network_architecture.bin')
    return 'ok'


@app.route('/retrieve_network_architecture')
def retrieve_network_architecture():
    with open('./static/config/network_architecture.bin', 'rb+') as f:
        network_architecture = pickle.load(f)
    return network_architecture


@app.route('/confirm_network_activations', methods=['POST'])
def confirm_network_activations():
    network_architecture = {
        'nr_hidden_layers': int(request.form['nr_hidden_layers']),
        'hidden_layer_size_list': np.array(request.form.getlist('hidden_layer_size_list[]')).astype('int').tolist(),
        'hidden_layer_activation_list': request.form.getlist('hidden_layer_activation_list[]'),
        'output_layer_activation': request.form['output_layer_activation']
    }
    save_object(network_architecture, './static/config/network_architecture.bin')
    return 'ok'

if __name__ == '__main__':
    app.run()
