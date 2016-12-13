import pylp
from l2_graph import L2Graph
from solver import L2GraphSolver
import random

def create_random_graph(num_nodes = 100, num_conflicts = 100, num_implications = 50):

    graph = L2Graph(num_nodes)

    for i in range(num_nodes):
        graph.set_cost(i, 1.0 - 2*random.random())

    for i in range(num_conflicts):

        u = random.randint(0, num_nodes-1)
        v = random.randint(0, num_nodes-1)

        if u != v:
            graph.add_conflict([u, v])

    for i in range(num_implications):

        source = random.randint(0, num_nodes-1)
        targets = [ random.randint(0, num_nodes-1) for j in range(num_nodes/10) ]
        graph.add_equal_sum_constraint([source], targets)

    return graph

if __name__ == "__main__":

    pylp.setLogLevel(pylp.LogLevel.Debug)

    random.seed(42)

    print "Create random graph...."
    #graph = create_random_graph(int(1e4), int(5e3), int(1e4))
    graph = create_random_graph(int(1e2), int(5e2), int(1e2))

    print "Create ILP...."
    solver = L2GraphSolver(graph)

    print "Solving...."
    solution = solver.solve()

    sum = 0
    for i in range(len(solution)):
        if len(solution) <= 100:
            print "y_" + str(i) + ": " + str(solution[i])
        if solution[i] > 0.5:
            sum += 1
    print "numer of non-zeros in solution: " + str(sum)
