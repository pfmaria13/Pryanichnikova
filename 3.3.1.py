import pandas as pd
import xmltodict
import requests


def get_currency_frequency(data_file):
    """Получает список валют, которые встречаются в более чем в 5000 вакансий
    Args:
        data_file (DataFrame): Данные из файла vacancies_dif_currencies.csv
    Returns:
        list: Cписок валют
    """
    currency_dict = data_file['salary_currency'].value_counts().to_dict()
    currency_dict = {key: value for key, value in currency_dict.items() if value >= 5000}
    return list(currency_dict.keys())


def get_years_currency(file_name):
    """Собирает курсы валют за диапазон между самой старой и новой вакансией с частотностью раз в месяц,
     сохранет полученный результат (формат dataframe) в csv
    Args:
        file_name (str): Путь к файлу vacancies_dif_currencies.csv
    """
    data_file = pd.read_csv(file_name)
    result = pd.DataFrame()
    currency_dict = get_currency_frequency(data_file)
    data_file = data_file[data_file["salary_currency"].isin(currency_dict)]
    range_date = [data_file["published_at"].min().split("-")[:2], data_file["published_at"].max().split("-")[:2]]
    row = {}
    for year in range(int(range_date[0][0]), int(range_date[1][0]) + 1):
        for month in range(int(range_date[0][1]), 13):
            print(year, month)
            try:
                response = requests.get(r"http://www.cbr.ru/scripts/XML_daily.asp?date_req=01/{0}/{1}"
                                        .format(str(month).zfill(2), year))
            except Exception:
                continue

            response = xmltodict.parse(response.text)
            for i in response['ValCurs']['Valute']:
                if i['CharCode'] in currency_dict:
                    row["date"] = "{0}-{1}".format(year, str(month).zfill(2))
                    row[i['CharCode']] = round(float(i["Value"].replace(",", ".")) / int(i["Nominal"]), 7)
            result = pd.concat([result, pd.DataFrame([row])])
            if year == int(range_date[1][0]) and month == int(range_date[1][1]) or month == 12:
                break

    result.to_csv("currency.csv", index=False)

def split_by_year(path_to_file):
    """
    Разделяет входной файл на меньшие, группирует по годам
    Args:
        path_to_file (str): Путь к входному csv-файлу
    """
    data_of_file = pd.read_csv(path_to_file)
    data_of_file["year"] = data_of_file["published_at"].apply(lambda x: x[:4])
    data_of_file = data_of_file.groupby("year")
    for year, data in data_of_file:
        data[["name", "salary_from", "salary_to", "salary_currency", "area_name", "published_at"]].\
            to_csv(rf"data\csv_by_years_dif_currencies\year_number_{year}.csv", index=False)


get_years_currency('vacancies_dif_currencies.csv')

split_by_year("vacancies_dif_currencies.csv")