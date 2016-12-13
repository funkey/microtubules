import pylp
import random

class L2Graph:

    def __init__(self, num_ids):

        self.num_ids = num_ids

        self.costs = [0]*num_ids

        # tuple of ids in conflict
        self.conflicts = []

        # map from id to list of implied ids
        self.implications = {}

    def add_conflict(self, u, v):

        self.__check_id(u)
        self.__check_id(v)

        self.conflicts.append((u,v))

    def add_implication(self, source, targets):
        '''Add targets (list of ids) as implications of source (single id).

        This means that if source is selected, at least one of targets has to be 
        selected as well. If multiple implications for one source are set, all 
        of them have to be fulfilled.
        '''

        self.__check_id(source)
        for n in targets:
            self.__check_id(n)

        #self.implications[source] -> [ [1,2,3], [4,5] ]
        #                          -> (1 or 2 or 3) and (4 or 5)

        if source not in self.implications:
            self.implications[source] = []
        self.implications[source].append(targets)

    def set_cost(self, n, cost):

        self.__check_id(n)
        self.costs[n] = cost

    def set_costs(self, costs):

        assert(len(costs) == len(self.costs))
        self.costs = costs

    def __check_id(self, n):

        if n >= self.num_ids:
            raise RuntimeError("exceeded number of IDs (" + str(self.num_ids) + ")")


class L2GraphSolver:

    def __init__(self, graph):

        self.backend = pylp.GurobiBackend()
        self.backend.initialize(graph.num_ids, pylp.VariableType.Binary)

        self.objective = pylp.LinearObjective(graph.num_ids)
        for n in range(graph.num_ids):
            self.objective.set_coefficient(n, graph.costs[n])
        self.backend.set_objective(self.objective)

        self.constraints = pylp.LinearConstraints()
        for conflict in graph.conflicts:
            constraint = pylp.LinearConstraint()
            constraint.set_coefficient(conflict[0], 1)
            constraint.set_coefficient(conflict[1], 1)
            constraint.set_relation(pylp.Relation.LessEqual)
            constraint.set_value(1)
            self.constraints.add(constraint)

        for source in graph.implications.keys():
            for targets in graph.implications[source]:
                constraint = pylp.LinearConstraint()
                for target in targets:
                    constraint.set_coefficient(target, 1)
                constraint.set_coefficient(source, -1)
                constraint.set_relation(pylp.Relation.GreaterEqual)
                constraint.set_value(0)
                self.constraints.add(constraint)

        self.backend.set_constraints(self.constraints)

    def solve(self):

        solution = pylp.Solution()
        self.backend.solve(solution)

        return solution

def create_random_graph(num_ids = 100, num_conflicts = 100, num_implications = 50):

    graph = L2Graph(num_ids)

    for i in range(num_ids):
        graph.set_cost(i, 1.0 - 2*random.random())

    for i in range(num_conflicts):

        u = random.randint(0, num_ids-1)
        v = random.randint(0, num_ids-1)

        if u != v:
            graph.add_conflict(u, v)

    for i in range(num_implications):

        source = random.randint(0, num_ids-1)
        targets = [ random.randint(0, num_ids-1) for j in range(num_ids/10) ]
        graph.add_implication(source, targets)

    return graph

if __name__ == "__main__":

    pylp.setLogLevel(pylp.LogLevel.Debug)

    print "Create random graph...."
    graph = create_random_graph(int(1e4), int(5e3), int(1e4))

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
