import os

import h5py
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import torch

# from nn import convert_from_one_hot, convert_to_one_hot

TRAIN_COLORS = ['rgb(172,84,84)', 'rgb(84,99,172)', 'rgb(69,118,69)', 'Orange']
VAL_COLORS = ['rgb(177,109,109)', 'rgb(130,139,179)', 'rgb(97,120,97)', 'rgb(244,213,158)']


def compute_nbrs(pts, alg, k=15, r=0.1):
    if alg == 'knn':
        nbrs = NearestNeighbors(algorithm='auto', n_neighbors=k).fit(pts)
        out = nbrs.kneighbors_graph(pts, mode='distance').todense()
    elif alg == 'rad':
        nbrs = NearestNeighbors(algorithm='auto', radius=r).fit(pts)
        out = nbrs.radius_neighbors_graph(pts, mode='distance').todense()
    return out


def graph_construct(pts, alg, k=15, r=0.1):
    out = compute_nbrs(pts, alg, k, r)
    G=nx.from_numpy_array(out, create_using=nx.Graph)
    edges = [[x[0] for x in G.edges()], [x[1] for x in G.edges]]
    return np.array(edges)


def visualise_graph(obj_name, sel_graph_alg='knn', k=15, r=0.05, n_pts=5000, noise=0, seg=False, graph=False, no_axis=False):
    # static/images/modelnet/show_samples/point
    if not seg:
        dataset_name = 'modelnet'
    else:
        dataset_name = 'shapenet'
        scale_masks = {
            'airplane': (1, 1, 2),
            'earphone': (2, 1.5, 1),
            'guitar': (2, 1, 0.5),
            'motorbike': (0.5, 1, 1),
            'rocket': (0.5, 2, 2),
            'skateboard': (0.5, 1, 2)
        }
        scale_mask = scale_masks[obj_name]
    if graph:
        n_pts = 1000
    obj_name = obj_name + '.h5'

    base_path = f'static/images/{dataset_name}/show_samples/{obj_name}'
    f = h5py.File(base_path, 'r')

    # Nodes
    x_nodes = []
    y_nodes = []
    z_nodes = []
    nodes = f['nodes'][:]

    # Apply Gaussian Noise
    nodes = np.array(nodes)
    if noise > 0:
        nodes += np.random.normal(0., noise, nodes.shape)

    # Downsample
    if len(nodes) > n_pts:
        sample_idx = np.random.randint(0, len(nodes), size=n_pts)
        nodes = [nodes[i] for i in sample_idx]

    for i in nodes:
        if seg:
            x_nodes.append(i[0]/scale_mask[0])
            y_nodes.append(i[2]/scale_mask[1])
            z_nodes.append(i[1]/scale_mask[2])
        else:
            x_nodes.append(i[0])
            y_nodes.append(i[1])
            z_nodes.append(i[2])

    if seg:
        labels = f['labels'][:]
        if len(labels) > n_pts:
            labels = [labels[i] for i in sample_idx]
        # Create a color map for the labels
        unique_labels = sorted(set(labels))
        colors = px.colors.qualitative.Plotly[:len(unique_labels)]
        label_to_color = {label: colors[i] for i, label in enumerate(unique_labels)}
        point_colors = [label_to_color[label] for label in labels]
    else:
        point_colors = 'rgb(80, 101, 168)'

    trace_nodes = go.Scatter3d(x=x_nodes, y=y_nodes, z=z_nodes, mode='markers',
                               marker=dict(symbol='circle', size=4, color=point_colors, opacity=1))
    data = [trace_nodes]

    if graph:
        # Edges
        x_edges = []
        y_edges = []
        z_edges = []
        edges = graph_construct(nodes, sel_graph_alg, k=k, r=r)
        for i in range(0, edges[0].size):
            start = edges[0][i]
            end = edges[1][i]
            x_start = x_nodes[start]
            y_start = y_nodes[start]
            z_start = z_nodes[start]
            x_end = x_nodes[end]
            y_end = y_nodes[end]
            z_end = z_nodes[end]
            x_edges += [x_start, x_end, None]
            y_edges += [y_start, y_end, None]
            z_edges += [z_start, z_end, None]

        trace_edges = go.Scatter3d(x=x_edges, y=y_edges, z=z_edges, mode='lines', line=dict(color='darkgray', width=1),
                                   hoverinfo='none')
        data.append(trace_edges)

    layout = go.Layout(title="", width=900, height=678, showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    if no_axis:
        fig.update_layout(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False)
            )
        )

    # n_pts = dataset_name.split('_')[2]
    if not graph:
        param_dict = {
            'n_pts': int(n_pts),
            'noise': noise
        }
    else:
        param_dict = {
            'n_pts_fixed': 1000,
            'sel_graph_alg': sel_graph_alg,
            'sel_k': k,
            'sel_r': r,
        }

    meta_dict = {
        'obj_name': obj_name,
        'graph': graph,
    }

    return fig.to_html(full_html=False, default_width='100%', default_height='100%'), meta_dict, param_dict


def draw_plot():
    df = pd.read_csv('static/data/model_results/data_graph/data_graph_1000_k15_lr0.0005/airplane/gcn_01.csv')
    tr_loss = go.Scatter(x=df['epoch'], y=df['train_ls'], name='Train Loss')
    test_loss = go.Scatter(x=df['epoch'], y=df['test_ls'], name='Test Loss')
    test_acc = go.Scatter(x=df['epoch'], y=df['test_acc'], name='Test Accuracy')

    fig_loss = go.Figure([tr_loss, test_loss])
    fig_loss.update_layout(title='Loss', showlegend=True, xaxis_title="Epochs", yaxis_title="Loss",     paper_bgcolor='rgba(245, 245, 245,0)', )

    fig_acc = go.Figure(test_acc)
    fig_acc.update_layout(title='Accuracy', showlegend=True, xaxis_title="Epochs", yaxis_title="Accuracy",     paper_bgcolor='rgba(245, 245, 245,0)', )

    return fig_loss.to_html(full_html=False, default_width='99%', default_height='99%'), fig_acc.to_html(full_html=False, default_width='99%', default_height='99%')
