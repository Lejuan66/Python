#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 3: Controlling Maximum Flow

Team Number: 
Student Names: 
'''

import unittest
import networkx as nx
# API for networkx flow algorithms changed in v1.9:
if (list(map(lambda x: int(x), nx.__version__.split("."))) < [1, 9]):
    max_flow = nx.ford_fulkerson
else:
    max_flow = nx.maximum_flow
"""
We use max_flow() to generate flows for the included tests,
and you may of course use it as well in any tests you generate.
As always, your implementation of the senstive() function may NOT make use
of max_flow(), or any of the other graph algorithm implementations 
provided by networkx.
"""

# If your solution needs a queue (like the BFS algorithm), you can use this one:
from collections import deque

try:
    import matplotlib.pyplot as plt

    HAVE_PLT = True
except ImportError:
    HAVE_PLT = False

"""
F is represented in python as a dictionary of dictionaries; 
i.e., given two nodes u and v, 
the computed flow from u to v is given by F[u][v].
"""


def sensitive(G, s, t, F):
    """
    Sig:   Graph(V,E), int, int, int matrix [0..|V|-1][0..|V|-1]
               $\longrightarrow$ int, int
    Pre:    G is a flow network, s is the source and t the sink of the network
            F matrix contains flow values for every pair of nodes
    Post:   
    Ex:    sensitive(G,0,5,F) $\longrightarrow$ (1, 3)
    """

    # Obtain a residual network G' of the input flow network G
    G_prime = build_res_network(G, F)
    # Find a S-cut of the G' (= all nodes reachable from s)
    S_cut = get_conn_component(G_prime, s)

    # T-cut is every node, which is not in S-cut. We are interested in
    # edges between those two cuts, because they are the sensitive ones
    # Variant:  edge of G being explored
    # Invariant:    None, the function immediately returns when
    #               conditions are met
    for edge in G.edges():
        (v1, v2) = edge

        if S_cut.__contains__(v1) and not S_cut.__contains__(v2):
            return v1, v2

    return None, None


def build_res_network(G, F):
    """
    Sig:   Graph(V,E),  int matrix [0..|V|-1][0..|V|-1]
               $\longrightarrow$ Graph(V,E)
    Pre:   G is a flow network, F matrix contains flow values for each pair of nodes
    Post:  returns a residual network of G
    """
    # residual network G' is the same as G at the beginning
    G_prime = G.copy()

    # start to alter the edges taking into account the flow (in F)
    # Variant:  edge of G' being explored
    # Invariant:    G' up to 'edge' is a residual network of G
    for edge in G_prime.edges():
        (u, v) = edge
        flow_value = F[u][v]

        if flow_value == 0:
            continue

        # If the flow is non-zero, add a backward edge
        G_prime.add_edge(v, u, capacity=flow_value)
        if G_prime[u][v]["capacity"] == flow_value:
            G_prime.remove_edge(u, v)
        else:
            G_prime[u][v]["capacity"] -= flow_value

    return G_prime


def get_conn_component(T, u):
    """
    Given a graph 'T' and node 'u', function finds a set of vertices forming
    a fully connected component of graph 'T' containing vertex 'u'. DFS

    Sig: graph T(V,E), vertex ==> vertex[]
    Pre: 'start' vertex is the start and the end of the cycle), current vertex
         'vertex' and the list of already visited edges
    Post: returns a list containing vertices forming a connected component of T
          containing given 'u'
    """
    # Holds vertices, which have been already visited so the algorithm won't
    # process them again
    visited = []
    # Holds the frontier of the explored area. Vertices to be visited
    # and expanded are chosen from this list
    frontier = [u]

    # Following code is a basic DFS, which collects all vertices it explored
    # Invariant : Visited list keeps its property defined higher
    # Variant   : Frontier list being reduced by 1 and then expanded by 0...deg(vertex)
    while len(frontier) != 0:
        vertex = frontier.pop()

        # Invariant : Frontier list keeps its property defined higher
        # Variant   : child vertex of the one currently being expanded
        for child in T[vertex]:
            if not visited.__contains__(child) and not frontier.__contains__(child):
                frontier.append(child)
        visited.append(vertex)

    return visited


class SensitiveSanityCheck(unittest.TestCase):
    """
    Test suite for the sensitive edge problem
    """

    def draw_graph(self, H, u, v, flow1, F1, flow2, F2):
        if not HAVE_PLT:
            return
        pos = nx.spring_layout(self.G)
        plt.subplot(1, 2, 1)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_labels(self.G, pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u, v): '{}/{}'.format(
                F1[u][v],
                self.G[u][v]['capacity']
            ) for (u, v, data) in nx.to_edgelist(self.G)})
        plt.title('before: flow={}'.format(flow1))
        plt.subplot(1, 2, 2)
        plt.axis('off')
        nx.draw_networkx_nodes(self.G, pos)
        nx.draw_networkx_edges(self.G, pos)
        nx.draw_networkx_edges(
            self.G, pos,
            edgelist=[(u, v)],
            width=3.0,
            edge_color='b')
        nx.draw_networkx_labels(self.G, pos)
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels={(u, v): '{}/{}'.format(
                F2[u][v], H[u][v]['capacity']
            ) for (u, v, data) in nx.to_edgelist(self.G)})
        plt.title('after: flow={}'.format(flow2))

    def setUp(self):
        """start every test with an empty directed graph"""
        self.G = nx.DiGraph()

    def run_test(self, s, t, draw=False):
        """standard tests to run for all cases
        
        Uses networkx to generate a maximal flow
        """
        H = self.G.copy()
        # compute max flow
        flow_g, F_g = max_flow(self.G, s, t)
        # find a sensitive edge
        u, v = sensitive(self.G, s, t, F_g)
        # is u a node in G?
        self.assertIn(u, self.G, "Invalid edge ({}, {})".format(u, v))
        # is (u,v) an edge in G?
        self.assertIn(v, self.G[u], "Invalid edge ({}, {})".format(u, v))
        # decrease capacity of (u,v) by 1
        H[u][v]["capacity"] = H[u][v]["capacity"] - 1
        # recompute max flow
        flow_h, F_h = max_flow(H, s, t)
        if draw:
            self.draw_graph(H, u, v, flow_g, F_g, flow_h, F_h)
            # is the new max flow lower than the old max flow?
            # self.assertLess(
            #     flow_h,
            #     flow_g,
            #     "Returned non-sensitive edge ({},{})".format(u, v))

    def test_sanity(self):
        """Sanity check"""
        # The attribute on each edge MUST be called "capacity"
        # (otherwise the max flow algorithm in run_test will fail).
        self.G.add_edge(0, 1, capacity=16)
        self.G.add_edge(0, 2, capacity=13)
        self.G.add_edge(2, 1, capacity=4)
        self.G.add_edge(1, 3, capacity=12)
        self.G.add_edge(3, 2, capacity=9)
        self.G.add_edge(2, 4, capacity=14)
        self.G.add_edge(4, 3, capacity=7)
        self.G.add_edge(3, 5, capacity=20)
        self.G.add_edge(4, 5, capacity=4)
        self.run_test(0, 5, draw=True)

    @classmethod
    def tearDownClass(cls):
        if HAVE_PLT:
            plt.show()


if __name__ == "__main__":
    unittest.main()
