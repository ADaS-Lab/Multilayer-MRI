#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 16:03:37 2021

@author: jcasasr
"""

import pandas as pd
import numpy as np
import pickle
import os
import csv


# Data labels
CT_CONTROL = -1
CT_RRMS = 0
CT_SPMS = 1
CT_PPMS = 2


def get_clinic_data(fs, path=None):
    # path
    if path is None:
        path = os.getcwd()
    
    # import Pickle object to DF
    clinic = pickle.load(open(path+ "/data/clinic.pkl", "rb"))
    noms_nodes = pickle.load(open(path+ "/data/noms_nodes.pkl", "rb"))
    
    fs.info("'clinic' shape is     {}".format(clinic.shape))
    fs.info("'noms_nodes' shape is {}".format(noms_nodes.shape))
    
    return(clinic, noms_nodes)


def get_matrix_data(fs, matrix, path=None):
    # path
    if path is None:
        path = os.getcwd()
    
    # import values from numpy object
    Ms = np.load(path +"/data/"+ matrix +".npy")
    
    fs.info("Matrix shape is    {}".format(Ms.shape))
    
    return(Ms)


# return indices (IDX) from HV
def get_mstype_idx(mstype, ct_val):
    return list(np.where(np.array(mstype)==ct_val)[0])


def get_patients(fs, PATIENTS_TYPE, clinic):
    idxs_controls = get_mstype_idx(clinic['mstype'], CT_CONTROL)
    idxs_rrms = get_mstype_idx(clinic['mstype'], CT_RRMS)
    idxs_spms = get_mstype_idx(clinic['mstype'], CT_SPMS)
    idxs_ppms = get_mstype_idx(clinic['mstype'], CT_PPMS)
    
    # patients
    if PATIENTS_TYPE==0:
        idxs_pacients = idxs_rrms
    elif PATIENTS_TYPE==1:
        idxs_pacients = np.sort(np.concatenate((np.asarray(idxs_rrms), np.asarray(idxs_spms))))
    elif PATIENTS_TYPE==2:
        idxs_pacients = np.sort(np.concatenate((np.asarray(idxs_rrms), np.asarray(idxs_spms), np.asarray(idxs_ppms))))
    else:
        fs.info("Incorrect value! (PATIENTS_TYPE is {})".format(PATIENTS_TYPE))
    
    fs.info("*** Subjects info...")
    fs.info("Controls [{}] \n{}".format(len(idxs_controls), idxs_controls))
    fs.info("RRMS     [{}] \n{}".format(len(idxs_rrms), idxs_rrms))
    fs.info("SPMS     [{}] \n{}".format(len(idxs_spms), idxs_spms))
    fs.info("PPMS     [{}] \n{}".format(len(idxs_ppms), idxs_ppms))
    fs.info("Patients [{}] \n{}".format(len(idxs_pacients), idxs_pacients))
    
    return(idxs_controls, idxs_pacients)


def export_matrix_csv(fs, Ms):
    num_subjs = Ms.shape[0]
    num_x1 = Ms.shape[1]
    num_x2 = Ms.shape[2]

    # export shape
    arr_info = np.array([num_subjs, num_x1, num_x2], dtype=np.int32)
    np.savetxt(fs.get_matrices_folder() +"info.csv", arr_info, delimiter=",", fmt='%d')

    # export each matrix
    for subj in range(num_subjs):
        np.savetxt(fs.get_matrices_folder() + str(subj) +".csv", Ms[subj,:,:], delimiter=",", fmt='%1.8f')
    
    fs.info("Matrices exported successfully!")


def import_metric_csv(fs, metric):
    ifile = fs.get_metrics_folder() + metric + "-values.csv"

    if os.path.isfile(ifile):
        values = np.genfromtxt(ifile, delimiter=",")
    else:
        fs.error("File '{}' does not exist!".format(ifile))
        values = None

    return(values)


def export_object_from_matrix(fs, values, metric):
    # export object
    np.save(fs.get_metrics_folder() + metric +"-values.npy", values, allow_pickle=True)


def export_df_from_matrix(fs, values, metric, clinic):
    num_nodes = values.shape[1]

    # export to Pandas Dataframe
    df = pd.DataFrame(data=values, columns=range(1, num_nodes+1))
    df.insert(loc=0, column="mstype", value=clinic['mstype'])
    df.insert(loc=0, column="id", value=clinic['id'])
    df.to_csv(fs.get_metrics_folder() + metric +"-values (with Clinic).csv", sep=",", float_format="%1.8f", header=True, index=True)
