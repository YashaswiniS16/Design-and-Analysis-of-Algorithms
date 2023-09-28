import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict


def anime(graph, edge_first, removal):
    fig.text(0.02, 0.95, "TOPOLOGICAL ORDER = []")
    graph.add_edges_from(edge_first)
    nx.draw(graph, with_labels=True)
    plt.show(block=False)
    plt.pause(6)
    plt.clf()
    for i in removal:
        # text.set_text("topological order = "+i+" ")
        text.append(i)
        fig.text(0.02, 0.95, "TOPOLOGICAL ORDER = [" + ' '.join(text) + "]")
        graph.remove_node(i)
        nx.draw(graph, with_labels=True)
        plt.show(block=False)
        if removal.index(i) < len(removal) - 1:
            plt.pause(3)
            plt.clf()
        else:
            plt.pause(5)
            plt.close()


def topsort(g, vtx):
    degree = [0] * vtx
    for node in g:
        for adjnode in g[node]:
            degree[adjnode] += 1

    bfs = [i for i in range(vtx) if degree[i] == 0]
    for node in bfs:
        for adjnode in g[node]:
            degree[adjnode] -= 1
            if degree[adjnode] == 0:
                bfs.append(adjnode)
    return bfs


g = defaultdict(list)
G = nx.DiGraph()
fig = plt.figure(figsize=(10, 6))
fig.canvas.manager.set_window_title("TOPOLOGICAL SORTING USING SOURCE REMOVAL")
text = []
# vtx, e = map(int, input().split())
while True:
    try:
        vtx = int(input("Enter number of vertices:"))
    except Exception as e:
        print("\nEnter only integer values\n")
    else:
        break
while True:
    try:
        edges = int(input("Enter number of edges:"))
    except Exception as e:
        print("\nEnter only integer values\n")
    else:
        break
out = []
for i in range(edges):
    print("Enter source and destination for edge no ",(i+1)," in format <src> <dest>")
    u, v = map(str, input().split())
    out.append((u, v))
    u = ord(u) - ord('A')
    v = ord(v) - ord('A')
    g[u].append(v)
topSort = topsort(g, vtx)
topSort = [chr(i + 65) for i in topSort]
anime(G, out, topSort)
print("Topological Order after sorting using Source removal method:\n", topSort)
