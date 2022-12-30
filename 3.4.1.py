import pandas as pd
import csv

comp = dict()

with open('dataframe.csv', encoding='utf-8') as file:
    reader = csv.reader(file)
    comp_head = next(reader)
    for i in reader:
        comp[tuple(i[0].split('-'))] = {k: v for k, v in zip(comp_head, i)}

def salary_conversion(sal_from, sal_to, sal_cur, publ_at):
    year, month = publ_at.split('T')[0].split('-')[:2]
    if (year, month) not in comp or sal_cur == '' or (sal_to == 0 and sal_from == 0):
        return None
    d = comp[year, month]
    if d[sal_cur] == '' or sal_cur not in d:
        return None
    sal, c = 0, 0
    if sal_from != 0:
        sal += sal_from
        c += 1
    if sal_to != 0:
        sal += sal_to
        c += 1
    if sal_cur != 'RUR':
        sal *= float(d[sal_cur])
    return sal // c

data = pd.read_csv('vacancies_dif_currencies.csv', encoding='utf-8-sig').fillna(0)
data['salary'] = data.apply(lambda row: salary_conversion(row['salary_from'], row['salary_to'], row['salary_currency'], row['published_at']), axis=1)
with open('new_salary.csv', 'w', encoding='utf-8-sig', newline='') as file:
    data[['name', 'salary', 'area_name', 'published_at']][:100].to_csv(file, index=False)