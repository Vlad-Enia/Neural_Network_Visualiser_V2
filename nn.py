import torch.utils.data as data
import torch
import os
import numpy as np
from PointNet_Class import PointDataClass, PointNetClass, PointTrainerClass
from GCN_Class import GCNDataClass, GCNTrainerClass, GCNClass
from PointNet_Seg import PointNetSeg, PointSegData, PointTrainerSeg
from GCN_Seg import GCNSegTrainer, GCNSeg, GCNSegData
from drawPlot import vis_pts


def init_train(opts):
    if opts['task'] == 'class':
        if opts['net'] == 'pointnet':
            point_class_train(opts)
        elif opts['net'] == 'gcn':
            gcn_class_train(opts)
    elif opts['task'] == 'seg':
        if opts['net'] == 'pointnet':
            point_seg_train(opts)
        elif opts['net'] == 'gcn':
            gcn_seg_train(opts)


def point_class_train(opts):
    opts['out_name'] = 'point_class'
    dataset_name = 'modelnet_points_' + str(opts['n_pts'])

    dataset_train = PointDataClass('static/data/modelnet/data_points/' + dataset_name + '/train', noise=opts['noise'])
    dataset_test = PointDataClass('static/data/modelnet/data_points/' + dataset_name + '/test')
    opts['model_out_path'] = 'static/data/results/PointNet Classification/trained_models/' + dataset_name + '_lr_' + str(opts['lr']) + '_noise_' + str(opts['noise'])
    opts['res_out_path'] = 'static/data/results/PointNet Classification/results/' + dataset_name + '_lr_' + str(opts['lr']) + '_noise_' + str(opts['noise'])

    model = PointNetClass()

    trainer = PointTrainerClass(model=model, train_set=dataset_train, test_set=dataset_test, opts=opts, device='mps')
    trainer.train()


def gcn_class_train(opts):
    opts['out_name'] = 'gcn_class'
    if(opts['graph_alg']) == 'knn':
        dataset_name = 'modelnet_graphs_' + str(opts['n_pts']) + '_k' + str(opts['k']) + '_'
    elif(opts['graph_alg']) == 'rad':
        dataset_name = 'modelnet_graphs_' + str(opts['n_pts']) + '_r' + str(opts['r']) + '_'

    dataset_train = GCNDataClass('static/data/modelnet/data_graphs/' + dataset_name + '/train')
    dataset_test = GCNDataClass('static/data/modelnet/data_graphs/' + dataset_name + '/test')

    opts['model_out_path'] = 'static/data/results/GCN Classification/trained_models/' + dataset_name + 'lr_' + str(opts['lr'])
    opts['res_out_path'] = 'static/data/results/GCN Classification/results/' + dataset_name + 'lr_' + str(opts['lr'])

    model = GCNClass()
    trainer = GCNTrainerClass(model=model, train_set=dataset_train, test_set=dataset_test, opts=opts, device='cpu')
    trainer.train()


def point_seg_train(opts):
    n_train_samples = 100
    n_test_samples = 20
    n_points = opts['n_pts']
    lr = opts['lr']
    dataset_ver = 'data_points_' + str(n_points)
    class_ = opts['class']
    noise = opts['noise']

    dataset_train = PointSegData(os.path.join('static/data/shapenet/data_points', dataset_ver, 'train'), class_, n_train_samples, noise=noise)
    dataset_test = PointSegData(os.path.join('static/data/shapenet/data_points', dataset_ver, 'test'), class_, n_test_samples)

    n_classes = dataset_train.get_n_classes()

    model = PointNetSeg(n_classes)

    opts['model_out_path'] = os.path.join('static/data/results/PointNet Segmentation/trained_models', dataset_ver + '_lr_' + str(lr)),

    opts['res_out_path'] = os.path.join('static/data/results/PointNet Segmentation/results', dataset_ver + '_lr_' + str(lr)),
    opts['model_out_name'] = 'pointnet_1.pt',
    opts['res_out_name'] = 'pointnet_1.csv'

    trainer = PointTrainerSeg(model=model, train_set=dataset_train, test_set=dataset_test, opts=opts, device='mps')

    trainer.train()


def gcn_seg_train(opts):
    n_train_samples = 100
    n_test_samples = 20
    n_points = 1000
    lr = opts['lr']
    class_ = opts['class']
    alg = opts['graph_alg']
    k = opts['k']
    r = opts['r']

    if alg == 'knn':
        dataset_ver = 'data_graph_' + str(n_points) + '_k' + str(k) + '_'
    elif alg == 'rad':
        dataset_ver = 'data_graph_' + str(n_points) + '_r' + str(r) + '_'


    dataset_train = GCNSegData(os.path.join('static/data/shapenet/data_graph', dataset_ver, 'train'), class_, n_train_samples)
    dataset_test = GCNSegData(os.path.join('static/data/shapenet/data_graph', dataset_ver, 'test'), class_, n_test_samples)

    n_classes = dataset_train.get_n_classes()

    model = GCNSeg(n_classes)

    opts['model_out_path'] = os.path.join('static/data/results/GCN Segmentation/trained_models',dataset_ver + '_lr_' + str(lr)),

    opts['res_out_path'] = os.path.join('static/data/results/GCN Segmentation/results',dataset_ver + '_lr_' + str(lr)),
    opts['model_out_name'] = 'pointnet_1.pt',
    opts['res_out_name'] = 'pointnet_1.csv'

    trainer = PointTrainerSeg(model=model, train_set=dataset_train, test_set=dataset_test, opts=opts, device='mps')
    (trainer.train())



def load_model(model_path, task, net, device, n_classes):
    model = ''
    if task == 'class':
        if net == 'pointnet':
            model = PointNetClass()
        else:
            model = GCNClass()
    elif task == 'seg':
        if net == 'pointnet':
            model = PointNetSeg(n_classes)
        else:
            model = GCNSeg(n_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    device = torch.device(device)
    model.to(device)
    return model

def predict(opts):
    n_pts = opts['n_pts']
    class_ = opts['class']
    lr = opts['lr']
    alg = opts['graph_alg']
    if opts['net'] == 'pointnet':
        dataset_ver = 'data_points_' + str(n_pts)
        dataset_test = PointSegData(os.path.join('static/data/shapenet/data_points', dataset_ver, 'test'), class_, 20)
        pts, labels, n_classes = dataset_test[0]
        x = pts.to(torch.device('cpu'))
        x = x.unsqueeze(0)
        model_path = os.path.join('static/data/results/PointNet Segmentation/trained_models', dataset_ver + '_lr_' + str(lr), class_, 'pointnet_1.pt')
        model = load_model(model_path, opts['task'], opts['net'], torch.device('cpu'),  n_classes)

        with torch.no_grad():
            outputs = model(x)
            _, predicted = torch.max(outputs, 2)
    elif opts['net'] == 'gcn':
        k = opts['k']
        r = opts['r']
        if alg == 'knn':
            dataset_ver = 'data_graph_' + str(n_pts) + '_k' + str(k) + '_'
        elif alg == 'rad':
            dataset_ver = 'data_graph_' + str(n_pts) + '_r' + str(r) + '_'
        dataset_test = GCNSegData(os.path.join('static/data/shapenet/data_graph', dataset_ver, 'test'), class_, 20)
        pts, _, _, labels, n_classes = dataset_test[0]
        x = pts.to(torch.device('cpu'))
        x = x.unsqueeze(0)
        model_path = os.path.join('static/data/results/GCN Segmentation/trained_models', dataset_ver + '_lr_' + str(lr), class_, 'pointnet_1.pt')
        model = load_model(model_path, opts['task'], opts['net'], torch.device('cpu'), n_classes)

        with torch.no_grad():
            outputs = model(x)
            _, predicted = torch.max(outputs, 2)

    fig_act = vis_pts(pts.numpy(), n_pts, labels.squeeze().numpy(), class_)
    fig_pred = vis_pts(pts.numpy(), n_pts, predicted.squeeze().numpy(), class_)

    return fig_act, fig_pred


def test_model(model_path, task, model_name, dataset_test, device, n_classes):
    model = load_model(model_path, task, model_name, device, n_classes)
    device = torch.device(device)
    model.eval()
    test_accuracy = []
    if model_name == 'pointnet':
        if task == 'class':
            for i, (x, labels) in enumerate(dataset_test):
                x, labels = x.to(device), labels.to(device)

                with torch.no_grad():
                    outputs = model(x)  # Forward pass

                outputs = outputs[0]
                outputs = outputs.unsqueeze(0)
                _, predicted = torch.max(outputs, 1)  # Get predicted classes per point

                # Compare predictions to true labels
                correct = predicted.eq(labels.view_as(predicted))
                # Calculate accuracy for this batch
                accuracy = torch.mean(correct.float())
                test_accuracy.append(accuracy.item())
        elif task == 'seg':
            for i, (x, labels, _) in enumerate(dataset_test):
                x, labels = x.to(device), labels.to(device)

                with torch.no_grad():
                    outputs = model(x)  # Forward pass

                _, predicted = torch.max(outputs, 2)  # Get predicted classes per point

                # Compare predictions to true labels
                correct = predicted.eq(labels.view_as(predicted))
                # Calculate accuracy for this batch
                accuracy = torch.mean(correct.float())
                test_accuracy.append(accuracy.item())
    elif  model_name == 'gcn':
        if task == 'class':
            for i, (x, edges, weights, labels) in enumerate(dataset_test):
                x, edges, weights, labels = x.to(device), edges.to(device), weights.to(device), labels.to(device)

                with torch.no_grad():
                    outputs = model(x, edges, weights)

                outputs = outputs.unsqueeze(0)
                _, predicted = torch.max(outputs, 2)  # Get predicted classes per point

                # Compare predictions to true labels
                correct = predicted.eq(labels.view_as(predicted))
                # Calculate accuracy for this batch
                accuracy = torch.mean(correct.float())
                test_accuracy.append(accuracy.item())
        if task == 'seg':
            for i, (x, edges, weights, labels, _) in enumerate(dataset_test):
                x, edges, weights, labels = x.to(device), edges.to(device), weights.to(device), labels.to(device)

                with torch.no_grad():
                    outputs = model(x, edges, weights)

                outputs = outputs.unsqueeze(0)
                _, predicted = torch.max(outputs, 2)  # Get predicted classes per point

                # Compare predictions to true labels
                correct = predicted.eq(labels.view_as(predicted))
                # Calculate accuracy for this batch
                accuracy = torch.mean(correct.float())
                test_accuracy.append(accuracy.item())

    return np.mean(test_accuracy)


def test_resistance(opts):
    n_classes = 0
    if opts['task'] == 'class':
        if opts['net'] == 'pointnet':
            dataset_name = 'modelnet_points_' + str(opts['n_pts'])
            path = 'static/data/modelnet/data_points/' + dataset_name
            dataset_test = PointDataClass(path+ '/test')
            dataset_test_stretch = PointDataClass(path + '_stretch'+ '/test')
            dataset_test_translate = PointDataClass(path + '_translate'+ '/test')
            model_path = 'static/data/results/PointNet Classification/trained_models/' + dataset_name + '_lr_' + str(opts['lr']) + '_noise_' + str(opts['noise']) + '/point_class.pt'
        elif opts['net'] == 'gcn':
            if (opts['graph_alg']) == 'knn':
                dataset_name = 'modelnet_graphs_' + str(opts['n_pts']) + '_k' + str(opts['k'])
            elif (opts['graph_alg']) == 'rad':
                dataset_name = 'modelnet_graphs_' + str(opts['n_pts']) + '_r' + str(opts['r'])
            path = 'static/data/modelnet/data_graphs/' + dataset_name + '_'
            dataset_test = GCNDataClass(path+ '/test')
            dataset_test_stretch = GCNDataClass(path + 'stretch'+ '/test')
            dataset_test_translate = GCNDataClass(path + 'translate'+ '/test')
            model_path = 'static/data/results/GCN Classification/trained_models/' + dataset_name + '_lr_' + str(opts['lr']) + '/gcn_class.pt'
    elif opts['task'] == 'seg':
        if opts['net'] == 'pointnet':
            dataset_ver = 'data_points_' + str(opts['n_pts'])
            path = os.path.join('static/data/shapenet/data_points', dataset_ver)
            dataset_test = PointSegData(path + '/test', opts['class'], 20)
            dataset_test_stretch = PointSegData(path + '_stretch'+ '/test', opts['class'], 20)
            dataset_test_translate = PointSegData(path + '_translate'+ '/test', opts['class'], 20)
            n_classes = dataset_test.get_n_classes()
            dataset_test = torch.utils.data.DataLoader(dataset=dataset_test, batch_size=1, shuffle=False)
            dataset_test_stretch = torch.utils.data.DataLoader(dataset=dataset_test_stretch, batch_size=1, shuffle=False)
            dataset_test_translate = torch.utils.data.DataLoader(dataset=dataset_test_translate, batch_size=1,
                                                                shuffle=False)
            model_path = os.path.join('static/data/results/PointNet Segmentation/trained_models', dataset_ver + '_lr_' + str(opts['lr']), opts['class'], 'pointnet_1.pt')
        elif opts['net'] == 'gcn':
            if (opts['graph_alg']) == 'knn':
                dataset_name = 'modelnet_graphs_' + str(opts['n_pts']) + '_k' + str(opts['k'])
            elif (opts['graph_alg']) == 'rad':
                dataset_name = 'modelnet_graphs_' + str(opts['n_pts']) + '_r' + str(opts['r'])
            path = os.path.join('static/data/shapenet/data_graph', dataset_name + '_')
            dataset_test = GCNSegData(path+ '/test', opts['class'], 20)
            n_classes = dataset_test.get_n_classes()
            dataset_test_stretch = GCNSegData(path + 'stretch'+ '/test', opts['class'], 20)
            dataset_test_translate = GCNSegData(path + 'translate'+ '/test', opts['class'], 20)
            model_path = os.path.join('static/data/results/GCN Segmentation/trained_models', dataset_name + '_lr_' + str(opts['lr']),opts['class'], 'gcn_1.pt')


    data = [
        [opts['net']]
    ]

    acc = "{:.2f}".format(test_model(model_path, opts['task'], opts['net'], dataset_test, torch.device('cpu'), n_classes))
    acc_stretch = "{:.2f}".format(test_model(model_path, opts['task'], opts['net'], dataset_test_stretch, torch.device('cpu'),  n_classes))
    acc_translate = "{:.2f}".format(test_model(model_path, opts['task'], opts['net'], dataset_test_translate, torch.device('cpu'),  n_classes))
    data.append([acc])
    data.append([acc_stretch])
    data.append([acc_translate])
    return data