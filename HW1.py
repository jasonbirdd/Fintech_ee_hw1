# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 21:19:34 2021

@author: 詹凱錞
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import mplfinance as mpf

# In[1]
label = ["date", "time", "price", "volume"]
TX_df = pd.DataFrame([], columns=label)

for root, dirs, files in os.walk("./HW1_data", topdown=False):
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
plt.plot(y_ticks_VWAP, label = "tick bars",c = "red")
plt.xlabel("10k ticks", fontsize = 20)
plt.ylabel("price", fontsize = 20)
plt.legend(fontsize = 20)
plt.show()

# In[4]
accumulate_volume = TX_df.volume.cumsum()

volume_number = 10**5
number_of_bars = math.ceil(sum(TX_df.volume)/volume_number)

y_volumn_VWAP = []

accumulate_volume = TX_df.volume.cumsum()
index = 0
index_next = 0
for i in range(number_of_bars-1):
    index_next = TX_df.index[accumulate_volume//volume_number == i+1][0]
    y_volumn_VWAP.append(sum(TX_df.volume[index:index_next]*TX_df.price[index:index_next])/sum(TX_df.volume[index:index_next]))
    index = index_next

plt.figure(figsize = (20, 10))
plt.plot(y_volumn_VWAP, label = "volume bars",c = "orange")
plt.xlabel("100k volumes", fontsize = 20)
plt.ylabel("price", fontsize = 20)
plt.legend(fontsize = 20)
plt.show()

# In[5]
price_number = 10**9
number_of_bars = math.ceil(sum(TX_df.volume*TX_df.price)/price_number)

y_dollar_VWAP = []

accumulate_dollar = (TX_df.volume*TX_df.price).cumsum()
index = 0
index_next = 0
for i in range(number_of_bars-1):
    index_next = TX_df.index[accumulate_dollar//price_number == i+1][0]
    y_dollar_VWAP.append(sum(TX_df.volume[index:index_next]*TX_df.price[index:index_next])/sum(TX_df.volume[index:index_next]))
    index = index_next

plt.figure(figsize = (20, 10))
plt.plot(y_dollar_VWAP, label = "dollar bars",c = "green")
plt.xlabel("1B dollars", fontsize = 20)
plt.ylabel("price", fontsize = 20)
plt.legend(fontsize = 20)
plt.show()


#%% total plot

fig, ax1 = plt.subplots(figsize = (20, 10))

curve1, = ax1.plot(y_VWAP, label = "time bars")
plt.xticks(x, x_1d, fontsize = 10)
plt.xlabel("date", fontsize = 20)
plt.ylabel("price", fontsize = 20)


ax2, ax3, ax4, ax5 = ax1.twiny(), ax1.twiny(), ax1.twiny(), ax1.twiny()
curve2, = ax2.plot(y_ticks_VWAP, c = "r", label = "tick bars")
curve3, = ax3.plot(y_volumn_VWAP, c = "orange", label = "volume bars")
curve4, = ax4.plot(y_dollar_VWAP, c = "green", label = "dollar bars")

curves = [curve1, curve2, curve3, curve4]

TX_date_df = pd.DataFrame([] , columns=['Date', 'Volume', 'Open', 'High', 'Low', 'Close'])
for day in x_1d:
    temp_date_list = [(day, sum(TX_df[(TX_df["date"]==day)].volume), TX_df.price[(TX_df["date"]==day)].iloc[0], max(TX_df.price[(TX_df["date"]==day)]),
                      min(TX_df.price[(TX_df["date"]==day)]), TX_df.price[(TX_df["date"]==day)].iloc[-1])]
    temp_date_df = pd.DataFrame(temp_date_list, columns=['Date', 'Volume', 'Open', 'High', 'Low', 'Close'])
    TX_date_df = TX_date_df.append(temp_date_df, ignore_index=True)
TX_date_df["Date"] = pd.to_datetime(TX_date_df['Date'], format='%Y%m%d')
TX_date_df.set_index('Date', inplace=True)
mpf.plot(TX_date_df, type='candle', style='yahoo', ylabel='price', ax = ax5)
ax5.margins(x = 0)

ax2.set_xticklabels("off")
ax3.set_xticklabels("off")
ax4.set_xticklabels("off")

ax1.legend(curves, [curve.get_label() for curve in curves], fontsize = 20)
plt.title("TX, due:202110", fontsize = 30)
plt.show()