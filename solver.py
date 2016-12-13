import pylp

class L2GraphSolver:

    def __init__(self, graph):

        #self.backend = pylp.GurobiBackend()
        self.backend = pylp.ScipBackend()
        self.backend.initialize(graph.num_ids, pylp.VariableType.Binary)

        self.objective = pylp.LinearObjective(graph.num_ids)
        for n in range(graph.num_ids):
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
