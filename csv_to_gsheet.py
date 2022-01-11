import csv
import os
import glob
import sys

import moment
import gspread
from oauth2client.service_account import ServiceAccountCredentials


passedDate = '2021-10-12'
passedFile = 'file.csv'
dataDate = moment.date(passedDate).subtract(days=1).format('YYYY-MM-DD')
print(dataDate)

gcreds = os.environ['key_file']

SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(gcreds, SCOPES)
gc = gspread.authorize(credentials)

sht = gc.open_by_key('spreadsheet_id')

countries = ['BR_NC', 'ID_NC', 'MY_NC', 'PH_NC', 'SG_NC', 'TH_NC', 'VN_NC', 'ID_EC', 'MY_EC', 'PH_EC', 'SG_EC', 'TH_EC', 'VN_EC']
data = {key:{'buyers': 0, 'new_buyers': 0, 'orders': 0, 'gmv': 0, 'first_order_gmv': 0, 'reinstalls': 0} for key in countries}
# print(data)

with open(passedFile) as csvFile:
    reader = csv.DictReader(csvFile)
    # print(reader.fieldnames)
    for row in reader:
        if row['Event Date'] == dataDate:
                gmv = 0 if row['GMV'] == '' else float(row['GMV'])
                firstOrderGMV = 0 if row['First Order GMV'] == '' else float(row['First Order GMV'])
                if 'ec' in row['Campaign'].lower():
                    data[row['\ufeffCountry'] + '_EC']['buyers'] += int(row['# Buyers'])
                    data[row['\ufeffCountry'] + '_EC']['new_buyers'] += int(row['# New Buyers'])
                    data[row['\ufeffCountry'] + '_EC']['orders'] += int(row['Checkouts'])
                    data[row['\ufeffCountry'] + '_EC']['gmv'] += gmv
                    data[row['\ufeffCountry'] + '_EC']['first_order_gmv'] += firstOrderGMV
                    data[row['\ufeffCountry'] + '_EC']['reinstalls'] += int(row['re_installs'])
                elif 'nc' in row['Campaign'].lower():
                    data[row['\ufeffCountry'] + '_NC']['buyers'] += int(row['# Buyers'])
                    data[row['\ufeffCountry'] + '_NC']['new_buyers'] += int(row['# New Buyers'])
                    data[row['\ufeffCountry'] + '_NC']['orders'] += int(row['Checkouts'])
                    data[row['\ufeffCountry'] + '_NC']['gmv'] += gmv
                    data[row['\ufeffCountry'] + '_NC']['first_order_gmv'] += firstOrderGMV
                    data[row['\ufeffCountry'] + '_NC']['reinstalls'] += int(row['re_installs'])

for cntry in countries:
    dataToUpdate = []
    dataToUpdate.extend([dataDate, data[cntry]['buyers'], data[cntry]['new_buyers'], data[cntry]['orders'], data[cntry]['gmv'], data[cntry]['first_order_gmv'], data[cntry]['reinstalls']])
    print(dataToUpdate)

    # update to sheet
    shttoUpdate = sht.worksheet(cntry.replace('_', ' '))
    nextRow = shttoUpdate.row_count + 1
    shttoUpdate.append_row(dataToUpdate, 'USER_ENTERED')
