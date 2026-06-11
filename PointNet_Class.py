import h5py
import networkx as nx
import json
import argparse
import torch
import os
import pandas as pd
import numpy as np
import shutil
import glob
from torch_geometric.data import InMemoryDataset, download_url, extract_zip
import os.path as osp
from tqdm.notebook import tqdm
from sklearn import preprocessing
import torch.utils.data as data
import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, TopKPooling, SAGPooling, ASAPooling, EdgePooling
from torch_geometric.data import Data
import os
import h5py
from sklearn import preprocessing
import numpy as np
import torch.utils.data as data


class PointDataClass(data.Dataset):
    paths = []
    labels = []

    def __init__(self, base_path, aug='', noise=0):
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
        self.aug = aug
        self.noise = noise

    def __getitem__(self, index):
        f = h5py.File(self.paths[index], 'r')
        nodes = f['nodes'][:]
        if self.aug != '':
            if self.aug == 'stretch':
                nodes = nodes * 10
            elif self.aug == 'translate':
                nodes = nodes + 1

        if self.noise > 0:
            nodes += np.random.normal(0., self.noise, nodes.shape)

        x = torch.tensor(nodes, dtype=torch.float)
        f.close()
        y = torch.from_numpy(np.array(self.labels[index]))
        return x, y

    def __len__(self):
        return len(self.paths)


class PointNetClass(nn.Module):
    def __init__(self, class_num=10):
        super(PointNetClass, self).__init__()
        self.mlp_first = nn.Sequential(
            nn.Conv1d(3, 16, 1),
            nn.ReLU()
        )
        self.mlp_second = nn.Sequential(
            nn.Conv1d(16, 32, 1),
            nn.ReLU()
        )
        # )
        self.mlp_third = nn.Sequential(
            nn.Conv1d(32, class_num, 1),
        )

    def forward(self, x):
        if len(x.shape) == 3:
            x = torch.transpose(x, 1, 2)
        else:
            x = torch.transpose(x, 0, 1)
        x = self.mlp_first(x)
        x = self.mlp_second(x)
        x, crit_set = F.max_pool1d(x, x.shape[-1], return_indices=True)
        x = self.mlp_third(x)
        if len(x.shape) == 3:
            x = x.squeeze(2)
            return F.log_softmax(x, dim=1), crit_set
        else:
            x = x.squeeze(1)
            return F.log_softmax(x, dim=0), crit_set


class PointTrainerClass():
    def __init__(self, model, train_set, test_set, opts, device):
        self.model = model
        self.device = torch.device(device)
        self.model.to(self.device)
        self.epochs = opts['epochs']
        print(model)
        # optimizer method for gradient descent
        self.optimizer = torch.optim.Adam(model.parameters(), opts['lr'])
        self.criterion = torch.nn.CrossEntropyLoss()  # loss function
        self.train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=opts['batch_size'], shuffle=True)
        self.test_loader = torch.utils.data.DataLoader(dataset=test_set, batch_size=1, shuffle=False)
        self.stats = []
        self.best_acc = 0
        self.model_out_path = opts['model_out_path']
        self.res_out_path = opts['res_out_path']
        self.out_name = opts['out_name']
        self.model.apply(self.weights_init)

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
        self.model.train()
        for epoch in range(self.epochs):
            self.tr_loss = []
            for i, (x, labels) in enumerate(self.train_loader):
                x, labels = x.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                outputs, _ = self.model(x)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                self.tr_loss.append(loss.item())

            self.test(epoch)  # run through the validation set
        self.save_stats()

    def test(self, epoch):
        self.model.eval()
        self.test_loss = []
        self.test_accuracy = []
        for i, (x, labels) in enumerate(self.test_loader):
            x, labels = x.to(self.device), labels.to(self.device)
            with torch.no_grad():
                outputs, _ = self.model(x)

            _, predicted = torch.max(outputs.data, 1)
            loss = self.criterion(outputs, labels)
            self.test_loss.append(loss.item())

            self.test_accuracy.append((predicted == labels).sum().item() / predicted.size(0))

        print('epoch: {}, train loss: {}, test loss: {}, test accuracy: {}'.format(epoch + 1, np.mean(self.tr_loss),
                                                                                   np.mean(self.test_loss),
                                                                                   np.mean(self.test_accuracy)))
        self.stats.append((epoch + 1, np.mean(self.tr_loss), np.mean(self.test_loss), np.mean(self.test_accuracy)))
        temp_acc = np.mean(self.test_accuracy)
        if temp_acc > self.best_acc:
            print('Found better. Saving model dict')
            self.best_acc = temp_acc
            os.makedirs(self.model_out_path, exist_ok=True)
            torch.save(self.model.state_dict(), os.path.join(self.model_out_path, self.out_name + '.pt'))
