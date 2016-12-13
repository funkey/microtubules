import pylp
import random
from l1_graph import L1Graph
from l2_graph import L2Graph
from graph_converter import l1_to_l2
from solver import L2GraphSolver
from io import write_itk_graph

def set_random_positions(graph):

    for n in range(graph.num_nodes):
        graph.positions[n] = (
                int(random.random()*100),
                int(random.random()*100),
                int(random.random()*100)
        )

def create_l1_graphs():

    chain = L1Graph(10)
    for n in range(9):
        chain.add_edge(n,n+1)

    full = L1Graph(10)
    for i in range(10):
        for j in range(i+1, 10):
            full.add_edge(i,j)

    star = L1Graph(10)
    for i in range(1, 10):
        star.add_edge(0,i)

    single_node = L1Graph(1)

    num_nodes = 100
    num_edges = 1000
    randomized = L1Graph(num_nodes)
    random.seed(42)
    for (u,v) in [ (random.randint(0, num_nodes-1), random.randint(0, num_nodes-1)) for i in range(num_edges) ]:
        if u != v:
            randomized.add_edge(u, v)

    graphs = { 'chain': chain, 'full': full, 'star': star, 'single_node': single_node, 'randomized': randomized }

    for (_, graph) in graphs.iteritems():
        set_random_positions(graph)

    return graphs

if __name__ == "__main__":

    pylp.setLogLevel(pylp.LogLevel.Debug)

    print "Creating L1 graphs..."

    for (name, l1_graph) in create_l1_graphs().iteritems():

        print "Converting to L2 graph..."
        (l2_graph, l2_node_to_l1_edges) = l1_to_l2(l1_graph)

        # select as many as possible (but not so many start edges)
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

        selected_edges = set()
        for n in l2_node_to_l1_edges.keys():
            if solution[n] > 0.5:
                for e in l2_node_to_l1_edges[n]:
                    if e != L2Graph.START_EDGE:
                        selected_edges.add(e)

        print "Selected L1 edges:"
        print selected_edges

        write_itk_graph(l1_graph, name + '.itk', id=1)
        write_itk_graph(l1_graph, name + '_solution.itk', selected_edges, id=2)
