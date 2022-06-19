import numpy as np
import plotly.graph_objects as go
from sklearn import datasets

def return_dataset_scatters(dataset, labels, marker_size):
    colors = ['rgb(172,84,84)', 'rgb(84,99,172)', 'rgb(69,118,69)', 'Orange']

    unique_labels = list(set(labels))

    separate_datasets = []

    for unique_label in unique_labels:
        separate_datasets.append(
            np.array([dataset[i] for i in range(0, dataset.shape[0]) if labels[i] == unique_label]))

    scatters = []

    for unique_label in unique_labels:
        scatter = go.Scatter(
            x=separate_datasets[unique_label][:, 0],
            y=separate_datasets[unique_label][:, 1],
            mode='markers',
            hovertext=str(unique_label),
            hoverinfo='x+y+text',
            name='Label ' + str(unique_label),
            marker=dict(
                color=colors[unique_label],
                size=marker_size,
                line=dict(
                    color='Black',
                    width=2
                )
            )
        )
        scatters.append(scatter)
    return scatters


def plot_dataset(dataset, labels, figure_title, marker_size):
    scatters = return_dataset_scatters(dataset, labels, marker_size)

    fig = go.Figure(
        data=scatters,
        layout=dict(
            title=figure_title,
            showlegend=True
        )
    )

    # fig.show()
    return fig


def create_blobs_dataset(n_clusters=2, n_colors=2, n_samples_per_cluster=500, noise=2.5, distance_between_clusters=10):
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

    fig = plot_dataset(dataset, labels, '', 10)

    return fig, dataset, labels, {'n_samples': n_samples_per_cluster, 'noise': noise, 'distance': distance_between_clusters}


def create_moons_dataset(n_samples_per_cluster=500, noise=0.1):
    dataset, labels = datasets.make_moons([n_samples_per_cluster, n_samples_per_cluster], noise=noise)
    fig = plot_dataset(dataset, labels, '', 10)
    return fig, dataset, labels, {'n_samples': n_samples_per_cluster, 'noise': noise}


def create_circles_dataset(n_samples_per_cluster=500, noise=0.05, factor=0.2):
    dataset, labels = datasets.make_circles([n_samples_per_cluster, n_samples_per_cluster], noise=noise, factor=factor)
    fig = plot_dataset(dataset, labels, '', 10)
    return fig, dataset, labels, {'n_samples': n_samples_per_cluster, 'noise': noise, 'factor': factor}


def draw_plot(plot_name):
    if plot_name == 'column_1_1':
        fig, dataset, labels, param_dict = create_blobs_dataset()
    elif plot_name == 'column_1_2':
        fig, dataset, labels, param_dict = create_blobs_dataset(n_clusters=3, n_samples_per_cluster=1000, n_colors=2, noise=2)
    elif plot_name == 'column_2_1':
        fig, dataset, labels, param_dict = create_blobs_dataset(n_clusters=3, n_samples_per_cluster=1000, n_colors=3, noise=2)
    elif plot_name == 'column_2_2':
        fig, dataset, labels, param_dict = create_blobs_dataset(n_clusters=4, n_samples_per_cluster=1000, n_colors=2, noise=2)
    elif plot_name == 'column_3_1':
        fig, dataset, labels, param_dict = create_blobs_dataset(n_clusters=4, n_samples_per_cluster=1000, n_colors=3, noise=2)
    elif plot_name == 'column_3_2':
        fig, dataset, labels, param_dict = create_blobs_dataset(n_clusters=4, n_samples_per_cluster=1000, n_colors=4, noise=2)
    elif plot_name == 'column_4_1':
        fig, dataset, labels, param_dict = create_moons_dataset()
    elif plot_name == 'column_4_2':
        fig, dataset, labels, param_dict = create_circles_dataset()
    return fig, dataset, labels, param_dict


def draw_custom_plot(plot_name, param_dict):
    if plot_name == 'column_1_1':
        fig, dataset, labels, res_param_dict = create_blobs_dataset(n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']))
    elif plot_name == 'column_1_2':
        fig, dataset, labels, res_param_dict = create_blobs_dataset(n_clusters=3, n_colors=2, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']))
    elif plot_name == 'column_2_1':
        fig, dataset, labels, res_param_dict = create_blobs_dataset(n_clusters=3, n_colors=3, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']))
    elif plot_name == 'column_2_2':
        fig, dataset, labels, res_param_dict = create_blobs_dataset(n_clusters=4, n_colors=2, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']))
    elif plot_name == 'column_3_1':
        fig, dataset, labels, res_param_dict = create_blobs_dataset(n_clusters=4, n_colors=3, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']))
    elif plot_name == 'column_3_2':
        fig, dataset, labels, res_param_dict = create_blobs_dataset(n_clusters=4, n_colors=4, n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), distance_between_clusters=int(param_dict['distance']))
    elif plot_name == 'column_4_1':
        fig, dataset, labels, res_param_dict = create_moons_dataset(n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']))
    elif plot_name == 'column_4_2':
        fig, dataset, labels, res_param_dict = create_circles_dataset(n_samples_per_cluster=int(param_dict['n_samples']), noise=float(param_dict['noise']), factor=float(param_dict['factor']))
    return fig, dataset, labels, res_param_dict