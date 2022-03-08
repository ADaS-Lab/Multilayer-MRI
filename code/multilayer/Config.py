#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 13:12:20 2021

@author: jcasasr
"""

import configparser
import ast

class Config:
    def __init__(self, fin):
        self.config = configparser.ConfigParser()
        self.config.read(fin)
    

    def info(self, fs):
        fs.info("**** CONFIGURATION PARAMETERS *****")
        for conf in self.config.sections():
            fs.info("+++ Section [{}]".format(conf))
            for key in self.config[conf]:  
                fs.info("    {} = {}".format(key, self.config.get(conf, key)))
        
        fs.info("***********************************")

    
    def get(self, section, key):
        return self.config.get(section, key)

    
    def get_int(self, section, key):
        return self.config.getint(section, key)


    def get_boolean(self, section, key):
        return self.config.getboolean(section, key)

    def get_list(self, section, key):
        return ast.literal_eval(self.config.get(section, key))