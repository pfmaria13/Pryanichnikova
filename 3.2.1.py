import pandas as pd

file_name = input()
file = pd.read_csv(file_name)

''' Выделяет все года из файла и записывает уникальные значения в массив'''
file["years"] = file["published_at"].apply(lambda date: int(".".join(date[:4].split("-"))))
years = list(file["years"].unique())

''' По году получает значения из csv файла и записывает их в новый csv файл'''
for year in years:
    data = file[file["years"] == year]
    data.iloc[:, :6].to_csv(f"files_years\\{year}.csv", index=False)