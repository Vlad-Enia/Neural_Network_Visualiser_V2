import glob
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


class PointSegData(Dataset):
    paths = []

    def __init__(self, base_path, cls_choice, n_samples, noise=0, aug=''):
        path = os.path.join(base_path, cls_choice)
        path += '/*.h5'
        self.paths = glob.glob(path)
        n_samples_total = len(self.paths)
        self.aug = aug
        if (n_samples < n_samples_total):
            self.n_samples = n_samples
            idx = np.random.choice(n_samples_total, n_samples, replace=False)
            self.paths = [self.paths[i] for i in idx]
        else:
            self.n_samples = n_samples_total
        f = h5py.File(self.paths[0], 'r')
        self.n_classes = f['classes'][()]
        self.noise = noise

    def __len__(self):
        return self.n_samples

    def get_n_classes(self):
        return self.n_classes

    def __getitem__(self, index):
        f = h5py.File(self.paths[index], 'r')
        nodes = f['nodes'][:]
        labels = f['labels'][:]

        # Offset labels to 0
        labels = labels - min(labels)
        nodes = np.array(nodes)

        if self.noise > 0:
            nodes += np.random.normal(0., self.noise, nodes.shape)

        nodes = torch.tensor(np.array(nodes), dtype=torch.float)
        labels = torch.tensor(np.array(labels), dtype=torch.long)
        return nodes, labels, self.n_classes


class PointNetSeg(nn.Module):
    def __init__(self, class_num=10):
        super(PointNetSeg, self).__init__()

        self.input = nn.Sequential(
            nn.Conv1d(3, 64, 1),
            nn.ReLU()
        )
        self.mlp1 = nn.Sequential(
            nn.Conv1d(64, 128, 1),
            nn.ReLU()
        )
        self.mlp2 = nn.Sequential(
            nn.Conv1d(128, 64, 1),
            nn.ReLU(),
        )

        self.mlp3 = nn.Sequential(
            nn.Conv1d(64, class_num, 1),
            nn.ReLU(),
        )

    def forward(self, x):
        # Ensure input shape is [batch_size, num_features (i.e. coordinates), num_points]
        if len(x.shape) == 3:
            x = torch.transpose(x, 1, 2)
        else:
            x = torch.transpose(x, 0, 1)

        x = self.input(x)
        x = self.mlp1(x)
        x = self.mlp2(x)
        x = self.mlp3(x)

        # Transpose to [batch_size, num_points, num_classes]
        x = torch.transpose(x, 1, 2)
        return F.log_softmax(x, dim=1)


## PointNet Trainer
class PointTrainerSeg():
    def __init__(self, model, train_set, test_set, opts, device):
        self.model = model
        self.device = torch.device(device)
        self.model.to(self.device)
        self.epochs = opts['epochs']
        self.opts = opts
        self.optimizer = torch.optim.Adam(model.parameters(), opts['lr'])  # optimizer method for gradient descent
        self.criterion = torch.nn.CrossEntropyLoss()  # loss function
        self.train_loader = torch.utils.data.DataLoader(dataset=train_set, batch_size=opts['batch_size'], shuffle=True)
        self.test_loader = torch.utils.data.DataLoader(dataset=test_set, batch_size=1, shuffle=False)
        self.stats = []

        self.best_acc = 0
        print(opts['model_out_path'])
        print(opts['class'])
        self.model_out_path = os.path.join(opts['model_out_path'][0], opts['class'])
        self.res_out_path = os.path.join(opts['res_out_path'][0], opts['class'])
        self.model_out_name = opts['model_out_name']
        self.res_out_name = opts['res_out_name']
        self.model.apply(self.weights_init)
        print(model)

    def weights_init(self, l):
        if isinstance(l, nn.Conv1d):
            nn.init.xavier_uniform_(l.weight)
            nn.init.zeros_(l.bias)

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
        outputs = torch.transpose(outputs, 1, 2)
        return self.criterion(outputs, labels)

    def train(self):
        self.model.train()
        t0 = time.time()
        for epoch in range(self.epochs):
            self.tr_loss = []

            for i, (x, labels, _) in enumerate(self.train_loader):
                x, labels = x.to(self.device), labels.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(x)

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
        for i, (x, labels, _) in enumerate(self.test_loader):
            x, labels = x.to(self.device), labels.to(self.device)

            with torch.no_grad():
                outputs = self.model(x)  # Forward pass

            # Calculate loss (assuming CrossEntropyLoss is used)
            loss = self.compute_loss(outputs, labels)
            self.test_loss.append(loss.item())

            # Calculate accuracy
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
            model_out_path = os.path.join(self.model_out_path, self.model_out_name[0])
            torch.save(self.model.state_dict(), model_out_path)

    def get_stats(self):
        return self.stats