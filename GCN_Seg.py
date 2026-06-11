import os
import shutil
import numpy as np
import plotly.graph_objects as go
import torch
from torch.utils.data import Dataset
import json
import h5py
# import open3d as o3
import random
# from IPython import display
import plotly.graph_objs as go
import plotly.express as px
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import time
import plotly.io as pio
import networkx as nx
import glob
from sklearn.neighbors import NearestNeighbors
pio.renderers.default = "vscode"
from torch.nn import Upsample, ConvTranspose2d, Linear, MaxUnpool2d, MaxPool2d
from torch.nn.functional import interpolate, upsample
from torch_geometric.nn import GCNConv, SAGPooling, ASAPooling

class GCNSegData(Dataset):
    paths = []
    def __init__(self, base_path, cls_choice, n_samples, n_pts=1000):
        path = os.path.join(base_path, cls_choice)
        path += '/*.h5'
        self.paths = glob.glob(path)
        n_samples_total = len(self.paths)
        if (n_samples < n_samples_total):
            self.n_samples = n_samples
            idx = np.random.choice(n_samples_total, n_samples, replace=False)
            self.paths = [self.paths[i] for i in idx]
        else:
            self.n_samples = n_samples_total
        f = h5py.File(self.paths[0], 'r')
        self.n_classes = f['classes'][()]

    def __len__(self):
        return self.n_samples

    def get_n_classes(self):
        return self.n_classes

    def __getitem__(self, index):
        f = h5py.File(self.paths[index], 'r')
        edge_w = f['edge_weight'][:]
        edges = f['edges'][:]
        nodes = f['nodes'][:]
        labels = f['labels'][:]

        # Offset labels to 0
        labels = labels - min(labels)
        nodes = np.array(nodes)
        nodes = torch.tensor(np.array(nodes), dtype=torch.float)
        labels = torch.tensor(np.array(labels), dtype=torch.long)
        edges = torch.tensor(np.array(edges), dtype=torch.long)
        edge_w = torch.tensor(np.array(edge_w), dtype=torch.float)
        return nodes, edges, edge_w, labels, self.n_classes


class GCNSeg(nn.Module):
    def __init__(self, class_num=10):
        super(GCNSeg, self).__init__()
        self.conv1 = GCNConv(3, 64, normalize=True)
        self.conv2 = GCNConv(64, 128, normalize=True)
        self.conv3 = GCNConv(128, 128, normalize=True)
        self.conv4 = GCNConv(128, 64, normalize=True)
        self.conv5 = GCNConv(64, class_num, normalize=True)

    def forward(self, x, edge_index, edge_attr):
        # because the dataloader packeges the inputs of size [1000, 3] in batches, but we use batches of size 1, we resize from [1, 1000, 3] to [1000, 3]
        x = x.view(-1, 3)
        # same for edge_index [1, 2, num_edges] -> [2, num_edges]
        edge_index = edge_index.view(2, -1)
        edge_attr = edge_attr.view(-1)  # [1, num_edges] -> [num_edges]
        # we use batches of size 1 because num_edges is not the same for every object, which causes errors in training, because the model expects all the inputs in a batch to have the same shape

        x = self.conv1(x, edge_index, edge_attr)
        x = F.relu(x)

        x = self.conv2(x, edge_index, edge_attr)
        x = F.relu(x)

        x = self.conv3(x, edge_index, edge_attr)
        x = F.relu(x)

        x = self.conv4(x, edge_index, edge_attr)
        x = F.relu(x)

        x = self.conv5(x, edge_index, edge_attr)

        return F.log_softmax(x, dim=-1)


class GCNSegTrainer():
    def __init__(self, model, device, train_set, test_set, opts):
        self.model = model  # neural net
        self.epochs = opts['epochs']
        self.n_points = opts['n_points']
        self.n_classes = opts['n_classes']
        self.device = device
        print(model)
        self.batch = opts['batch_size']
        self.model.to(self.device)
        # optimizer method for gradient descent
        self.optimizer = torch.optim.Adam(model.parameters(), opts['lr'])
        self.criterion = torch.nn.CrossEntropyLoss()  # loss function
        self.train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=1, shuffle=True)
        self.test_loader = torch.utils.data.DataLoader(dataset=test_set, batch_size=1, shuffle=False)
        self.stats = []
        self.best_acc = 0
        self.res_out_path = os.path.join(opts['res_out_path'], opts['class'])
        self.model_out_path = os.path.join(opts['model_out_path'], opts['class'])
        self.model_out_name = opts['model_out_name']
        self.res_out_name = opts['res_out_name']
        # self.model.apply(self.weights_init)

    def weights_init(self, l):
        if isinstance(l, GCNConv):
            nn.init.xavier_uniform_(l.lin.weight)
            # nn.init.uniform_(l.lin.bias)

    def save_results(self):
        out = pd.DataFrame()
        out['epoch'] = [x[0] for x in self.stats]
        out['train_ls'] = [x[1] for x in self.stats]
        out['test_ls'] = [x[2] for x in self.stats]
        out['time'] = [x[3] for x in self.stats]
        out['test_acc'] = [x[4] for x in self.stats]
        os.makedirs(self.res_out_path, exist_ok=True)
        res_out_path = os.path.join(self.res_out_path, self.res_out_name)
        out.to_csv(res_out_path, index=False)

    def compute_loss(self, outputs, labels):
        outputs = outputs.unsqueeze(0)
        outputs = torch.transpose(outputs, 1, 2)
        return self.criterion(outputs, labels)

    def train(self):
        self.model.train()
        t0 = time.time()
        for epoch in range(self.epochs):
            self.tr_loss = []

            for i, (x, edges, weights, labels, _) in enumerate(self.train_loader):
                x, edges, weights, labels = x.to(self.device), edges.to(self.device), weights.to(
                    self.device), labels.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(x, edges, weights)

                # Calculate loss
                loss = self.compute_loss(outputs, labels)
                loss.backward()

                self.optimizer.step()
                self.tr_loss.append(loss.item())

            t1 = time.time()
            t_delta = time.gmtime(t1 - t0)
            t_delta = time.strftime('%H:%M:%S', t_delta)

            # Run validation on the test set after each epoch
            self.test(epoch, t_delta)

        # Save training results after all epochs are completed
        self.save_results()

    def test(self, epoch, t_delta):
        self.model.eval()
        self.test_loss = []
        self.test_accuracy = []
        for i, (x, edges, weights, labels, _) in enumerate(self.test_loader):
            x, edges, weights, labels = x.to(self.device), edges.to(self.device), weights.to(self.device), labels.to(
                self.device)

            with torch.no_grad():
                outputs = self.model(x, edges, weights)  # Forward pass

            # Calculate loss (assuming CrossEntropyLoss is used)
            loss = self.compute_loss(outputs, labels)
            self.test_loss.append(loss.item())

            # Calculate accuracy
            outputs = outputs.unsqueeze(0)
            _, predicted = torch.max(outputs, 2)  # Get predicted classes per point

            correct = predicted.eq(labels.view_as(predicted))  # Compare predictions to true labels
            accuracy = torch.mean(correct.float())  # Calculate accuracy for this batch
            self.test_accuracy.append(accuracy.item())

        # Calculate mean loss and accuracy across batches
        tr_loss_mean = np.mean(self.tr_loss)
        test_loss_mean = np.mean(self.test_loss)
        test_acc_mean = np.mean(self.test_accuracy)

        # Print and store statistics
        print('Epoch {}: train loss: {}, test loss: {:.4f}, time: {}, test accuracy: {:.4f}'.format(epoch + 1,
                                                                                                    tr_loss_mean,
                                                                                                    test_loss_mean,
                                                                                                    t_delta,
                                                                                                    test_acc_mean))
        self.stats.append((epoch + 1, tr_loss_mean, test_loss_mean, t_delta, test_acc_mean))

        # Save model if accuracy improved
        if test_acc_mean > self.best_acc:
            print('Found better. Saving model dict')
            self.best_acc = test_acc_mean
            os.makedirs(self.model_out_path, exist_ok=True)
            model_out_path = os.path.join(self.model_out_path, self.model_out_name)
            torch.save(self.model.state_dict(), model_out_path)

    def get_stats(self):
        return self.stats