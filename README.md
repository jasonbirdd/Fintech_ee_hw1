---
title: 'Fintech COM HW1 詹凱錞'
disqus: hackmd
---

Fintech COM HW1 詹凱錞
===
Some modules are required:    
* matplotlib  
* pandas  
* mplfinance  
please install them or use
```
>> pip install -r requirements.txt
```

## First part:save TX.csv
This part will extract "TX" & due date at 2021/10 from each csv data in Hw1_data.
```python
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
```


## Second part:plot time bar
From TX_df dataframe, This part plot the VWAP value at each date.
```python
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
```
![](https://i.imgur.com/1SNGY44.png)



## Third part:plot ticks bar
This part plot the VWAP value in the number of “10k” ticks.
```python
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
```
![](https://i.imgur.com/6liRRpx.png)



## Fourth part:plot volume bar
This part plot the VWAP value in the volume of “100k”.
```python
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

```
![](https://i.imgur.com/tkXYtZz.png)



## Fifth part:plot dollar bar
This part plot the VWAP value every “1B” NTD.
```python
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

```
![](https://i.imgur.com/LL9vjaz.png)




## Sixth part:plot all & Candlestick Charts
Combine part2~part5 in a figure and add Candlestick Charts.
```python
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
```
![](https://i.imgur.com/Eof3hzm.png)

