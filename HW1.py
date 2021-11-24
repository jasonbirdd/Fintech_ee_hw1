# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 21:19:34 2021

@author: 詹凱錞
"""

import os
import pandas as pd

label = ["date", "time", "price", "volume"]
TX = pd.DataFrame([], columns=label)

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name.endswith(".csv"):
            temp_df = pd.read_csv(os.path.join(root, name), encoding= 'gbk')