import unittest
from Task232 import *


class MyTestCase(unittest.TestCase):
    def test_HTML_TAG(self):
        self.assertEqual(DataSet("vacancies.csv").formatting_str(["<p><strong>О компании:</strong></p>"]), ['О компании:'])  # add assertion here

    def test_escaped_chars(self):
        self.assertEqual(DataSet("vacancies.csv").formatting_str(["sdvsd\nascc"]), ["sdvsd\nascc"])

    def test_big_count_spaces(self):
        self.assertEqual(DataSet("vacancies.csv").formatting_str(["s     c"]), ["s c"])

    def test_filter_currency(self):
        vacancy1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                            'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                            'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy2 = Vacancy({'name': 'Программист', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                            'experience_id': 'noExperience', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vacancy1, vacancy2]
        self.assertEqual(InputConnectVacancy('', '', '', [0,91], '').data_filter(vacancies, ["Идентификатор валюты оклада", "Рубли"]), [vacancy2])

    def test_filter_salary(self):
        vacancy1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                            'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                            'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy2 = Vacancy({'name': 'Программист', 'description': 'Нет данных', 'key_skills': 'Нет данных',
                            'experience_id': 'noExperience', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vacancy1, vacancy2]
        self.assertEqual(InputConnectVacancy('', '', '', [0, 91], '').data_filter(vacancies,
                                                                                  ["Оклад",
                                                                                   "1000"]), [vacancy1])

    def test_filter_skills(self):
        vacancy1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Python\nCSS',
                            'experience_id': 'noExperience', 'premium': 'true', 'employer_name': 'Нет данных',
                            'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy2 = Vacancy({'name': 'Программист', 'description': 'Нет данных', 'key_skills': 'Git\nPython',
                            'experience_id': 'noExperience', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true', 'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vacancy1, vacancy2]
        self.assertEqual(InputConnectVacancy('', '', '', [0, 91], '').data_filter(vacancies,
                                                                                  ["Навыки",
                                                                                   "Git"]), [vacancy2])

    def test_sort_experience_id(self):
        vacancy1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Python\nCSS',
                            'experience_id': 'between3And6', 'premium': 'true', 'employer_name': 'Нет данных',
                            'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy2 = Vacancy({'name': 'Программист', 'description': 'Нет данных', 'key_skills': 'Git\nPython',
                            'experience_id': 'between1And3', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true',
                            'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy3 = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'Git\nPython',
                            'experience_id': 'noExperience', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true',
                            'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vacancy3, vacancy2, vacancy1]
        self.assertEqual(InputConnectVacancy('', '', '', [0, 91], '').sort_data(vacancies, "Опыт работы", False), vacancies)

    def test_sort_salary(self):
        vacancy1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Python\nCSS',
                            'experience_id': 'between3And6', 'premium': 'true', 'employer_name': 'Нет данных',
                            'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy2 = Vacancy({'name': 'Программист', 'description': 'Нет данных', 'key_skills': 'Git\nPython',
                            'experience_id': 'between1And3', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '10', 'salary_to': '1000000', 'salary_gross': 'true',
                            'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy3 = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'Git\nPython',
                            'experience_id': 'noExperience', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true',
                            'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vacancy3, vacancy2, vacancy1]
        self.assertEqual(InputConnectVacancy('', '', '', [0, 91], '').sort_data(vacancies, "Оклад", True), vacancies)

    def test_sort_skills(self):
        vacancy1 = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Python\nHTML',
                            'experience_id': 'between3And6', 'premium': 'true', 'employer_name': 'Нет данных',
                            'salary_from': '100', 'salary_to': '1000', 'salary_gross': 'true', 'salary_currency': 'EUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy2 = Vacancy({'name': 'Программист', 'description': 'Нет данных', 'key_skills': 'Git\nPython',
                            'experience_id': 'between1And3', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '10', 'salary_to': '1000000', 'salary_gross': 'true',
                            'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancy3 = Vacancy({'name': 'Фронт-разработчик', 'description': 'Нет данных', 'key_skills': 'Git\nHTML',
                            'experience_id': 'noExperience', 'premium': 'false', 'employer_name': 'Нет данных',
                            'salary_from': '100000', 'salary_to': '1000000', 'salary_gross': 'true',
                            'salary_currency': 'RUR',
                            'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        vacancies = [vacancy3, vacancy2, vacancy1]
        self.assertEqual(InputConnectVacancy('', '', '', [0, 91], '').sort_data(vacancies, "Навыки", False), vacancies)

    def test_formatter(self):
        vacancy = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Python\nHTML',
                                'experience_id': 'between3And6', 'premium': 'True', 'employer_name': 'Нет данных',
                                'salary_from': '1000', 'salary_to': '11000', 'salary_gross': 'True',
                                'salary_currency': 'EUR',
                                'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        result = ['Аналитик', 'Нет данных', 'Python\nHTML', 'От 3 до 6 лет', 'Да', 'Нет данных',
                  '1 000 - 11 000 (Евро) (Без вычета налогов)', 'Москва', '06.07.2022']
        self.assertEqual(InputConnectVacancy('', '', '', [0, 91], '').formatter(vacancy), result)

    def test_formatter_check_false(self):
        vacancy = Vacancy({'name': 'Аналитик', 'description': 'Нет данных', 'key_skills': 'Python\nHTML',
                           'experience_id': 'between3And6', 'premium': 'False', 'employer_name': 'Нет данных',
                           'salary_from': '1000', 'salary_to': '11000', 'salary_gross': 'e',
                           'salary_currency': 'EUR',
                           'area_name': 'Москва', 'published_at': '2022-07-06T02:05:26+0300'})
        result = ['Аналитик', 'Нет данных', 'Python\nHTML', 'От 3 до 6 лет', 'Нет', 'Нет данных',
                  '1 000 - 11 000 (Евро) (С вычетом налогов)', 'Москва', '06.07.2022']
        self.assertEqual(InputConnectVacancy('', '', '', [0, 91], '').formatter(vacancy), result)

if __name__ == '__main__':
    unittest.main()