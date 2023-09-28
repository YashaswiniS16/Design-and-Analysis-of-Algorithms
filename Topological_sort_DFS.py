from networkx import draw, DiGraph, spring_layout
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        # dictionary containing keys that map to the corresponding vertex object
        self.vertices = {}

    def add_vertex(self, key):
        """Add a vertex with the given key to the graph."""
        vertex = Vertex(key)
        self.vertices[key] = vertex

    def get_vertex(self, key):
        """Return vertex object with the corresponding key."""
        return self.vertices[key]

    def __contains__(self, key):
        return key in self.vertices

    def add_edge(self, src_key, dest_key, weight=1):
        """Add edge from src_key to dest_key with given weight."""
        self.vertices[src_key].add_neighbour(self.vertices[dest_key], weight)

    def does_edge_exist(self, src_key, dest_key):
        """Return True if there is an edge from src_key to dest_key."""
        return self.vertices[src_key].does_it_point_to(self.vertices[dest_key])

    def __iter__(self):
        return iter(self.vertices.values())


class Vertex:
    def __init__(self, key):
        self.key = key
        self.points_to = {}

    def get_key(self):
        """Return key corresponding to this vertex object."""
        return self.key

    def add_neighbour(self, dest, weight):
        """Make this vertex point to dest with given edge weight."""
        self.points_to[dest] = weight

    def get_neighbours(self):
        """Return all vertices pointed to by this vertex."""
        return self.points_to.keys()

    def get_weight(self, dest):
        """Get weight of edge from this vertex to dest."""
        return self.points_to[dest]

    def does_it_point_to(self, dest):
        """Return True if this vertex points to dest."""
        return dest in self.points_to


def get_topological_sorting(graph):
    """Return a topological sorting of the DAG. Return None if graph is not a DAG."""
    tlist = []
    visited = set()
    on_stack = set()
    for v in graph:
        if v not in visited:
            if not get_topological_sorting_helper(v, visited, on_stack, tlist):
                return None
    return tlist


def get_topological_sorting_helper(v, visited, on_stack, tlist):
    """Perform DFS traversal starting at vertex v and store a topological
    sorting of the DAG in tlist. Return False if it is found that the graph is
    not a DAG. Uses set visited to keep track of already visited nodes."""
    if v in on_stack:
        # graph has cycles and is therefore not a DAG.
        return False

    on_stack.add(v)
    for dest in v.get_neighbours():
        if dest not in visited:
            if not get_topological_sorting_helper(dest, visited, on_stack, tlist):
                return False
    on_stack.remove(v)
    visited.add(v)
    tlist.insert(0, v.get_key())  # prepend node key to tlist
    return True


def anime(graph, connections, wind_title):
    fig = plt.figure(figsize=(12, 6))
    fig.canvas.manager.set_window_title(wind_title)
    ind = (len(connections) - 1)
    for i in range(ind):
        graph.add_edges_from(connections[i])
        pos = spring_layout(graph)
        draw(
            graph, pos, edge_color='black', width=1, linewidths=1,
            node_size=500, node_color='pink', alpha=0.9,
            labels={node: node for node in graph.nodes()}
        )
        plt.show(block=False)
        plt.pause(2)
        plt.clf()
    graph.add_edges_from(connections[ind])
    pos = spring_layout(graph)
    draw(
        graph, pos, edge_color='black', width=1, linewidths=1,
        node_size=500, node_color='pink', alpha=0.9,
        labels={node: node for node in graph.nodes()}
    )
    plt.show(block=False)
    plt.pause(60)
    plt.clf()
    plt.close()


g = Graph()
print('Menu')
print('add vertex <key>')
print('add edge <src> <dest>')
print('topological')
print('display')
print('before_sort')
print('after_sort')
print('quit')
out = []
b_s = False
a_s = False
while True:
    do = input('What would you like to do? ').split()

    operation = do[0]
    if operation == 'add':
        suboperation = do[1]
        if suboperation == 'vertex':
            # key = int(do[2])
            key = do[2]
            if key not in g:
                g.add_vertex(key)
            else:
                print('Vertex already exists.')
        elif suboperation == 'edge':
            src = do[2]
            dest = do[3]
            if src not in g:
                print('Vertex {} does not exist.'.format(src))
            elif dest not in g:
                print('Vertex {} does not exist.'.format(dest))
            else:
                if not g.does_edge_exist(src, dest):
                    out.append([(src, dest)])
                    g.add_edge(src, dest)
                    b_s = True
                else:
                    print('Edge already exists.')

    elif operation == 'topological':
        tlist = get_topological_sorting(g)
        if tlist is not None:
            print("INPUT : ", out)
            print('Topological Sorting: ', end='')
            next_out = tlist
            a_s = True
            print(tlist)
        else:
            print('Graph is not a DAG.')

    elif operation == 'display':
        print('Vertices: ', end='')
        for v in g:
            print(v.get_key(), end=' ')
        print()

        print('Edges: ')
        for v in g:
            for dest in v.get_neighbours():
                w = v.get_weight(dest)
                print('(src={}, dest={}, weight={}) '.format(v.get_key(),
                                                             dest.get_key(), w))
        print()
    elif operation == 'before_sort':
        if b_s:
            G = DiGraph()
            anime(G, out, "BEFORE SORTING TOPOLOGICALLY USING DFS")
        else:
            print("\n!!!Add Edges First!!!\n")
    elif operation == 'after_sort':
        if a_s:
            visited = []
            redundanti = []
            redundantj = []
            for i in range(len(next_out)):
                for j in range(i, len(next_out)):
                    if [(next_out[i], next_out[j])] in out and [(next_out[i], next_out[j])] not in visited and (
                            next_out[i] not in redundanti or next_out[j] not in redundantj):
                        visited.append([(next_out[i], next_out[j])])
                        redundanti.append(next_out[i])
                        redundantj.append(next_out[j])
                        i = j
        # print(visited)
            x = DiGraph()
            anime(x, visited, "AFTER SORTING TOPOLOGICALLY USING DFS")
        else:
            print("\n!!!Calculate \"topological\" First!!!\n")
    elif operation == 'quit':
        break
