#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:42:11 2021

@author: jcasasr
"""
import networkx as nx
import numpy as np
import sys


def compute_CC_ML(fs, G):
    """
    Compute the closeness centrality (CC) in multilayer networks

    PARAMETERS
    ----------

    G: Networkx graph
        Adjancency matrix of minum distances between nodes (76x76)
    """
    num_nodes = G.number_of_nodes()
    nodes = list(G.nodes())

    # array to store the scores
    values = np.zeros(num_nodes, dtype=float)

    # compute SP for all nodes
    sp = dict(nx.all_pairs_dijkstra_path_length(G, weight='weight'))
    
    # for each node, compute the CC
    # CC(x) = (N-1) / (Sum_y d(x,y))
    for node in nodes:
        values[node] = (num_nodes-1) / sum(sp[node].values())

    return values


def compute_LE_SL(fs, G):
    """
    Local Efficiency (LE) for single layer networks   

    PARAMETERS
    ----------

    G: Networkx graph
        Adjancency matrix of minum distances between nodes (76x76) 
    """
    num_nodes = G.number_of_nodes()

    # array to store the scores
    values = np.zeros(num_nodes, dtype=float)

    # for each node in G
    for node in list(G.nodes):
        # get the ego network
        subG = nx.ego_graph(G, n=node, radius=1, center=False, undirected=True)
        fs.debug("Creating subgraph of 1-neighbourhood of node {}... [n={} and e={}]".format(node, subG.number_of_nodes(), subG.number_of_edges()))

        # node efficiency
        eff_node = 0

        # check if subgraph is not null
        if subG.number_of_nodes() > 1:
            # check if it is connected
            if not nx.is_connected(subG):
                fs.info("   Subgraph is not connected: extracting the largest component...")
                subG = subG.subgraph(max(nx.connected_components(subG), key=len))
                fs.info("   New subgraph of node {} has n={} and e={}".format(node, subG.number_of_nodes(), subG.number_of_edges()))

            # compute SP for all nodes in ego network
            sp = dict(nx.all_pairs_dijkstra_path_length(subG, weight='weight'))
            subnodes = list(subG.nodes())
            num_subnodes = subG.number_of_nodes()

            for node_source in subnodes:
                for node_target in subnodes:
                    if(node_source != node_target):
                        eff_node = eff_node + (1 / sp[node_source][node_target])
            
            eff_node = eff_node / (num_subnodes * (num_subnodes - 1))
        
        # store node efficiency
        values[node] = eff_node

    return values
