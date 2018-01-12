# !/usr/bin/env python
import os.path
import sys
import networkx as nx
import pylab
import numpy as np

import parse_dependency

def pom_visitor(poms, dirname, names):
    if 'pom.xml' in names:
        pom = '%s/pom.xml' % dirname
        poms.append(parse_dependency.parse(pom))

def dependency_edges(pom, group = None):
    if group is None:
        group_filter = lambda d: True
    else:
        group_filter = lambda d: d.groupId.startswith(group)
    edges = set()
    for dependency in filter(group_filter, pom['dependencies']):
        edges.add((pom['artifact'].artifactId, dependency.artifactId))
    return edges

def print_edge(edges):
    sorted(edges)
    print 'digraph dependencies {'
    for edge in edges:
        a, b = edge
        print ' "%s" ----> "%s";' %(a, b)
    print '}'

def draw_graph(edges):
    G = nx.Graph()
    G = nx.DiGraph()
    from_array = np.array([])
    to_array = np.array([])
    from_list = list(from_array)
    to_list = list(to_array)
    for edge in edges:
        from_node, to_node = edge
        G.add_edge(from_node, to_node)
    pos = nx.shell_layout(G)
    nx.draw(G,pos,with_labels=True,node_color='white',edge_color='red',
            node_size=400, alpha=0.5)
    pylab.title('Self_define net', fontsize=15)
    pylab.show()


if __name__ == '__main__':
    directory = sys.argv[1]
    group = sys.argv[2]
    poms = []
    os.path.walk(directory, pom_visitor, poms)
    edges = set()
    for pom in poms:
        edges = edges | dependency_edges(pom,group)
    print_edge(edges)
    draw_graph(edges)


