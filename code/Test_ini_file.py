#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 15:47:17 2021

@author: jcasasr
"""
import configparser

config = configparser.ConfigParser()
config.read('Test.ini')

for conf in config.sections():
    print("*** Section [{}]".format(conf))
    for key in config[conf]:  
        print("{} = {}".format(key, config.get(conf, key)))