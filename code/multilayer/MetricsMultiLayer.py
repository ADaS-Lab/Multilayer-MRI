#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:42:11 2021

@author: jcasasr
"""
import networkx as nx
import numpy as np
import sys
from multilayer.GraphMultiLayer import plot_ml_matrix
import multilayer.Metrics as Metrics
import multilayer.Functions as Functions


def get_metric_values(fs, em, clinic, METRIC=None):
    num_subjs = em.shape[0]
    num_nodes = 76
    file_metric = fs.get_metrics_folder() + METRIC +"-values.csv"
    
    # check if metric is computed and stored previously 
    if fs.file_exists(file_metric):
        fs.info("Metric '{}' was previously computed and stored... ".format(METRIC))
        return None
    else:
        fs.info("Computing values for metric '{}'...".format(METRIC))

    values = np.zeros((num_subjs, num_nodes), dtype=float)
    
    for i in range(num_subjs):
        fs.debug("Processing subject {}...".format(i))
        
        # get data 
        A = em[i,:,:]
        bool_reshape = True
        
        # compute the specific metric
        try:
            if METRIC=='Degree':
                temp = np.count_nonzero(A > 0, axis=0)

            elif METRIC=='Strength':
                temp = np.sum(A, axis=0)

            elif METRIC=='LocalEfficiency':
                fs.info("Processing subject {}...".format(i))
                # Use 'distance'
                A_inv = Functions.create_distance_A_from_A(fs, A)

                # debug only
                #plot_ml_matrix(fs, A, i)

                # Compute A min
                A_min = Functions.compute_A_min(fs, A_inv)

                # create G
                G = Functions.create_graph_from_AM(fs, A_min)

                # compute LE as a single layer
                temp = Metrics.compute_LE_SL(fs, G)

                # Do not reshape 
                bool_reshape = False

            elif METRIC=='ClosenessCentrality':
                fs.info("Processing subject {}...".format(i))
                # Use 'distance'
                A_inv = Functions.create_distance_A_from_A(fs, A)

                # debug only
                #plot_ml_matrix(fs, A, i)

                # Compute A min
                A_min = Functions.compute_A_min(fs, A_inv)

                # create G
                G = Functions.create_graph_from_AM(fs, A_min)

                # compute LE as a single layer
                temp = np.array(list(nx.closeness_centrality(G, distance='weight').values()))
                
                # Do not reshape 
                bool_reshape = False

            elif METRIC=='BetweennessCentrality':
                fs.info("Processing subject {}...".format(i))
                # Use 'distance'
                A_inv = Functions.create_distance_A_from_A(fs, A)

                # debug only
                #plot_ml_matrix(fs, A, i)

                # Compute A min
                A_min = Functions.compute_A_min(fs, A_inv)

                # create G
                G = Functions.create_graph_from_AM(fs, A_min)

                # compute LE as a single layer
                temp = np.array(list(nx.betweenness_centrality(G, k=None, normalized=True, weight='weight').values()))
                
                # Do not reshape 
                bool_reshape = False
            
            else:
                raise Exception("ERROR: Incorrect metric value! (METRIC is {})".format(METRIC))
        except Exception as e:
                fs.error(e)
                return None
    
        # Interlink
        # interlink: folding results to get 76 nodes (instead of 152)
        if bool_reshape:
            temp2 = temp.reshape((76,2), order='F')
            # sum values
            temp3 = np.sum(temp2, axis=1)
        else:
            temp3 = temp
            
        # store the results for each node
        values[i,:] = temp3
        
    # export
    np.savetxt(file_metric, values, delimiter=",", fmt='%1.8f')

    return(values)
