import collections
import math
import random
import numpy as np
import pickle


def CREATE_IDS(data_train, ids):
    for line in data_train:
        y, txt = line.split('\t')
        txt = txt.lower()
        words = txt.split()
        for word in words:
            ids['UNI:' + word]


def CREATE_FEATURES(txt, ids, flag_test=0):
    phi_0 = [0 for i in range(len(ids))]
    words = txt.split()
    for word in words:
        if flag_test == 1:
            if ('UNI:' + word) not in ids.keys():
                continue
        phi_0[ids['UNI:' + word]] += 1

    return phi_0


def FORWARD_NN(network, phi_0):
    phi = [None for i in range(len(network) + 1)]
    phi[0] = phi_0
    for i in range(len(network)):
        w, b = network[i]
        phi[i+1] = np.tanh(np.dot(w, phi[i]) + b)

    return phi


def BACKWARD_NN(network, phi, y, num_node):
    error = [0, 0, np.array([y - phi[len(network)][0]])]
    gra = [0, 0, 0]
    for i in range(len(network) - 1, -1, -1):
        gra[i+1] = error[i+1]*(1 - phi[i+1]**2)
        w, b = network[i]
        error[i] = np.dot(gra[i+1], w)

    return gra, error


def UPDATE_WEIGHTS(network, phi, gra, rate_train, num_node):
    for i in range(len(network)):
        # w, b = network[i][0], network[i][1]
        w, b = network[i]
        network[i][0] += rate_train*np.outer(gra[i+1], phi[i])
        network[i][1] += rate_train*gra[i+1]


def train_nn(data_train_list, network, num_node, ids):
    rate_train = 0.050

    for line in data_train_list:
        y, txt = line.split('\t')
        y = int(y)
        txt = txt.lower()
        phi_0 = CREATE_FEATURES(txt, ids)
        phi = FORWARD_NN(network, phi_0)
        gra, error = BACKWARD_NN(network, phi, y, num_node)
        UPDATE_WEIGHTS(network, phi, gra, rate_train, num_node)


def train_nn_epoch(epoch, ids, path_data_train, num_node, path_data_network, path_data_ids):
    with open(path_data_train, 'r') as data_train:
        CREATE_IDS(data_train, ids)
    with open(path_data_ids, 'w') as data_ids:
        for key, value in ids.items():
            print('{}\t{}'.format(key, value), file=data_ids)

    w_0 = np.array((np.random.rand(num_node, len(ids))-0.5)/5)
    b_0 = (np.random.rand(num_node) - 0.5) / 5
    w_1 = np.array([(np.random.rand(num_node)-0.5)/5])
    b_1 = (np.random.rand(1) - 0.5) / 5
    network = [[w_0, b_0], [w_1, b_1]]

    for num_epoch in range(epoch):
        with open(path_data_train, 'r') as data_train:
            data_train_list = list(data_train)
            random.shuffle(data_train_list)
            train_nn(data_train_list, network, num_node, ids)
    with open(path_data_network, 'wb') as data_network:
        pickle.dump(network, data_network)


if __name__ == '__main__':
    epoch = 2
    num_node = 2
    ids = collections.defaultdict(lambda: len(ids))
    path_data_train = '../../data/titles-en-train.labeled'
    path_data_network = 'train_nn_network.result'
    path_data_ids = 'train_nn_ids.result'
    train_nn_epoch(epoch, ids, path_data_train, num_node, path_data_network, path_data_ids)
