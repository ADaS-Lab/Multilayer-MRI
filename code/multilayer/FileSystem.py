#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:12:20 2021

@author: jcasasr
"""

from datetime import datetime
import os
import logging


class FileSystem:
    def __init__(self, logging_level, logging_name, str_name=None, str_path_exp=None, b_create_dirs=False):
        if str_path_exp is None:
            self.base_path = os.getcwd()
        else:
            self.base_path = str_path_exp
        # Constants
        self.CT_FIGS_SELECTED = "figs_selected"
        self.CT_FIGS_ALL = "figs_all"
        self.CT_METRICS = "metrics"
        self.CT_STATS = "statistics"
        self.CT_MATRICES = "matrices"
        self.CT_TMP = "tmp"
        
        if str_name is None or len(str_name) == 0:
            self.folder_name = datetime.now().strftime("%Y%m%d-%H%M%S")
        else:
            self.folder_name = str_name
        
        # create folders
        if b_create_dirs:
            self.create_folder(self.base_path +"/"+ self.folder_name)
            self.create_folder(self.base_path +"/"+ self.folder_name +"/"+ self.CT_FIGS_SELECTED)
            self.create_folder(self.base_path +"/"+ self.folder_name +"/"+ self.CT_FIGS_ALL)
            self.create_folder(self.base_path +"/"+ self.folder_name +"/"+ self.CT_METRICS)
            self.create_folder(self.base_path +"/"+ self.folder_name +"/"+ self.CT_TMP)
            self.create_folder(self.base_path +"/"+ self.folder_name +"/"+ self.CT_STATS)
            self.create_folder(self.base_path +"/"+ self.folder_name +"/"+ self.CT_MATRICES)
        
        # set logging
        self.set_logging(logging_level, logging_name)
        
        print("+++ Starting test '{}'...".format(self.folder_name))
        print("    Execution results stored in {}".format(self.base_path +"/"+ self.folder_name))
        
    
    def set_logging(self, logging_level=logging.DEBUG, logging_name="log"):
        # remove older loggers
        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)

        # Start logging system
        logging.basicConfig(filename=self.get_base_folder() +"/"+ logging_name +".txt", format="%(asctime)s %(levelname)s %(message)s"
                            , filemode='w', level=logging_level)
        logging.getLogger('matplotlib.font_manager').disabled = True
    

    def get_timestamp(self):
        return self.folder_name
    
    
    def get_base_folder(self):
        return self.base_path +"/"+ self.folder_name +"/"
    
    
    def get_figs_selected_folder(self):
        return self.base_path +"/"+ self.folder_name +"/" + self.CT_FIGS_SELECTED +"/"


    def get_figs_all_folder(self):
        return self.base_path +"/"+ self.folder_name +"/" + self.CT_FIGS_ALL +"/"

    
    def get_stats_folder(self):
        return self.base_path +"/"+ self.folder_name +"/" + self.CT_STATS +"/"


    def get_tmp_folder(self):
        return self.base_path +"/"+ self.folder_name +"/" + self.CT_TMP +"/"


    def get_metrics_folder(self):
        return self.base_path +"/"+ self.folder_name +"/" + self.CT_METRICS +"/"

    
    def get_matrices_folder(self):
        return self.base_path +"/"+ self.folder_name +"/" + self.CT_MATRICES +"/"


    def create_folder(self, path):
        try:
            os.mkdir(path)
        except OSError:
            print("Error creating directory {}".format(path))

    
    def file_exists(self, path):
        return os.path.isfile(path)
    
    
    def info(self, message):
        logging.info(message)
        
        
    def debug(self, message):
        logging.debug(message)
        
    
    def error(self, message):
        logging.error(message)
        
        
    def close(self):
        logging.shutdown()
