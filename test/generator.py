# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 13:16:41 2020

@author: muitanprasert
"""

def post(filename):
    # No pre-conditions
    with open(filename, 'a') as file:
        file.write('test test')