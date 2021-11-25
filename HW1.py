# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 21:19:34 2021

@author: 詹凱錞
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import math

# In[1]
label = ["date", "time", "price", "volume"]
TX_df = pd.DataFrame([], columns=label)

for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name.endswith(".csv"):
            temp_df = pd.read_csv(os.path.join(root, name), encoding= 'big5')
            temp_df["商品代號"] = temp_df["商品代號"].str.split(" ").str[0].str.strip()
            temp_df["到期月份(週別)"] = temp_df["到期月份(週別)"].str.split(" ").str[0].str.strip()
            temp_extract_df = pd.DataFrame(temp_df[(temp_df["商品代號"] == "TX") & (temp_df["到期月份(週別)"] == "202110")])
            temp_extract_df = pd.concat([temp_extract_df["成交日期"], temp_extract_df["成交時間"], temp_extract_df["成交價格"], temp_extract_df["成交數量(B+S)"]], axis = 1)
            temp_extract_df.columns = label
            TX_df = TX_df.append(temp_extract_df, ignore_index=True)

TX_df.to_csv("./TX.csv")

# In[2]
x_1d = list(set(TX_df["date"].tolist()))
x_1d.sort()
x = [*range(len(x_1d))]

y_VWAP = []
for day in x_1d:
    y_VWAP.append(sum(TX_df[(TX_df["date"]==day)].volume*TX_df[(TX_df["date"]==day)].price)/sum(TX_df[(TX_df["date"]==day)].volume))


plt.figure(figsize = (20, 10))
plt.plot(y_VWAP, label = "time bars")
plt.xticks(x, x_1d, fontsize = 10)
plt.xlabel("date", fontsize = 20)
plt.ylabel("price", fontsize = 20)
plt.legend(fontsize = 20)
plt.show()

# In[3]
ticks_number = 10**4
number_of_bars = math.ceil(len(TX_df)/ticks_number)
x_ticks = [*range(number_of_bars)]
y_ticks_VWAP = []
for ticks in x_ticks:
    y_ticks_VWAP.append(sum(TX_df.volume[ticks*ticks_number:(ticks+1)*ticks_number]*TX_df.price[ticks*ticks_number:(ticks+1)*ticks_number])/sum(TX_df.volume[ticks*ticks_number:(ticks+1)*ticks_number]))  


plt.figure(figsize = (20, 10))
plt.plot(y_ticks_VWAP, label = "ticks bars",c = "red")
plt.xlabel("10k ticks", fontsize = 20)
plt.ylabel("price", fontsize = 20)
plt.legend(fontsize = 20)
plt.show()

# In[4]
volume_number = 10**5
number_of_bars = math.ceil(sum(TX_df.volume)/volume_number)
x_volumes = [*range(number_of_bars)]

y_volumn_VWAP = []
volume_count = 0
price_count = 0
for loc in range(len(TX_df)):
    volume_count += TX_df.iloc[loc].volume
    price_count += TX_df.iloc[loc].volume*TX_df.iloc[loc].price
    if volume_count >= volume_number:
        y_volumn_VWAP.append(price_count/volume_count)
        price_count = 0
        volume_count = 0

plt.figure(figsize = (20, 10))
plt.plot(y_volumn_VWAP, label = "volumes bars",c = "orange")
plt.xlabel("100k volumes", fontsize = 20)
plt.ylabel("price", fontsize = 20)
plt.legend(fontsize = 20)
plt.show()

# In[5]
price_number = 10**9
number_of_bars = math.ceil(sum(TX_df.volume*TX_df.price)/sum(TX_df.volume)/price_number)
x_volumes = [*range(number_of_bars)]

y_volumn_VWAP = []
volume_count = 0
price_count = 0
for loc in range(len(TX_df)):
    volume_count += TX_df.iloc[loc].volume
    price_count += TX_df.iloc[loc].volume*TX_df.iloc[loc].price
    if price_count >= price_number:
        y_volumn_VWAP.append(price_count/volume_count)
        price_count = 0
        volume_count = 0

plt.figure(figsize = (20, 10))
plt.plot(y_volumn_VWAP, label = "dollars bars",c = "green")
plt.xlabel("1B dollars", fontsize = 20)
plt.ylabel("price", fontsize = 20)
plt.legend(fontsize = 20)
plt.show()



