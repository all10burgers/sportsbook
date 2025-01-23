import re
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']
base_url = "https://www.basketball-reference.com/leagues/NBA_2024_games-"
urls = [f"{base_url}{month}.html" for month in months]

def scrape_monthly(url):
    response = requests.get(url)
    time.sleep(10)
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all('table', {'id': 'schedule'})

    data = []
    for table in tables:
        for row in table.find_all('tr')[1:]:
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols]
            data.append(cols)

    return data

all_data = []
for url in urls:
    monthly_data = scrape_monthly(url)
    all_data.extend(monthly_data)

# for i, row in enumerate(all_data):
#     if len(row) != 11:
#         print(f"Row {i} has {len(row)} columns: {row}")

columns = ['Date', 'Start', 'Visitor', 'VisitorPTS', 'Home', 'HomePTS', 'BoxScore' , '' , 'OT', 'Attendance', 'Arena' , 'Notes']
df = pd.DataFrame(all_data, columns=columns)
#df.head()
#fixed_df = df.drop(df['Attendance'], df['Arena'], df['Notes'])
#fixed_df.head()

dd = df.to_csv('test_1.csv', index=False)