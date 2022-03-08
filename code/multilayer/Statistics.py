#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 18:09:56 2021

@author: jcasasr
"""

from scipy import stats
import numpy as np
import math
import matplotlib.pyplot as plt


def compute_ttest(fs, values, metric, idx_controls, idx_patients, region_name, labels=None):
    # vars
    threshold_1 = 0.05
    threshold_2 = 0.01
    threshold_3 = 0.001
    num_1 = 0
    num_2 = 0
    num_3 = 0
    name_cols = ('node', 't-statistic', 'p-value', 'controls_mean', 'controls_std', 'controls_n', 'controls_ci'
        , 'patients_mean', 'patients_std', 'patients_n', 'patients_ci')
    num_cols = len(name_cols)
    
    results = np.zeros((len(region_name), num_cols), dtype=float)
    
    fs.info("")
    fs.info("[{:25s}] Computing statistics...".format(metric))

    for node in range(len(region_name)):
        # T-test
        (t, p) = stats.ttest_ind(values[idx_controls, node], values[idx_patients, node])
        controls_mean = np.mean(values[idx_controls, node])
        controls_std = np.std(values[idx_controls, node])
        controls_n = len(values[idx_controls, node])
        controls_ci = 1.96 * controls_std / math.sqrt(controls_n)
        patients_mean = np.mean(values[idx_patients, node])
        patients_std = np.std(values[idx_patients, node])
        patients_n = len(values[idx_patients, node])
        patients_ci = 1.96 * patients_std / math.sqrt(patients_n)
        
        # figure title
        str_title = "Node "+ str(node+1) +" - "+ region_name[node] +" (p="+ str(round(p, 4)) +")"

        # boxplot
        data = [values[idx_controls, node], values[idx_patients, node]]
        plt.boxplot(data, labels=labels)
        plt.title(str_title)
        plt.ylabel(metric)
        plt.savefig(fs.get_figs_all_folder() + metric +"_"+ str(node+1) +"_boxplot.png")
        if(p <= threshold_1):
            plt.savefig(fs.get_figs_selected_folder() + metric +"_"+ str(node+1) +"_boxplot.png")
        plt.close()

        # CI plot
        x = (0,1)
        plt.plot(x, (controls_mean, patients_mean))
        plt.fill_between(x, (controls_mean - controls_ci, patients_mean - patients_ci), (controls_mean + controls_ci, patients_mean + patients_ci)
            , color='b', alpha=.1)
        plt.title(str_title)
        plt.xticks(x, labels, rotation=0)  # Set text labels and properties.
        plt.ylabel(metric)
        plt.grid(axis='y', color='grey', linestyle='dotted', linewidth=0.5)
        plt.savefig(fs.get_figs_all_folder() + metric +"_"+ str(node+1) +"_ci.png")
        if(p <= threshold_1):
            plt.savefig(fs.get_figs_selected_folder() + metric +"_"+ str(node+1) +"_ci.png")
        plt.close()

        # report nodes with significance
        if(p <= threshold_1):
            fs.info("Node {} \t t-statistic is {:.4f} and p-value is {:.4f}".format(node+1, t, p))
            num_1 += 1

            # check 99% CI
            if(p <= threshold_2):
                num_2 += 1
            
            # check 99.9% CI
            if(p <= threshold_3):
                num_3 += 1
        
        # save 
        results[node,:] = (node+1, t, p, controls_mean, controls_std, controls_n, controls_ci, patients_mean, patients_std, patients_n, patients_ci)
    
    fs.info("Number of values with p<{:.3f} is: {}".format(threshold_1, num_1))
    fs.info("Number of values with p<{:.3f} is: {}".format(threshold_2, num_2))
    fs.info("Number of values with p<{:.3f} is: {}".format(threshold_3, num_3))

    print("    [{:25s}] Number of values with p<{:.3f} is: {}".format(metric, threshold_1, num_1))
    
    # export
    np.savetxt(fs.get_stats_folder() + metric +"-stats.csv", results, delimiter=",", header=','.join(name_cols), fmt='%1.8f')


def plot_metric_mean_values(fs, values, metric, idx_controls, idx_patients, region_name, labels=None):
    # vars
    num_nodes = values.shape[1]
    x = np.arange(start=1, stop=(num_nodes+1))
    y_controls = np.mean(values[idx_controls,:], axis=0)
    e_controls = np.std(values[idx_controls,:], axis=0)
    y_patients = np.mean(values[idx_patients,:], axis=0)
    e_patients = np.std(values[idx_patients,:], axis=0)

    # plot
    plt.figure(figsize=(14,7))
    plt.errorbar(x, y_patients, e_patients, linestyle='None', fmt='s', color='r', ecolor='r', capthick=2, capsize=2, alpha=1.0, label=labels[1])
    plt.errorbar(x, y_controls, e_controls, linestyle='None', fmt='o', color='g', ecolor='g', capthick=2, capsize=2, alpha=0.5, label=labels[0])
    plt.title(metric)
    plt.xlabel("Nodes")
    plt.ylabel("Mean and STD values")
    plt.legend()

    plt.savefig(fs.get_tmp_folder() + metric +"_mean_std.png")
    plt.close()