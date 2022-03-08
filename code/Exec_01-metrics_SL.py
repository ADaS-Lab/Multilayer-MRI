#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 15:47:17 2021

@author: jcasasr
"""
from multilayer.FileSystem import FileSystem
from multilayer.Config import Config

import multilayer.LoadData as LoadData
import multilayer.MetricsSingleLayer as MetricsSingleLayer
import logging
import sys

## Debugging
# logging.INFO 
# logging.DEBUG
logging_level = logging.INFO


def main(ini_file):
    # Load configuration file
    conf = Config(ini_file)
    # Create folders and logging system
    fs = FileSystem(logging_level, "log_compute"
        , str_name=conf.get('GENERAL', 'name')
        , str_path_exp=conf.get('GENERAL', 'PATH_EXPS')
        , b_create_dirs=True)
    # Log basic info
    conf.info(fs)
    
    # Load clinical data
    (clinic, _) = LoadData.get_clinic_data(fs, path=conf.get('GENERAL', 'PATH_DATA'))
        
    # Load data
    str_type = conf.get('GENERAL', 'TYPE')

    if not str_type == 'SL':
        fs.error("TYPE unknown! (value is {})".format(str_type))
        sys.exit()

    # Load matrices data
    Ms = LoadData.get_matrix_data(fs, conf.get('SINGLELAYER', 'MATRIX'), path=conf.get('GENERAL', 'PATH_DATA'))

    # Export matrices
    LoadData.export_matrix_csv(fs, Ms)

    # compute graph metrics
    lst_metrics = conf.get_list('GENERAL', 'METRICS_COMPUTE')
    for METRIC in lst_metrics:
        # Compute metric
        MetricsSingleLayer.get_metric_values(fs, Ms, clinic, METRIC=METRIC)
    
    # close
    fs.info("Process finished successfully!")
    fs.close()
    print("    Process finished successfully!")


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("ERROR: Please, specifiy the INI file!")
    else:
        main(sys.argv[1])