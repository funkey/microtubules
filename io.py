def write_itk_graph(graph, filename, selected_edges = None, id = 0):

    with open(filename, 'w') as f:

        f.write('ID ' + str(id) + '\n')

        f.write('POINTS ' + str(graph.num_nodes) + ' FLOAT\n')
        for n in range(graph.num_nodes):
            f.write('%f %f %f\n'%graph.positions[n])

        edges = selected_edges if selected_edges is not None else range(graph.num_edges)
        f.write('EDGES ' + str(len(edges)) + '\n')
        for e in edges:
            f.write('%d %d\n'%graph.edges[e])
