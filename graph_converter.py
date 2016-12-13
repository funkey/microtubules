from l2_graph import L2Graph

def l1_to_l2(l1_graph):
    '''Convert an L1 graph into an L2 graph.

    Returns (l2_graph, l2_node_to_l1_edges): The L2 graph, and a dictonary to 
    map L2 nodes to L1 edges.
    '''

    # one l2 node for every connected pair of edges in l1 graph

    l1_edge_to_l2_nodes = {}
    l2_node_to_l1_edges = {}

    # o----o----o    == l2 node (the whole thing)
    #      ^         == center l1 node of this l2 node
    center_l1_node = {}

    num_l2_nodes = 0
    conflicts = []
    implications = {}

    # find all l2 nodes, and conflict sets as well
    for n in range(l1_graph.num_nodes):

        conflict = []

        # l2 node selecting two l1 edges (or one l1 edge and START_EDGE)
        for e1 in l1_graph.get_incident_edges(n):
            for e2 in l1_graph.get_incident_edges(n) + [L2Graph.START_EDGE]:

                if e1 >= e2 and e2 != L2Graph.START_EDGE:
                    continue

                # create a new variable for (e1, e2)
                var_num = num_l2_nodes
                num_l2_nodes += 1
                l2_node_to_l1_edges[var_num] = (e1, e2)

                # all edge pairs centered around n are in conflict
                conflict.append(var_num)

                # lookup from l1 edge to l2 node it is used in
                if not e1 in l1_edge_to_l2_nodes:
                    l1_edge_to_l2_nodes[e1] = []
                if not e2 in l1_edge_to_l2_nodes:
                    l1_edge_to_l2_nodes[e2] = []
                l1_edge_to_l2_nodes[e1].append(var_num)
                l1_edge_to_l2_nodes[e2].append(var_num)

                # remember the center l1 node of this l2 node
                center_l1_node[var_num] = n

        conflicts.append(conflict)

    # create the l2 graph
    l2_graph = L2Graph(num_l2_nodes)

    # conflict constraints between pairs that don't form a chain
    for conflict in conflicts:
        l2_graph.add_conflict(conflict)

    # continuation constraints
    for e in range(len(l1_graph.edges)):

        # get all l2 nodes using it, divided by "left" and "right"
        l2_nodes = l1_edge_to_l2_nodes[e]

        left_l1_node  = l1_graph.edges[e][0]
        right_l1_node = l1_graph.edges[e][1]

        left_l2_nodes  = [ l2_node for l2_node in l2_nodes if center_l1_node[l2_node] == left_l1_node  ]
        right_l2_nodes = [ l2_node for l2_node in l2_nodes if center_l1_node[l2_node] == right_l1_node ]

        assert(len(left_l2_nodes) + len(right_l2_nodes) == len(l2_nodes))

        # number of selected nodes in "left" has to be equal to "right"
        l2_graph.add_equal_sum_constraint(left_l2_nodes, right_l2_nodes)

    return (l2_graph, l2_node_to_l1_edges)
