#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Assignment 2: Recomputing the minimum spanning tree

Team Number: 
Student Names: 
'''
import unittest
import networkx as nx

"""IMPORTANT:
We're using networkx only to provide a reliable graph
object.  Your solution may NOT rely on the networkx implementation of
any graph algorithms.  You can use the node/edge creation functions to
create test data, and you can access node lists, edge lists, adjacency
lists, etc. DO NOT turn in a solution that uses a networkx
implementation of a graph traversal algorithm, as doing so will result
in a score of 0.
"""
try:
    import matplotlib.pyplot as plt

    have_plt = True
except:
    have_plt = False


def update_MST_1(G, T, e, w):
    """
    Sig: graph G(V,E), graph T(V, E), edge e, int ==> 
    Pre: T is a MST of graph G, its edge e is updated and will have a weight w
         e is not in E(T) and its new weight is bigger than the old one
    Post: T is still a MST of G, G contains the updated edge
    Example: TestCase 1
    """
    (u, v) = e
    assert (e in G.edges() and e not in T.edges() and w > G[u][v]['weight'])


def update_MST_2(G, T, e, w):
    """
    Sig: graph G(V,E), graph T(V, E), edge e, int ==> 
    Pre: T is a MST of graph G, its edge e is updated and will have a weight w
         e is not in E(T) and its new weight is smaller than the old one
    Post: T is still a MST of G, G contains the updated edge
    Example: TestCase 2
    """
    (u, v) = e
    assert (e in G.edges() and e not in T.edges() and w < G[u][v]['weight'])
    # update the edge of graph G to hold a new value
    G.remove_edge(u, v)
    G.add_edge(u, v, weight=w)

    # Firstly we add the edge with decreased weight to the MST. Doing that we create
    # a cycle in the tree. We therefore have to remove/break this cycle by removing
    # an edge with the biggest weight
    T.add_edge(u, v, weight=w)
    cycle = find_cycle_path(T, u, u, [])

    edge_to_remove = None
    max_weight = 0
    # Invariant : max_weight is the biggest weight among first i edges of the cycle
    #             edge_to_remove is the corresponding edge
    # Variant   : i
    for i in range(len(cycle)):
        vertex_from = cycle[i]
        vertex_to = cycle[i + 1] if i + 1 < len(cycle) else cycle[i + 1 - len(cycle)]

        if G[vertex_from][vertex_to]['weight'] > max_weight:
            max_weight = G[vertex_from][vertex_to]['weight']
            edge_to_remove = (vertex_from, vertex_to)

    T.remove_edge(edge_to_remove[0], edge_to_remove[1])


def find_cycle_path(T, start, vertex, visited_edges):
    """
    Given a 'vertex', this function explores paths through its children
    on the pursue for the path back to 'start' node indicating a cycle

    Sig: graph T(V,E), vertex, edge[] ==> vertex[]
    Pre: 'start' vertex is the start and the end of the cycle), current vertex
         'vertex' and the list of already visited edges
    Post: return list contains vertices forming a cycle in the 'MST'
    """
    # Invariant : 'visited_edges' contains edges traversed by this function so far
    #             'path' is either empty, meaning the path through 'child' does not
    #             contain a cycle or is populated, containing sub-graph of the cycle
    # Variant   : 'child' child vertex of the current one being explored
    for child in T[vertex]:
        extend_edge = (vertex, child)
        # reversed edge added since the graph is non-directional
        rev_extend_edge = (child, vertex)

        # Following lines are executed only for non-visited edges
        if not visited_edges.__contains__(extend_edge):
            # Check whether we reached the start (aka completed the loop)
            if child == start:
                return [vertex]
            # If not, add the edges (u,v) and (v,u), which are considered the same
            # to the visited list a proceed to evaluate the current child vertex
            visited_edges.append(extend_edge)
            visited_edges.append(rev_extend_edge)

            path = find_cycle_path(T, start, child, visited_edges)
            # If the recursive function return a non-empty list, we found a sub-path
            # of the cycle. Append the current vertex and return
            if len(path) != 0:
                path.append(vertex)
                return path

    return []


def update_MST_3(G, T, e, w):
    """
    Sig: graph G(V,E), graph T(V, E), edge e, int ==> 
    Pre: T is a MST of graph G, its edge e is updated and will have a weight w
         e is in E(T) and its new weight is smaller than the old one
    Post: T is still a MST of G, G contains the updated edge
    Example: TestCase 3
    """
    (u, v) = e
    assert (e in G.edges() and e in T.edges() and w < G[u][v]['weight'])


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


def update_MST_4(G, T, e, w):
    """
    Sig: graph G(V,E), graph T(V, E), edge e, int ==> 
    Pre: T is a MST of graph G, its edge e is updated and will have a weight w
         e is in E(T) and its new weight is bigger than the old one
    Post: T is still a MST of G, G contains the updated edge
    Example: TestCase 4
    """
    (u, v) = e
    assert (e in G.edges() and e in T.edges() and w > G[u][v]['weight'])
    # update the edge of graph G to hold a new value
    G.remove_edge(u, v)
    G.add_edge(u, v, weight=w)
    # Remove the increased edge from the MST and find a replacement (it can be
    # the same one). By removing the edge we divided the MST into two disjoint
    # sets of vertices/sub-graphs. We then need to find the minimal edge
    # connecting those components
    T.remove_edge(u, v)

    comp1 = get_conn_component(T, u)
    comp2 = get_conn_component(T, v)

    min_weight = float("inf")
    min_edge = None

    # Invariant : min_weight is the minimal weight among all bridge edges
    #             explored so far. Bridge edge is the edge connecting
    #             components 'comp1' and 'comp2'
    #             min_edge is the corresponding bridging edge
    # Variant   : current edge being evaluated
    for edge in G.edges():
        (v1, v2) = edge

        if (comp1.__contains__(v1) and comp2.__contains__(v2)) \
                or (comp1.__contains__(v2) and comp2.__contains__(v1)):

            bridge_weight = G[v1][v2]['weight']
            if bridge_weight < min_weight:
                min_weight = bridge_weight
                min_edge = edge

    T.add_edge(min_edge[0], min_edge[1])


class RecomputeMstTest(unittest.TestCase):
    """Test Suite for minimum spanning tree problem
    
    Any method named "test_something" will be run when this file is 
    executed. Use the sanity check as a template for adding your own 
    test cases if you wish.
    (You may delete this class from your submitted solution.)
    """

    def create_graph(self):
        G = nx.Graph()
        G.add_edge('a', 'b', weight=0.6)
        G.add_edge('a', 'c', weight=0.2)
        G.add_edge('c', 'd', weight=0.1)
        G.add_edge('c', 'e', weight=0.7)
        G.add_edge('c', 'f', weight=0.9)
        G.add_edge('a', 'd', weight=0.3)
        return G

    def draw_mst(self, G, T, n):
        if not have_plt:
            return
        pos = nx.spring_layout(G)  # positions for all nodes
        plt.subplot(220 + n)
        plt.title('updated MST %d' % n)
        plt.axis('off')
        # nodes
        nx.draw_networkx_nodes(G, pos, node_size=700)
        # edges
        nx.draw_networkx_edges(G, pos, width=6, alpha=0.5,
                               edge_color='b', style='dashed')
        nx.draw_networkx_edges(T, pos, width=6)
        # labels
        nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

    def test_mst1(self):
        """Sanity Test
        
        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """
        # TestCase 1: e in G.edges() and not e in T.edges() and 
        #             w > G[u][v]['weight']
        G = self.create_graph()
        T = nx.minimum_spanning_tree(G)
        update_MST_1(G, T, ('a', 'd'), 0.5)
        self.draw_mst(G, T, 1)
        self.assertItemsEqual(
            T.edges(),
            [('a', 'b'), ('a', 'c'), ('c', 'd'), ('c', 'e'), ('c', 'f')]
        )

    def test_mst2(self):
        # TestCase 2: e in G.edges() and not e in T.edges() and 
        #             w < G[u][v]['weight']
        G = nx.complete_graph(6);

        G[0][1]['weight'] = 115;
        G[0][2]['weight'] = 121;
        G[0][3]['weight'] = 49;
        G[0][4]['weight'] = 55;
        G[0][5]['weight'] = 87;
        G[1][2]['weight'] = 77;
        G[1][3]['weight'] = 16;
        G[1][4]['weight'] = 21;
        G[1][5]['weight'] = 81;
        G[2][3]['weight'] = 61;
        G[2][4]['weight'] = 74;
        G[2][5]['weight'] = 124;
        G[3][4]['weight'] = 129;
        G[3][5]['weight'] = 9;
        G[4][5]['weight'] = 34;

        T = nx.minimum_spanning_tree(G)
        update_MST_2(G, T, (0, 5), 52)

        self.draw_mst(G, T, 2)

        weight = 0
        for u, v in T.edges():
            weight += G[u][v]['weight']

        self.assertEqual(weight, 156)

    def test_mst3(self):
        # TestCase 3: e in G.edges() and e in T.edges() and 
        #             w < G[u][v]['weight']
        G = self.create_graph()
        T = nx.minimum_spanning_tree(G)
        update_MST_3(G, T, ('a', 'c'), 0.1)
        self.draw_mst(G, T, 3)
        self.assertItemsEqual(
            T.edges(),
            [('a', 'b'), ('a', 'c'), ('c', 'd'), ('c', 'e'), ('c', 'f')]
        )

    def test_mst4(self):
        # TestCase 4: e in G.edges() and e in T.edges() and 
        #             w > G[u][v]['weight']
        G = self.create_graph()
        T = nx.minimum_spanning_tree(G)
        update_MST_4(G, T, ('a', 'c'), 0.4)
        self.draw_mst(G, T, 4)
        self.assertItemsEqual(
            T.edges(),
            [('a', 'b'), ('a', 'd'), ('c', 'd'), ('c', 'e'), ('c', 'f')]
        )

    @classmethod
    def tearDownClass(cls):
        if have_plt:
            plt.show()


if __name__ == '__main__':
    unittest.main()
