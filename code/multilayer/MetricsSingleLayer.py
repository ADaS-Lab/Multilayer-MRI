#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:42:11 2021

@author: jcasasr
"""
import networkx as nx
import numpy as np
import multilayer.Metrics as Metrics
import multilayer.Functions as Functions


def get_metric_values(fs, em, clinic, METRIC=None):
    num_subjs = em.shape[0]
    num_nodes = 76
    
    fs.info("Computing values for metric '{}'...".format(METRIC))

    values = np.zeros((num_subjs, num_nodes), dtype=float)
    
    for i in range(num_subjs):
        fs.debug("Processing subject {}...".format(i))
        
        # data 
        A = em[i,:,:]

        # create graph
        G = Functions.create_graph_from_AM(fs, A)

        # compute metric values
        try:
            if METRIC=='Degree':
                temp = np.array(list(nx.degree_centrality(G).values()))

            elif METRIC=='Strength':
                temp = np.sum(A, axis=0)

            elif METRIC=='Clustering':
                temp = np.array(list(nx.clustering(G, weight='weight').values()))

            elif METRIC=='BetweennessCentrality':
                # Use 'distance'
                G = Functions.create_distance_graph_from_AM(fs, A)

                # debug only
                Functions.report_graph_basics(fs, G)

                temp = np.array(list(nx.betweenness_centrality(G, k=None, normalized=True, weight='weight').values()))

            elif METRIC=='ClosenessCentrality':
                # Use 'distance'
                G = Functions.create_distance_graph_from_AM(fs, A)

                temp = np.array(list(nx.closeness_centrality(G, distance='weight').values()))

            elif METRIC=='EigenvectorCentrality':
                temp = np.array(list(nx.eigenvector_centrality(G, max_iter=100, tol=1e-06, weight='weight').values()))

            elif METRIC=='PageRank':
                temp = np.array(list(nx.pagerank(G, max_iter=1000, weight='weight').values()))

            elif METRIC=='LocalEfficiency':
                # Use 'distance'
                G = Functions.create_distance_graph_from_AM(fs, A)

                # Implementation of LE on single layer networks
                temp = Metrics.compute_LE_SL(fs, G)
            
            else:
                raise Exception("ERROR: Incorrect metric value! (METRIC is {})".format(METRIC))
        except Exception as e:
                fs.error(e)
                return None
    
        values[i,:] = temp

    # export
    np.savetxt(fs.get_metrics_folder() + METRIC +"-values.csv", values, delimiter=",", fmt='%1.8f')

    return(values)
