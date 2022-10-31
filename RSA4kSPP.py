#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/8 12:15
# @Author  : Xavier Ma
# @Email   : xavier_mayiming@163.com
# @File    : RSA4kSPP.py
# @Statement : The ripple-spreading algorithm for the k-shortest paths problem
# @Reference : Hu X B, Zhang C, Zhang G P, et al. Finding the k shortest paths by ripple-spreading algorithms[J]. Engineering Applications of Artificial Intelligence, 2020, 87: 103229.
import copy


def find_neighbor(network):
    """
    Find the neighbor of each node
    :param network:
    :return: {node 1: [the neighbor nodes of node 1], ...}
    """
    nn = len(network)
    neighbor = []
    for i in range(nn):
        neighbor.append(list(network[i].keys()))
    return neighbor


def find_speed(network, neighbor):
    """
    Find the ripple-spreading speed
    :param network:
    :param neighbor:
    :return:
    """
    speed = 1e10
    for i in range(len(network)):
        for j in neighbor[i]:
            speed = min(speed, network[i][j])
    return speed


def main(network, source, destination, k):
    """
    The ripple-spreading algorithm for the k shortest path problem
    :param network: {node1: {node2: length, node3: length, ...}, ...}
    :param source: the source node
    :param destination: the destination node
    :param k: the k shortest paths
    :return:
    """
    # Step 1. Initialization
    nn = len(network)  # node number
    neighbor = find_neighbor(network)  # the neighbor set
    v = find_speed(network, neighbor)  # the ripple-spreading speed
    t = 0  # simulated time index
    nr = 0  # the current number of ripples - 1
    epicenter_set = []  # epicenter set
    radius_set = []  # radius set
    length_set = []  # length set
    path_set = []  # path set
    active_set = []  # the set containing all active ripples
    omega = {}  # the set that records the ripple generated at each node
    for node in range(nn):
        omega[node] = []

    # Step 2. Initialize the first ripple
    epicenter_set.append(source)
    radius_set.append(0)
    length_set.append(0)
    path_set.append([source])
    active_set.append(nr)
    omega[source].append(nr)
    nr += 1

    # Step 3. The main loop
    while len(omega[destination]) < k:

        # Step 3.1. If there is feasible solution
        if not active_set:
            print('No feasible solution!')
            return []

        # Step 3.2. Time updates
        t += 1
        incoming_ripples = {}

        for ripple in active_set:

            # Step 3.3. Active ripples spread out
            radius_set[ripple] += v

            # Step 3.4. New incoming ripples
            epicenter = epicenter_set[ripple]
            path = path_set[ripple]
            radius = radius_set[ripple]
            length = length_set[ripple]
            for node in neighbor[epicenter]:
                if len(omega[node]) < k:  # the node is visited no more than k times
                    temp_length = network[epicenter][node]
                    if temp_length <= radius < temp_length + v:
                        temp_path = copy.deepcopy(path)
                        temp_path.append(node)
                        if node in incoming_ripples.keys():
                            incoming_ripples[node].append({
                                'path': temp_path,
                                'radius': radius - temp_length,
                                'length': length + temp_length,
                            })
                        else:
                            incoming_ripples[node] = [{
                                'path': temp_path,
                                'radius': radius - temp_length,
                                'length': length + temp_length,
                            }]

        # Step 3.5. Generate new ripples
        for node in incoming_ripples.keys():
            new_ripples = sorted(incoming_ripples[node], key=lambda x: x['radius'], reverse=True)
            if len(omega[node]) + len(new_ripples) > k:
                new_ripples = new_ripples[: k - len(omega[node])]
            for item in new_ripples:
                path_set.append(item['path'])
                epicenter_set.append(node)
                radius_set.append(item['radius'])
                length_set.append(item['length'])
                active_set.append(nr)
                omega[node].append(nr)
                nr += 1

        # Step 3.6. Active -> Inactive
        remove_ripple = []
        for ripple in active_set:
            epicenter = epicenter_set[ripple]
            radius = radius_set[ripple]
            flag_inactive = True
            for node in neighbor[epicenter]:
                if radius < network[epicenter][node] and len(omega[node]) < k:
                    flag_inactive = False
                    break
            if flag_inactive:
                remove_ripple.append(ripple)
        for ripple in remove_ripple:
            active_set.remove(ripple)

    # Step 4. Sort the results
    result = {}
    index = 1
    for ripple in omega[destination]:
        result[index] = {
            'path': path_set[ripple],
            'length': length_set[ripple],
        }
        index += 1
    return result


if __name__ == '__main__':
    test_network = {
        0: {1: 3, 3: 2},
        1: {2: 4},
        2: {4: 2, 5: 1},
        3: {1: 1, 2: 2, 4: 3},
        4: {5: 2},
        5: {},
    }
    source_node = 0
    destination_node = 5
    k_num = 4
    print(main(test_network, source_node, destination_node, k_num))
