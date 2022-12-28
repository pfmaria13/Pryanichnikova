import pandas as pd

file = 'vacancies_dif_currencies.csv'
df = pd.read_csv(file)
currencies = df['salary_currency'].unique()
currency = []
df.sort_values(by='published_at', inplace=True)
for curr in currencies:
    if list(df['salary_currency']).count(curr) > 5000:
        currency.append(curr)
del currency[0]
early_date = list(df['published_at'])[0]
late_date = list(df['published_at'])[-1]
data_currency = pd.DataFrame(columns=["date", "BYR", "USD", "EUR", "KZT", "UAH"])
for year in range(2003, 2023):
    for month in range(1, 13):
        date = f'01/0{month}/{year}' if month < 10 else f'01/{month}/{year}'
        res = f'http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}'
        new_row = {'date': date}
        values_cur = pd.read_xml(res, encoding='cp1251')
        for cur in currency:
            if len(values_cur[values_cur['CharCode'] == cur]['Value'].values) != 0:
                value = '.'.join(str(values_cur[values_cur['CharCode'] == cur]['Value'].values[0]).split(','))
                new_row[cur] = float(value) / int(values_cur[values_cur['CharCode'] == cur]['Nominal'].values[0])
        data_currency = pd.concat([data_currency, pd.DataFrame.from_records([new_row])], axis=0, ignore_index=True)
        if date == '01/07/2022':
            break
data_currency.to_csv("data_currency.csv", index=False)
print(data_currency)