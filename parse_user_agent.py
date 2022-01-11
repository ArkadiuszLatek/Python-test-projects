import pandas as pd
from user_agents import parse
import json
import csv

click_data = pd.read_csv("file.csv", sep=',')

my_data = pd.DataFrame(click_data)
# print(my_data[1])


browser_data = []
os = []
dev = []
br = []
cn = []
for index, row in my_data.iterrows():
    user_agent = parse(row['user_agent'])
    cnt = row['cnt']
    cn.append(cnt)
    b_family = user_agent.browser.family
    os_family = user_agent.os.family
    device = user_agent.device.family
    dev.append(device)
    brand = user_agent.device.brand
    br.append(brand)
    browser_data.append(b_family)
    os.append(os_family)


# print(browser_data)
dfob = pd.DataFrame(browser_data)
dfob['os_family'] = os
dfob['device'] = dev
dfob['brand'] = br
dfob['cnt'] = cn

print(dfob)
dfob.to_csv(r'agent_data_file.csv', index = False)


