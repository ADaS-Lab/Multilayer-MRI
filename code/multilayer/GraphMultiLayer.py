#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 17:42:11 2021

@author: jcasasr
"""
import numpy as np
import matplotlib.pyplot as plt
import random
import math
import sys


def preproc_exp(m):
    num_subjs = m.shape[0]
    num_x1 = m.shape[1]
    num_x2 = m.shape[2]

    for s in range(num_subjs):
        for x1 in range(num_x1):
            for x2 in range(num_x2):
                m[s,x1,x2] = math.exp(m[s,x1,x2])

    return m


def preproc_norm(x):
    return (x+1)/2


def preproc_diag(m):
    num_nodes = m.shape[1]

    for i in range(num_nodes):
        m[:,i,i] = 1

    return m


def create_multilayer(fs, FA, RS, GM, INTERLINK=None, FA_diag=True, FA_exp=False, RS_neg=False, RS_exp=False, GM_neg=False, GM_exp=False):
    num_subjs = FA.shape[0]
    num_nodes = FA.shape[1]
    
    # data structure
    em = np.zeros((num_subjs, num_nodes*2, num_nodes*2), dtype=float)

    ### data preprocessing
    # invert RS
    if RS_neg:
        RS = -RS
        fs.info("RS matrix: INV() selected!")
    
    if GM_neg:
        GM = -GM
        fs.info("GM matrix: INV() selected!")

    # apply EXP() 
    if RS_exp:
        RS = preproc_exp(RS)
        fs.info("RS matrix: EXP() selected!")

    if FA_exp:
        FA = preproc_exp(FA)
        fs.info("FA matrix: EXP() selected!")
    
    if GM_exp:
        GM = preproc_exp(GM)
        fs.info("GM matrix: EXP() selected!")

    # FA diagonal = 1
    # transfer between each node in the different layers has cost=1
    if FA_diag:
        FA = preproc_diag(FA)
        fs.info("FA matrix: DIAG=1 selected!")

    ### create multilayer
    if INTERLINK=='FA':
        fs.info("Interlink type is FA!")

        for i in range(num_subjs):
            em[i,:76,:76] = RS[i,:,:]
            em[i,76:,76:] = GM[i,:,:]
            em[i,76:,:76] = FA[i,:,:]
            em[i,:76,76:] = FA[i,:,:]
        
    elif INTERLINK=='RS':
        fs.info("Interlink type is RS!")

        for i in range(num_subjs):
            em[i,:76,:76] = FA[i,:,:]
            em[i,76:,76:] = GM[i,:,:]
            em[i,76:,:76] = RS[i,:,:]
            em[i,:76,76:] = RS[i,:,:]
    
    elif INTERLINK=='GM':
        fs.info("Interlink type is GM!")

        for i in range(num_subjs):
            em[i,:76,:76] = FA[i,:,:]
            em[i,76:,76:] = RS[i,:,:]
            em[i,76:,:76] = GM[i,:,:]
            em[i,:76,76:] = GM[i,:,:]

    else:
        fs.error("ERROR:: Incorrect value! (INTERLINK is {})".format(INTERLINK))
        sys.exit()
        
    fs.info("Multilayer network shape is {}".format(em.shape))

    return(em)


def plot_ml_matrices(fs, em):
    num_subjs = em.shape[0]

    # plot
    n_rows = 1
    n_cols = 4
    _, axs = plt.subplots(n_rows, n_cols, figsize=(4*n_cols, 4*n_rows))

    # data sample
    individuals = random.sample(range(num_subjs), 4)

    for i, ind in enumerate(individuals):
        axs[i].imshow(em[ind,:,:], cmap='hot', interpolation='nearest')
        axs[i].set_title("Subject {}".format(ind))

    plt.savefig(fs.get_tmp_folder() + "MultiLayer_test.png")
    plt.close()


def plot_ml_matrix(fs, A, ind):
    plt.imshow(A, origin='lower', cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.title("Subject {}".format(ind))

    plt.savefig(fs.get_tmp_folder() + "MultiLayer_test_subj_"+ str(ind) +".png")
    plt.close()