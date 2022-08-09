### The Ripple-Spreading Algorithm for the *k* Shortest Path Problem

##### Reference: Hu X B, Zhang C, Zhang G P, et al. Finding the k shortest paths by ripple-spreading algorithms[J]. Engineering Applications of Artificial Intelligence, 2020, 87: 103229.

The k shortest paths problem aims to find the k shortest paths between two nodes. 

| Variables     | Meaning                                                      |
| ------------- | ------------------------------------------------------------ |
| network       | Dictionary, {node 1: {node 2: [weight 1, weight 2, ...], ...}, ...} |
| s_network     | The network described by a crisp weight on which we conduct the ripple relay race |
| source        | The source node                                              |
| destination   | The destination node                                         |
| k             | The *k* shortest paths                                       |
| nn            | The number of nodes                                          |
| neighbor      | Dictionary, {node1: [the neighbor nodes of node1], ...}      |
| v             | The ripple-spreading speed (i.e., the minimum length of arcs) |
| t             | The simulated time index                                     |
| nr            | The number of ripples - 1                                    |
| epicenter_set | List, the epicenter node of the i-th ripple is epicenter_set[i] |
| path_set      | List, the path of the i-th ripple from the source node to node i is path_set[i] |
| radius_set    | List, the radius of the i-th ripple is radius_set[i]         |
| active_set    | List, active_set contains all active ripples                 |
| objective_set | List, the objective value of the traveling path of the i-th ripple is objective_set[i] |
| Omega         | Dictionary, Omega[n] contains all ripples generated at node n |

#### Example

![k-SPP_example](C:\Users\dell\Desktop\研究生\个人算法主页\The ripple-spreading algorithm for the k shortest paths problem\k-SPP_example.png)

The source node is node 0, and the destination node is node 5. The aim is to find the four shortest paths.

```python
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
```

##### Output:

```python
{
    1: {'path': [0, 3, 2, 5], 'length': 5}, 
    2: {'path': [0, 3, 4, 5], 'length': 7}, 
    3: {'path': [0, 3, 2, 4, 5], 'length': 8}, 
    4: {'path': [0, 1, 2, 5], 'length': 8},
}
```

