import os
from dotenv import load_dotenv
load_dotenv()
import requests
from blockstream import blockexplorer
import matplotlib.pyplot as plt
address = os.getenv("address")
coinAPI_token = os.getenv("coinAPI_token")
import random
import numpy as np
import json
from matplotlib.dates import DateFormatter, datestr2num
import csv 
from datetime import datetime

# addr_info = blockexplorer.get_address(address)
# print(addr_info.chain_stats)
# btc_balance = addr_info.chain_stats["funded_txo_sum"]



url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USD/history?period_id=1DAY&time_start=2021-01-01T00:00:00&time_end=2022-11-10T00:00:00&limit=1000'
headers = {'X-CoinAPI-Key' :coinAPI_token}
#response = requests.get(url, headers=headers)

# with open('btcusd.json', 'wb') as f:
#    f.write(response.content)
with open("btcusd.json", "rb") as f:
    btcusd = json.load(f)

with open("electrum-history.json", "rb") as f:
    history = json.load(f)

btc_banker = []

with open("btc_banker_bot.csv", "r") as f:
    for row in csv.reader(f):
        date, value, status = row[0], row[3], row[-1]
        if status == ' confirm_payment':
            btc_banker.append({"date":datetime.strptime(date, '%d-%m-%Y %H:%M:%S').strftime('%m/%d/%Y %H:%M:%S'), "withdrawal":value})
btc_banker = btc_banker[::-1]



dates = []
balance = []
closes = []
highs = []
lows = []

withdrawal = []
current_balance:float = .0
total_withdrawal:float = .0


for trade_day in btcusd:
    if (len(history)> 0):
        history_item = history[0]
        if (history_item["date"]<=trade_day["time_close"]):
            current_balance = float(history_item["bc_balance"])
            history.pop(0)
    if len(btc_banker)> 0:
        banker_item = btc_banker[0]
        if datestr2num(banker_item["date"])<=datestr2num(trade_day["time_close"]):
            total_withdrawal += float(banker_item["withdrawal"])
            btc_banker.pop(0)


    dates.append(datestr2num(trade_day["time_close"]))
    balance.append(trade_day["rate_close"]*current_balance)
    closes.append(trade_day["rate_close"])
    highs.append(trade_day["rate_high"])
    lows.append(trade_day["rate_low"])
    withdrawal.append(total_withdrawal)


plt.ion()
fig, ax = plt.subplots()
fig.subplots_adjust(right=0.75)

ax2 = ax.twinx()
ax3 = ax.twinx()


l2, = ax2.plot(dates, balance, c="black", label = "Wealth")

ax.xaxis.set_major_formatter(DateFormatter("%Y-%m"))
ax.set_xlabel("Date")
ax2.set_ylabel("Total Wealth, $")
ax2.grid(True)
ax.set_xlim(dates[400], dates[-1])
ax2.yaxis.label.set_color(l2.get_color())



ax3.spines.right.set_position(("axes", 1.2))

l1, = ax.plot(dates, closes, c = "tab:blue")
ax.fill_between(dates,lows, highs, facecolor = "tab:blue", alpha=0.5)
ax.set_ylabel("BTC Rate, $")
ax.yaxis.label.set_color(l1.get_color())


l3, = ax3.plot(dates, withdrawal, color = "tab:green")
ax3.set_ylabel("Cash Withdrawal, RUB")
ax3.yaxis.label.set_color(l3.get_color())

ax.tick_params(axis='y', colors=l1.get_color())
ax2.tick_params(axis='y', colors=l2.get_color())
ax3.tick_params(axis='y', colors=l3.get_color())

fig.autofmt_xdate()

plt.show()
input("Any symbol to exit: ")
