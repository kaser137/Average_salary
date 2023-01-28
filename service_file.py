import requests
from terminaltables import AsciiTable


def choice_for_average_salary(vacancy_attrs, pay_from, pay_to):
    if vacancy_attrs['currency'] not in ("RUR", 'rub', None):
        return None
    if vacancy_attrs[pay_from] and vacancy_attrs[pay_to]:
        salary = (vacancy_attrs[pay_from] + vacancy_attrs[pay_to]) / 2
    elif vacancy_attrs[pay_from]:
        salary = vacancy_attrs[pay_from] * 1.2
    elif vacancy_attrs[pay_to]:
        salary = vacancy_attrs[pay_to] * 0.8
    else:
        salary = None
    return salary


def predict_rub_salary_hh(api_url, target_vacancy, api_page=20):
    page = 0
    per_page = 100
    area = 1
    vacancies_found_quantity = 0
    vacancies_quantity = 0
    total_sum = 0
    url = api_url
    while page < api_page:
        payload = {'page': f'{page}', 'per_page': per_page, 'area': area, 'vacancy_search_fields': 'name',
                   'text': f'{target_vacancy}'}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        answer = response.json()
        vacancy_attrs = answer['items']
        vacancies_found_quantity = answer['found']
        for vacancy in vacancy_attrs:
            if vacancy['salary']:
                salary = choice_for_average_salary(vacancy['salary'], 'from', 'to')
                if salary:
                    total_sum += salary
                    vacancies_quantity += 1
        page += 1
    if vacancies_quantity:
        return int(total_sum / vacancies_quantity), vacancies_quantity, vacancies_found_quantity
    else:
        return 0, 0, vacancies_found_quantity


def predict_rub_salary_sj(api_url, target_vacancy, app_code=None, app_key=None, api_page=1):
    page = 0
    count = 100
    town = 4
    vacancies_found_quantity = 0
    vacancies_quantity = 0
    total_sum = 0
    url = api_url
    while page < api_page:
        payload = {'code': app_code, 'app_key': app_key, 'town': town, 'count': count, 'keyword': f'{target_vacancy}',
                   'page': f'{page}'}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        answer = response.json()
        vacancy_attrs = answer['objects']
        vacancies_found_quantity = answer['total']
        for vacancy in vacancy_attrs:
            if vacancy:
                salary = choice_for_average_salary(vacancy, 'payment_from', 'payment_to')
                if salary:
                    total_sum += salary
                    vacancies_quantity += 1
        page += 1
    if vacancies_quantity:
        return int(total_sum / vacancies_quantity), vacancies_quantity, vacancies_found_quantity
    else:
        return 0, 0, vacancies_found_quantity


def get_stats_vacancies_hh(url, languages, api_page=20):
    vacancies_stats = {}
    for lang in languages:
        average_salary, vacancies_processed, vacancies_found = predict_rub_salary_hh(url, f'программист {lang}',
                                                                                     api_page)
        vacancies_stats[lang] = {'vacancies_found': vacancies_found, 'vacancies_processed': vacancies_processed,
                                 'average_salary': average_salary}
    return vacancies_stats


def get_stats_vacancies_sj(url, langs, app_code=None, app_key=None, api_page=5):
    vacancies_stats = {}
    for lang in langs:
        average_salary, vacancies_processed, vacancies_found = predict_rub_salary_sj(url, f'программист {lang}',
                                                                                     app_code, app_key, api_page)
        vacancies_stats[lang] = {'vacancies_found': vacancies_found, 'vacancies_processed': vacancies_processed,
                                 'average_salary': average_salary}
    return vacancies_stats


def draw_table(user_dictionary, title):
    table_vacancies_data = []
    heading = ['Язык программирования', 'Вакансий найдено ', 'Вакансий обработано', 'Средняя зарплата ']
    table_vacancies_data.append(heading)
    for language in user_dictionary:
        table_vacancies_data.append([item for item in user_dictionary[language].values()])
        table_vacancies_data[-1].insert(0, language)
    title = title
    table = AsciiTable(table_vacancies_data, title).table
    return table
