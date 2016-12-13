class L1Graph:

    def __init__(self, num_nodes):

        self.num_nodes = num_nodes
        self.num_edges = 0
        self.incident = {}
        self.edges    = []

        # node properties
        self.orientations = {}
        self.positions    = {}

    def add_edge(self, u, v):

        self.__check_id(u)
        self.__check_id(v)

        e = self.__add_edge(u, v)
        self.__add_incident(u, e)
        self.__add_incident(v, e)

        return e

    def get_incident_edges(self, n):

        self.__check_id(n)

        return self.incident[n]

    def __add_edge(self, u, v):

        id = len(self.edges)
        self.edges.append((u, v))
        return id

    def __add_incident(self, u, v):

        if u not in self.incident:
            self.incident[u] = []
        self.incident[u].append(v)

    def __check_id(self, n):

        if n >= self.num_nodes:
            raise RuntimeError("exceeded number of IDs (" + str(self.num_nodes) + ")")

