import numpy as np
import plotly.graph_objects as go
from sklearn import datasets
from sklearn.model_selection import train_test_split

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


def create_blobs_dataset(n_clusters=2, n_colors=2, n_samples_per_cluster=500, noise=2.5, distance_between_clusters=10, test_size=0.1):
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

    return fig, dataset_train, labels_train, dataset_test, labels_test, {'n_samples': n_samples_per_cluster, 'noise': noise, 'distance': distance_between_clusters, 'test_size': test_size}


def create_moons_dataset(n_samples_per_cluster=500, noise=0.1, test_size=0.1):
    dataset, labels = datasets.make_moons([n_samples_per_cluster, n_samples_per_cluster], noise=noise)
    dataset_train, dataset_test, labels_train, labels_test = train_test_split(dataset, labels, test_size = test_size)
    train_scatter, test_scatter = plot_dataset(dataset_train, dataset_test, labels_train, labels_test)
    fig = go.Figure(
        data=train_scatter + test_scatter,
        layout={
            'height': 500,
        }
    )
    return fig, dataset_train, labels_train, dataset_test,  labels_test, {'n_samples': n_samples_per_cluster, 'noise': noise, 'test_size': test_size}


def create_circles_dataset(n_samples_per_cluster=500, noise=0.05, factor=0.2, test_size=0.1):
    dataset, labels = datasets.make_circles([n_samples_per_cluster, n_samples_per_cluster], noise=noise, factor=factor)
    dataset_train, dataset_test, labels_train, labels_test = train_test_split(dataset, labels, test_size = test_size)
    train_scatter, test_scatter = plot_dataset(dataset_train, dataset_test, labels_train, labels_test)
    fig = go.Figure(
        data=train_scatter + test_scatter,
        layout={
            'height': 500,
        }
    )
    return fig, dataset_train, labels_train, dataset_test,  labels_test, {'n_samples': n_samples_per_cluster, 'noise': noise, 'factor': factor, 'test_size': test_size}


def draw_plot(plot_name):
    if plot_name == 'column_1_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset()
    elif plot_name == 'column_1_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=3, n_samples_per_cluster=1000, n_colors=2, noise=2)
    elif plot_name == 'column_2_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=3, n_samples_per_cluster=1000, n_colors=3, noise=2)
    elif plot_name == 'column_2_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=4, n_samples_per_cluster=1000, n_colors=2, noise=2)
    elif plot_name == 'column_3_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=4, n_samples_per_cluster=1000, n_colors=3, noise=2)
    elif plot_name == 'column_3_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_blobs_dataset(n_clusters=4, n_samples_per_cluster=1000, n_colors=4, noise=2)
    elif plot_name == 'column_4_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_moons_dataset()
    elif plot_name == 'column_4_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, param_dict = create_circles_dataset()
    return fig, dataset_train, dataset_test, labels_train, labels_test, param_dict


def draw_custom_plot(plot_name, param_dict):
    if plot_name == 'column_1_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_1_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=3, n_colors=2, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_2_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=3, n_colors=3, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 3
    elif plot_name == 'column_2_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=4, n_colors=2, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_3_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=4, n_colors=3, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 3
    elif plot_name == 'column_3_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_blobs_dataset(n_clusters=4, n_colors=4, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 4
    elif plot_name == 'column_4_1':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_moons_dataset(n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), test_size=float(param_dict['test_size']))
        res_param_dict['n_colors'] = 2
    elif plot_name == 'column_4_2':
        fig, dataset_train, dataset_test, labels_train, labels_test, res_param_dict = create_circles_dataset(n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), factor=float(param_dict['factor']), test_size=float(param_dict['test_size']))
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

