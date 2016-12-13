import pylp

class L2GraphSolver:

    def __init__(self, graph):

        self.backend = pylp.GurobiBackend()
        #self.backend = pylp.ScipBackend()
        self.backend.initialize(graph.num_nodes, pylp.VariableType.Binary)

        self.objective = pylp.LinearObjective(graph.num_nodes)
        for n in range(graph.num_nodes):
            self.objective.set_coefficient(n, graph.costs[n])
        self.backend.set_objective(self.objective)

        self.constraints = pylp.LinearConstraints()
        for conflict in graph.conflicts:
            constraint = pylp.LinearConstraint()
            for n in conflict:
                constraint.set_coefficient(n, 1)
            constraint.set_relation(pylp.Relation.LessEqual)
            constraint.set_value(1)
            self.constraints.add(constraint)

        for equal_sum_constraint in graph.equal_sum_constraints:

            nodes1 = equal_sum_constraint[0]
            nodes2 = equal_sum_constraint[1]

            constraint = pylp.LinearConstraint()
            for n in nodes1:
                constraint.set_coefficient(n, 1)
            for n in nodes2:
                constraint.set_coefficient(n, -1)
            constraint.set_relation(pylp.Relation.Equal)
            constraint.set_value(0)
            self.constraints.add(constraint)

        self.backend.set_constraints(self.constraints)

    def solve(self):

        solution = pylp.Solution()
        self.backend.solve(solution)

        return solution
