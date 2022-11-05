import os
from dotenv import load_dotenv
load_dotenv()
import requests
from blockstream import blockexplorer
import matplotlib.pyplot as plt
address = os.getenv("address")
import random
import numpy as np

addr_info = blockexplorer.get_address(address)
print(addr_info.chain_stats)
btc_balance = addr_info.chain_stats["funded_txo_sum"]
plt.ion()
plt.show()
p = []
balance = []
for i in range(100):
    p+=[i]
    btc_rub = np.random.normal(22000, 100)
    balance.append(btc_balance*btc_rub)
    plt.plot(p, balance)
    plt.pause(0.5)
