import numpy as np
import plotly.graph_objects as go
from sklearn import datasets
from sklearn.model_selection import train_test_split
from nn import convert_from_one_hot, convert_to_one_hot


def return_dataset_scatters(dataset, train, labels, marker_size):
    # colors = ['rgb(172,84,84)', 'rgb(84,99,172)', 'rgb(69,118,69)', 'Orange']
    train_colors = ['rgb(172,84,84)', 'rgb(84,99,172)', 'rgb(69,118,69)', 'Orange']
    test_colors = ['rgb(177,109,109)', 'rgb(130,139,179)', 'rgb(97,120,97)', 'rgb(244,213,158)']

    unique_labels = list(set(labels))

    separate_datasets = []

    for unique_label in unique_labels:
        separate_datasets.append(
            np.array([dataset[i] for i in range(0, dataset.shape[0]) if labels[i] == unique_label]))

    scatters = []

    if train:
        border_color = 'Black'
        name = 'Train Label '
        colors = train_colors
    else:
        border_color = 'DarkGrey'
        name = 'Test Label '
        colors = test_colors

    for unique_label in unique_labels:
        scatter = go.Scatter(
            x=separate_datasets[unique_label][:, 0],
            y=separate_datasets[unique_label][:, 1],
            mode='markers',
            hovertext=str(unique_label),
            hoverinfo='x+y+text',
            name=name + str(unique_label),
            marker=dict(
                color=colors[unique_label],
                size=marker_size,
                line=dict(
                    color=border_color,
                    width=2
                )
            )
        )
        scatters.append(scatter)
    return scatters


def plot_dataset(dataset_train, dataset_test, labels_train, labels_test):
    train_scatter = return_dataset_scatters(dataset_train, True, labels_train, 10)
    test_scatter = return_dataset_scatters(dataset_test, False, labels_test, 10)
    return train_scatter, test_scatter


def create_blobs_dataset(n_clusters=2, n_colors=2, n_samples_per_cluster=500, noise=2.5, distance_between_clusters=10,
                         test_size=0.1):
    if not (2 <= n_clusters <= 4):
        raise Exception('Invalid number of clusters. You can pick any natural number between 2 and 4.')
    if not (1 <= n_samples_per_cluster <= 10000):
        raise Exception('Invalid number of samples per cluster. You can pick any natural number between 1 and 10000.')
    if not (2 <= n_colors <= 4):
        raise Exception('Invalid number of features. You can pick any natural number between 2 and 4.')

    if n_clusters == 2:
        centers = [(-distance_between_clusters, -distance_between_clusters),
                   (distance_between_clusters, distance_between_clusters)]
    elif n_clusters == 3:
        centers = [(-distance_between_clusters, -distance_between_clusters), (0, 0),
                   (distance_between_clusters, distance_between_clusters)]
    elif n_clusters == 4:
        centers = [(-distance_between_clusters, -distance_between_clusters),
                   (distance_between_clusters, -distance_between_clusters),
                   (distance_between_clusters, distance_between_clusters),
                   (-distance_between_clusters, distance_between_clusters), ]

    n_samples = [n_samples_per_cluster for i in range(0, n_clusters)]
    dataset, labels = datasets.make_blobs(n_samples=n_samples, cluster_std=noise, centers=centers)
    labels = labels % n_colors

    dataset_train, dataset_test, labels_train, labels_test = train_test_split(dataset, labels, test_size=test_size)

    train_scatter, test_scatter = plot_dataset(dataset_train, dataset_test, labels_train, labels_test)

    fig = go.Figure(
        data=train_scatter + test_scatter,
        layout={
            'height': 500,
        }
    )

    return fig, dataset_train, labels_train, dataset_test, labels_test, {'n_samples': n_samples_per_cluster,
                                                                         'noise': noise,
                                                                         'distance': distance_between_clusters,
                                                                         'test_size': test_size}


def create_moons_dataset(n_samples_per_cluster=500, noise=0.1, test_size=0.1):
    dataset, labels = datasets.make_moons([n_samples_per_cluster, n_samples_per_cluster], noise=noise)
    dataset_train, dataset_test, labels_train, labels_test = train_test_split(dataset, labels, test_size=test_size)
    train_scatter, test_scatter = plot_dataset(dataset_train, dataset_test, labels_train, labels_test)
    fig = go.Figure(
        data=train_scatter + test_scatter,
        layout={
            'height': 500,
        }
    )
    return fig, dataset_train, labels_train, dataset_test, labels_test, {'n_samples': n_samples_per_cluster,
                                                                         'noise': noise, 'test_size': test_size}


def create_circles_dataset(n_samples_per_cluster=500, noise=0.05, factor=0.2, test_size=0.1):
    dataset, labels = datasets.make_circles([n_samples_per_cluster, n_samples_per_cluster], noise=noise, factor=factor)
    dataset_train, dataset_test, labels_train, labels_test = train_test_split(dataset, labels, test_size=test_size)
    train_scatter, test_scatter = plot_dataset(dataset_train, dataset_test, labels_train, labels_test)
    fig = go.Figure(
        data=train_scatter + test_scatter,
        layout={
            'height': 500,
        }
    )
    return fig, dataset_train, labels_train, dataset_test, labels_test, {'n_samples': n_samples_per_cluster,
                                                                         'noise': noise, 'factor': factor,
                                                                         'test_size': test_size}


def draw_plot(plot_name):
    if plot_name == 'column_1_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset()
    elif plot_name == 'column_1_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=3,
                                                                                                       n_samples_per_cluster=1000,
                                                                                                       n_colors=2,
                                                                                                       noise=2)
    elif plot_name == 'column_2_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=3,
                                                                                                       n_samples_per_cluster=1000,
                                                                                                       n_colors=3,
                                                                                                       noise=2)
    elif plot_name == 'column_2_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=4,
                                                                                                       n_samples_per_cluster=1000,
                                                                                                       n_colors=2,
                                                                                                       noise=2)
    elif plot_name == 'column_3_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=4,
                                                                                                       n_samples_per_cluster=1000,
                                                                                                       n_colors=3,
                                                                                                       noise=2)
    elif plot_name == 'column_3_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=4,
                                                                                                       n_samples_per_cluster=1000,
                                                                                                       n_colors=4,
                                                                                                       noise=2)
    elif plot_name == 'column_4_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_moons_dataset()
    elif plot_name == 'column_4_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_circles_dataset()
    return fig, dataset_train, dataset_test, labels_train, labels_test, param_dict


def draw_custom_plot(plot_name, param_dict):
    if plot_name == 'column_1_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(
            n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']),
            distance_between_clusters=int(param_dict['distance']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_1_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=3,n_colors=2,n_samples_per_cluster=int(param_dict['n_samples']),noise=float(param_dict['noise']),distance_between_clusters=int(param_dict['distance']),test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_2_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=3,n_colors=3,n_samples_per_cluster=int(param_dict['n_samples']),noise=float(param_dict['noise']),distance_between_clusters=int(param_dict['distance']),test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 3
    elif plot_name == 'column_2_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=4,n_colors=2,n_samples_per_cluster=int(param_dict['n_samples']),noise=float(param_dict['noise']),distance_between_clusters=int(param_dict['distance']),test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_3_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=4,n_colors=3,n_samples_per_cluster=int(param_dict['n_samples']),noise=float(param_dict['noise']),distance_between_clusters=int(param_dict['distance']),test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 3
    elif plot_name == 'column_3_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=4,n_colors=4,n_samples_per_cluster=int(param_dict['n_samples']),noise=float(param_dict['noise']),distance_between_clusters=int(param_dict['distance']),test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 4
    elif plot_name == 'column_4_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_moons_dataset(
            n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']),
            test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_4_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_circles_dataset(
            n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']),
            factor=float(param_dict['factor']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    return fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict


def draw_dataset(dataset_train, dataset_test, labels_train, labels_test):
    scatter_train = return_dataset_scatters(dataset_train, True, labels_train, 10)
    scatter_test = return_dataset_scatters(dataset_test, False, labels_test, 10)
    fig = go.Figure(
        data=scatter_train + scatter_test,
    )
    fig_html = fig.to_html(full_html=False, default_width='100%', default_height='100%')
    return fig_html


def plot_loss(history, key):
    if key == 'loss':
        title = 'Loss'
    else:
        title = 'Validation Loss'
    fig = go.Figure(
        data=go.Scatter(
            x=list(range(1, np.size(history[key]) + 1)),
            y=history[key],
            mode='lines',
            name=key,
        ),
        layout=dict(
            xaxis_title="Epoch",
            yaxis_title=title,
            showlegend=True
        )
    )
    return fig.to_html(full_html=False)


def plot_decision_boundary(dataset, labels, n_labels, model, steps=500, boundary_offset_x=0.5, boundary_offset_y=0.5):
    """
    Function to plot the decision boundary and data points of a model trained to classify 2-dimensional data-set.
    :param dataset: 2-dimensional data-set that the model was trained on;
    :param labels: the labels of the dataset; for multi-class classification problem, one-hot encoding is used
    :param model: compiled sequential keras model, with 2 neurons on the input (corresponding to the 2 coordinates of the training data-set) and 1 neuron on the output (prediction for label);
    :param steps: dimension for the mesh on which the decision boundaries will be drawn; the bigger, the finer the boundaries, but more omputationally expensive
    :return: a plotly heatmap illustrating the decision boundaries of the model, as well as the training data-set
    """

    colors = ['rgb(172,84,84)', 'rgb(84,99,172)', 'rgb(69,118,69)', 'rgb(254, 217, 166)']

    # In the case of multi-class classification (more than two), a one-hot encoding for the labels was used in the
    # training process (e.g. for label 1, the one-hot encoding is [0,1,0], for 2, [0,0,1])
    # Now, when we need to draw the decision surface, we need to convert back to integer labels
    if len(np.shape(labels)) > 1 and np.shape(labels)[1] > 1:
        labels = convert_from_one_hot(labels)

    # Compute the boundaries of the dataset, given by the min and max values coordinates x and y of all the points in
    # the dataset; The boundaries are then offset, depending on the values of the boundary_offset_x,
    # boundary_offset_y; What we are doing is basically define the boundaries of an area in the shape of a
    # rectangle, that includes the dataset in its entirety
    xmin, xmax = dataset[:, 0].min() - boundary_offset_x, dataset[:, 0].max() + boundary_offset_x
    ymin, ymax = dataset[:, 1].min() - boundary_offset_y, dataset[:, 1].max() + boundary_offset_y

    # Create a list of evenly spaced points in the area bounded by the boundaries computed above These points are
    # basically placed in an evenly spaced grid, of size steps x steps; therefore, the bigger the value of steps,
    # the finer the grid
    x_span = np.linspace(xmin, xmax, steps)
    y_span = np.linspace(ymin, ymax, steps)
    grid = np.array([[x_coord, y_coord] for y_coord in y_span for x_coord in x_span])

    # Using the model, make predictions for every single point of the grid computed above
    predictions = model.predict(grid)

    # Since we do multi-class classification (more than two), we have one neuron for each class on the output layer
    # In this situation, if softmax was applied on the output layer, the output would be a probability distribution
    # where each neuron would output a probability for each class.
    # Therefore, we consider the prediction as being the index of output neuron that gave the highest probability
    # For example, if we had 3 classes with labels [0, 1, 2] and the prediction from a properly trained network
    # for an instance from class 1 was [0.02, 0.85, 0.13], we would consider the predicted label as being 1,
    # since the maximum probability was given by the neuron with index 1 from the output layer.
    # This is how the method convert_from_one_hot converts from one-hot encodings to integers.
    if len(np.shape(predictions)) > 1 and np.shape(predictions)[1] > 1:
        predictions = convert_from_one_hot(predictions)

    # Because our model has a single neuron on the output layer, it will give a list of predictions, with shape (
    # steps*steps, 1); That is why we need to reshape it back to the grid form => (steps, steps)
    z = predictions.reshape((steps, steps))

    # Colorscale, where
    # - for two-class classification: we bind the color red to the label 0 (negative predictions), white for 0.5, and blue for 1 (positive predictions)
    # - for multi-class classification: we directly use the color array
    if n_labels == 2:
        colorscale = [[0, colors[0]], [0.5, 'white'], [1, colors[1]]]
    elif n_labels == 3:
        colorscale = colors[:3]
    else:
        colorscale = colors

    # We compute a heatmap by taking every point from the grid (each point has x coordinate in x_span and y
    # coordinate in y_span), and based on its predicted value from z (computed by the model), associate a color from
    # the heatmap.
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=x_span,
            y=y_span,
            colorscale=colorscale
        ),
        layout=dict(
            showlegend=False
        )
    )

    dataset_scatters = return_dataset_scatters(dataset, True, labels, 10)
    fig.add_traces(dataset_scatters)
    return fig.to_html(full_html=False)
