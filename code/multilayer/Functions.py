#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:42:11 2021

@author: jcasasr
"""
import networkx as nx
import numpy as np
import sys


# Print some basics properties of G
def report_graph_basics(fs, G):
    A = nx.adjacency_matrix(G).todense()
    v_min = np.min(A)
    v_max = np.max(A)
    n_zero = np.count_nonzero(A==0)
    n_non_zero = np.count_nonzero(A)

    fs.debug("   Min={:.2f}, Max={:.2f}, # Zero={}, # Non-Zero={}".format(v_min, v_max, n_zero, n_non_zero))


# Create graph G from adjacency matrix A
def create_graph_from_AM(fs, A):
    # create undirected and weighted graph from adjacency matrix
    G = nx.from_numpy_matrix(A=A, parallel_edges=False)

    return G


# Compute the 1/w to obtain the "distance" between nodes 
# higher values mean shorter distance
def create_distance_A_from_A(fs, A):
    A_inv = np.zeros(A.shape, dtype=float)

    # Compte A=1/w 
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            if not A[i,j] == 0:
                A_inv[i,j] = 1 / A[i,j]

    return A_inv


# some measures, like betweenness and closeness centrality, are based on distance, 
# so we need to compute 1/weights in order to get the shortest paths
def create_distance_graph_from_AM(fs, A):
    # Compte A=1/w 
    A_inv = create_distance_A_from_A(fs, A)

    # create undirected and weighted graph from adjacency matrix
    G = create_graph_from_AM(fs, A_inv)

    return G


def compute_A_min(fs, A):
    """
    Compute the matrix of minimum distances between nodes considering the multilayer network

    Parameters
    ----------
    A : ndarray
        Super-Adjacency matrix (152x152)
    
    Returns
    -------
    ndarray
        Adjacency matrix (76x76)
    """
    # number of nodes in supergraph
    num_nodes_SG = A.shape[0]

    # number of nodes in single graph
    if (num_nodes_SG % 2) == 0:
        num_nodes_G = int(num_nodes_SG / 2)
    else:
        fs.error("The number of nodes in super graph is not EVEN! ({})".format(num_nodes_SG))
        sys.exit(0)

    ###
    # Step 1: create A_min
    # A_min[i,j]: minimum path from i to j through any layer
    A_min = np.zeros((num_nodes_G, num_nodes_G), dtype=float)

    ### DEBUG
    count_min = np.zeros(4, dtype=int)

    # for each node in G (i.e. [1..76])
    for source in range(num_nodes_G):
        for target in range(num_nodes_G):
            # distance value through different layers
            tmp = np.asarray((A[source, target] # source RS --> target RS
                , A[source, (target+num_nodes_G)] # source RS --> target GM (through FA)
                , A[source+num_nodes_G, target] # source GM --> target RS (through FA)
                , A[(source+num_nodes_G), (target+num_nodes_G)])) # source GM --> target GM

            if np.count_nonzero(tmp):
                min_value = np.min(tmp[np.nonzero(tmp)])
                A_min[source, target] = min_value

                ### DEBUG 
                ind = np.where(tmp==min_value)[0][0]
                count_min[ind] = count_min[ind] + 1

            else:
                A_min[source, target] = 0

    ### DEBUG
    count_min_total = np.sum(count_min)
    count_min_rs = count_min[0]
    count_min_fa = count_min[1] + count_min[2] # FA includes: RS -> GM and GM -> RS
    count_min_gm = count_min[3]
    fs.info("RS={} ({:.2f} %), FA={} ({:.2f} %), GM={} ({:.2f} %), Total={}".format(
        count_min_rs, (count_min_rs / count_min_total) * 100
        , count_min_fa, (count_min_fa / count_min_total) * 100
        , count_min_gm, (count_min_gm / count_min_total) * 100
        , count_min_total))

    return A_min
