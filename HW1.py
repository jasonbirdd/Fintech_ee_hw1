# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 21:19:34 2021

@author: 詹凱錞
"""

import os
import pandas as pd


for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name.endswith(".csv"):
            print(os.path.join(root, name))