import pandas as pd
from multiprocessing import Process, Queue

''' Мультипроцессинг, начинает работу функций, построчно считывает вакансии из каждого файла в папке'''
def start(vac, queue, year):
    vacancies = pd.read_csv(f'files_csv\\{year}.csv')
    vacancies.loc[:, 'salary'] = vacancies.loc[:, ['salary_from', 'salary_to']].mean(axis=1)
    vac_job = vacancies[vacancies["name"].str.contains(vac)]

    salary_year = {year: []}
    count_year = {year: 0}
    job_salary_year = {year: []}
    job_count_year = {year: 0}

    salary_year[year] = int(vacancies['salary'].mean())
    count_year[year] = len(vacancies)
    job_salary_year[year] = int(vac_job['salary'].mean())
    job_count_year[year] = len(vac_job)

    list = [salary_year, count_year, job_salary_year, job_count_year]
    queue.put(list)


if __name__ == "__main__":
    class Input:
        ''' Класс для получения данных от пользователя'''
        def __init__(self):
            self.file_name = input("Введите название файла: ")
            self.job = input("Введите название профессии: ")

    class MakeCvs:
        ''' Класс для разбиения вакансий на отдельные файлы'''
        def __init__(self, file_name):
            self.file = pd.read_csv(file_name)

            self.file["years"] = self.file["published_at"].apply(
                lambda date: int(".".join(date[:4].split("-"))))
            self.years = list(self.file["years"].unique())

            for year in self.years:
                data = self.file[self.file["years"] == year]
                data[["name", "salary_from", "salary_to",
                      "salary_currency", "area_name",
                      "published_at"]].to_csv(f"files_csv\\{year}.csv", index=False)


    ''' Сортирует массивы вакансий по годам'''
    def sortedDic(dictionary):
        sorted_dict = {}
        for key in sorted(dictionary):
            sorted_dict[key] = dictionary[key]
        return sorted_dict


    ''' Сортирует массивы вакансий по городам'''
    def sorted_area(dictionary):
        sorted_tuples = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)[:10]
        sorted_dict = {k: v for k, v in sorted_tuples}
        return sorted_dict

    input = Input()
    file = input.file_name
    job = input.job
    makeCsv = MakeCvs(file)
    fileCsv = makeCsv.file
    years = makeCsv.years
    listDict = []

    ''' Преобразует зарплату и дату в нужный формат'''
    fileCsv['salary'] = fileCsv.loc[:, ['salary_from', 'salary_to']].mean(axis=1)
    fileCsv["published_at"] = fileCsv["published_at"].apply(lambda date: int(".".join(date[:4].split("-"))))

    ''' Находит самые крупные города и записывает только уникальные значения'''
    vacs = len(fileCsv)
    fileCsv["count"] = fileCsv.groupby("area_name")['area_name'].transform("count")
    dif = fileCsv[fileCsv['count'] >= 0.01 * vacs]
    cities = list(dif["area_name"].unique())

    salary_year = {}
    count_year = {}
    job_salary_year = {}
    job_count_year = {}
    job_salary_city = {}
    job_count_city = {}

    ''' Находит долю вакансий по городам'''
    for city in cities:
        difCities = dif[dif['area_name'] == city]
        job_salary_city[city] = int(difCities['salary'].mean())
        job_count_city[city] = round(len(difCities) / len(fileCsv), 4)

    queue = Queue()
    processes = []

    ''' Начало всех процессов мультипроцессинга'''
    for year in years:
        process = Process(target=start, args=(job, queue, year))
        processes.append(process)
        process.start()

    ''' Конец всех процессов мультипроцессинга'''
    for process in processes:
        listDict = queue.get()
        salary_year.update(listDict[0])
        count_year.update(listDict[1])
        job_salary_year.update(listDict[2])
        job_count_year.update(listDict[3])
        process.join()

    print("Динамика уровня зарплат по годам:", sortedDic(salary_year))
    print("Динамика количества вакансий по годам:", sortedDic(count_year))
    print("Динамика уровня зарплат по годам для выбранной профессии:", sortedDic(job_salary_year))
    print("Динамика количества вакансий по годам для выбранной профессии:", sortedDic(job_count_year))
    print("Уровень зарплат по городам (в порядке убывания):", sorted_area(job_salary_city))
    print("Доля вакансий по городам (в порядке убывания):", sorted_area(job_count_city))