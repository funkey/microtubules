import pylp
from l1_graph import L1Graph
from l2_graph import L2Graph
from graph_converter import l1_to_l2
from solver import L2GraphSolver

def create_l1_graph():

    l1_graph = L1Graph(10)

    for n in range(9):
        l1_graph.add_edge(n,n+1)

    return l1_graph

if __name__ == "__main__":

    print "Creating L1 graph..."
    l1_graph = create_l1_graph()

    print "Converting to L2 graph..."
    (l2_graph, l2_node_to_l1_edges) = l1_to_l2(l1_graph)

    # select as many as possible
    for i in range(l2_graph.num_nodes):
        # start edge?
        if L2Graph.START_EDGE in l2_node_to_l1_edges[i]:
            l2_graph.set_cost(i, -0.5)
        else:
            l2_graph.set_cost(i, -1)

    print "Create ILP...."
    solver = L2GraphSolver(l2_graph)

    print "Solving...."
    solution = solver.solve()

    sum = 0
    for i in range(len(solution)):
        if len(solution) <= 100:
            print "y_" + str(i) + ": " + str(solution[i])
        if solution[i] > 0.5:
            sum += 1
    print "numer of non-zeros in solution: " + str(sum)

    print "Selected L1 edges:"
    for n in l2_node_to_l1_edges.keys():
        if solution[n] > 0.5:
            print l2_node_to_l1_edges[n]
