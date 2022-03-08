#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 15:47:17 2021

@author: jcasasr
"""
from multilayer.FileSystem import FileSystem
from multilayer.Config import Config

import multilayer.LoadData as LoadData
import multilayer.Statistics as Statistics
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
    fs = FileSystem(logging_level, "log_stats"
        , str_name=conf.get('GENERAL', 'name')
        , str_path_exp=conf.get('GENERAL', 'PATH_EXPS')
        , b_create_dirs=False)
    # Log basic info
    conf.info(fs)
    
    # Load clinical data
    (clinic, noms_nodes) = LoadData.get_clinic_data(fs, path=conf.get('GENERAL', 'PATH_DATA'))

    # Get HV and MS patients IDs
    (idxs_controls, idxs_pacients) = LoadData.get_patients(fs, conf.get_int('GENERAL', 'PATIENTS_TYPE'), clinic)
        
    # Compute statistics for each metric
    lst_metrics = conf.get_list('GENERAL', 'METRICS_STATS')

    for metric in lst_metrics:
        # Load graph metrics
        values = LoadData.import_metric_csv(fs, metric)

        if (values is not None):
            # Export
            LoadData.export_object_from_matrix(fs, values, metric)
            LoadData.export_df_from_matrix(fs, values, metric, clinic)

            # Plot mean values to check consistency
            Statistics.plot_metric_mean_values(fs, values, metric, idxs_controls, idxs_pacients, noms_nodes['region_name'], labels=['Controls', 'RRMS'])

            # Compute statistics
            if values is not None:
                Statistics.compute_ttest(fs, values, metric, idxs_controls, idxs_pacients, noms_nodes['region_name'], labels=['Controls', 'RRMS'])
    
    # close
    fs.info("Process finished successfully!")
    fs.close()
    print("    Process finished successfully!")


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("ERROR: Please, specifiy the INI file!")
    else:
        main(sys.argv[1])