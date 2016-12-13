class L2Graph:

    def __init__(self, num_ids):

        self.num_ids = num_ids

        self.costs = [0]*num_ids

        # tuple of ids in conflict
        self.conflicts = []

        # map from id to list of implied ids
        self.implications = {}

    def add_conflict(self, exclusive_ids):

        for n in exclusive_ids:
            self.__check_id(n)

        self.conflicts.append(exclusive_ids)

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

