import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from google.cloud import bigquery
from google.oauth2 import service_account
from sendmail import send_mail

# connection with gsheet config
gcreds = os.environ['creds_fileT']
scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
credentials = ServiceAccountCredentials.from_json_keyfile_name(gcreds, scope)
gclient = gspread.authorize(credentials)


credentials = service_account.Credentials.from_service_account_file('bq.json')
project_id = 'my_project'
client = bigquery.Client(credentials=credentials, project=project_id)


query_job = client.query("""WITH
  counters AS (
  SELECT
    offer.identifier AS offer_identifier,
    1 AS imps,
    0 AS clicks
  FROM
    `table1`,
    UNNEST( offer.offers ) AS offer
  WHERE
    day BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  UNION ALL
  SELECT
    offer_identifier,
    0 AS imps,
    1 AS clicks,
  
  FROM
    `table2`
  WHERE
    day BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    AND DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY) )
SELECT
  offer_identifier,
  SUM(imps) AS impsCount,
  SUM(clicks) AS clicksCount
FROM
  counters
GROUP BY
  offer_identifier
ORDER BY
  impsCount DESC
""")

result = query_job.result()
rows = list(result)

data = []
for row in rows:
    data.append(row[0:3])


header = ('offer_id', 'impsCount', 'clicksCount')
data.insert(0,header)

with open('test.csv', 'w') as file:
        file.write("\n".join(str(item).replace("('","").replace(")","").replace("'","") for item in data))



recipients = ["arkadiusz.latek@com"]
title = 'test mail title'
fileToSend = "test.csv"
msg = """\
File in the attachment 
"""

send_mail(recipients, title, msg, fileToSend)

