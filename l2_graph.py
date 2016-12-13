class L2Graph:

    START_EDGE = -1

    def __init__(self, num_nodes):

        self.num_nodes = num_nodes

        self.costs = [0]*num_nodes

        # tuple of nodes in conflict
        self.conflicts = []

        # tuple of sets of nodes which should have same number of selections
        self.equal_sum_constraints = []

    def add_conflict(self, exclusive_nodes):

        for n in exclusive_nodes:
            self.__check_id(n)

        self.conflicts.append(exclusive_nodes)

    def add_equal_sum_constraint(self, nodes1, nodes2):
        '''Require that the number of selected nodes in nodes1 is equal to the 
        number of selected nodes in nodes2.'''

        for n in nodes1 + nodes2:
            self.__check_id(n)

        self.equal_sum_constraints.append((list(nodes1), list(nodes2)))

    def set_cost(self, n, cost):

        self.__check_id(n)
        self.costs[n] = cost

    def set_costs(self, costs):

        assert(len(costs) == len(self.costs))
        self.costs = costs

    def __check_id(self, n):

        if n >= self.num_nodes:
            raise RuntimeError("exceeded number of IDs (" + str(self.num_nodes) + ")")

