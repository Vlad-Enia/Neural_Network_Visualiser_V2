import h5py
import networkx as nx
import json
import argparse
import os
import pandas as pd
import numpy as np
from tqdm.notebook import tqdm
from sklearn import preprocessing
import numpy as np
import h5py
from sklearn.neighbors import NearestNeighbors
import networkx as nx
import torch
from torch_geometric.nn import GCNConv, SAGPooling, ASAPooling
from torch_geometric.data import InMemoryDataset, download_url, extract_zip, Data
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data
import time
import json


class GCNDataClass(data.Dataset):
    paths = []
    labels = []

    def __init__(self, base_path):
        paths = []
        labels = []
        for obj in os.listdir(base_path):
            temp = base_path + '/' + obj
            for f in os.listdir(temp):
                paths.append(temp + '/' + f)
                labels.append(obj)
        le = preprocessing.LabelEncoder()
        self.labels = le.fit_transform(labels)
        self.paths = paths
        self.dct = le.classes_

    def __getitem__(self, index):
        f = h5py.File(self.paths[index], 'r')
        edge_w = f['edge_weight'][:]
        edges = f['edges'][:]
        nodes = f['nodes'][:]
        edges = torch.tensor(edges, dtype=torch.long)
        x = torch.tensor(nodes, dtype=torch.float)
        weights = torch.tensor(edge_w, dtype=torch.float)
        f.close()
        y = torch.from_numpy(np.array(self.labels[index]))
        return x, edges, weights, y

    def __len__(self):
        return len(self.paths)

    def getdct(self):
        return self.dct


class GCNClass(nn.Module):
    def __init__(self, pool='SAG', ratio=0.5, class_num=10):
        super(GCNClass, self).__init__()
        self.conv1 = GCNConv(3, 64, normalize=True)
        self.conv2 = GCNConv(64, 128, normalize=True)
        self.pool1 = SAGPooling(in_channels=128, ratio=ratio)
        self.conv3 = GCNConv(128, 64, normalize=True)
        self.pool2 = SAGPooling(in_channels=64, ratio=ratio)
        self.conv4 = GCNConv(64, 32, normalize=True)
        self.conv5 = GCNConv(32, class_num, normalize=True)

    def forward(self, x, edge_index, edge_attr):
        x = x.view(-1, 3)
        edge_index = edge_index.view(2, -1)
        edge_attr = edge_attr.view(-1)

        x = self.conv1(x, edge_index, edge_attr)
        x = F.relu(x)

        x = self.conv2(x, edge_index, edge_attr)
        x = F.relu(x)

        temp = self.pool1(x, edge_index, edge_attr)
        x, edge_index, edge_attr = temp[0], temp[1], temp[2]

        x = self.conv3(x, edge_index, edge_attr)
        x = F.relu(x)

        temp = self.pool2(x, edge_index, edge_attr)
        x, edge_index, edge_attr = temp[0], temp[1], temp[2]

        x = self.conv4(x, edge_index, edge_attr)
        x = F.relu(x)

        x = self.conv5(x, edge_index, edge_attr)

        x = torch.max(x, dim=0, keepdim=True)[0]
        return F.log_softmax(x, dim=1)


class GCNTrainerClass():
    def __init__(self, model, train_set, test_set, opts, device):
        self.model = model
        self.device = torch.device(device)
        self.model.to(self.device)
        self.epochs = opts['epochs']
        self.optimizer = torch.optim.Adam(model.parameters(), opts['lr'])
        self.criterion = torch.nn.CrossEntropyLoss()
        self.train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=1, shuffle=True)
        self.test_loader = torch.utils.data.DataLoader(dataset=test_set, batch_size=1, shuffle=False)
        self.stats = []
        self.best_acc = 0
        self.model_out_path = opts['model_out_path']
        self.res_out_path = opts['res_out_path']
        self.out_name = opts['out_name']
        self.batch = opts['batch_size']
        # self.model.apply(self.weights_init)
        print(model)
    def weights_init(self, l):
        if isinstance(l, nn.Conv1d):
            nn.init.xavier_uniform_(l.weight)
            nn.init.zeros_(l.bias)

    def save_stats(self):
        out = pd.DataFrame()
        out['epoch'] = [x[0] for x in self.stats]
        out['train_ls'] = [x[1] for x in self.stats]
        out['test_ls'] = [x[2] for x in self.stats]
        out['test_acc'] = [x[3] for x in self.stats]
        os.makedirs(self.res_out_path, exist_ok=True)
        out.to_csv(os.path.join(self.res_out_path, self.out_name + '.csv'), index=False)

    def train(self):
        self.model.train()  # put model in training mode
        for epoch in range(self.epochs):
            t0 = time.time()
            self.tr_loss = []
            for i, (x, edges, weights, labels) in enumerate(self.train_loader):
                x, edges, weights, labels = x.to(self.device), edges.to(self.device), weights.to(self.device), labels.to(self.device)
                if i % self.batch == 0 or i == len(self.train_loader):
                    if i != 0:
                        self.optimizer.zero_grad()
                        loss = self.criterion(out, label)
                        loss.backward()
                        self.optimizer.step()
                        self.tr_loss.append(loss.item())
                    out = self.model(x, edges, weights)
                    label = labels
                else:
                    out = torch.cat((out, self.model(x, edges, weights)), 0)
                    label = torch.cat((label, labels), 0)
            t1 = time.time()
            t_delta = time.gmtime(t1 - t0)
            print('Epoch', epoch + 1, 'time:', time.strftime('%H:%M:%S', t_delta))
            self.test(epoch)  # run through the validation set
        self.save_stats()

    def test(self, epoch):
        # puts model in eval mode - not necessary for this demo but good to know
        self.model.eval()
        self.test_loss = []
        self.test_accuracy = []

        for i, (x, edges, weights, labels) in enumerate(self.test_loader):
            x, edges, weights, labels = x.to(self.device), edges.to(
                self.device), weights.to(self.device), labels.to(self.device)
            # pass data through network
            # turn off gradient calculation to speed up calcs and reduce memory
            with torch.no_grad():
                outputs = self.model(x, edges, weights)

            # make our predictions and update our loss info
            _, predicted = torch.max(outputs.data, 1)
            loss = self.criterion(outputs, labels)
            self.test_loss.append(loss.item())

            self.test_accuracy.append(
                (predicted == labels).sum().item() / predicted.size(0))

        temp_acc = np.mean(self.test_accuracy)
        print('epoch: {}, train loss: {}, test loss: {}, test accuracy: {}'.format(
            epoch + 1, np.mean(self.tr_loss), np.mean(self.test_loss), np.mean(self.test_accuracy)))
        print()
        self.stats.append((epoch + 1, np.mean(self.tr_loss),
                           np.mean(self.test_loss), temp_acc))
        if temp_acc > self.best_acc:
            print('Found better. Saving model dict')
            print()
            self.best_acc = temp_acc
            os.makedirs(self.model_out_path, exist_ok=True)
            torch.save(self.model.state_dict(), os.path.join(self.model_out_path, self.out_name + '.pt'))
