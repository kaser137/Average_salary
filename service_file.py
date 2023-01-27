import requests
from terminaltables import AsciiTable


def choice_for_average_salary(vacancy_attr_list, pay_from, pay_to):
    if vacancy_attr_list['currency'] not in ("RUR", 'rub', None):
        return None
    if vacancy_attr_list[pay_from] and vacancy_attr_list[pay_to]:
        salary = (vacancy_attr_list[pay_from] + vacancy_attr_list[pay_to]) / 2
    elif vacancy_attr_list[pay_from]:
        salary = vacancy_attr_list[pay_from] * 1.2
    elif vacancy_attr_list[pay_to]:
        salary = vacancy_attr_list[pay_to] * 0.8
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
        resp_json_list = answer['items']
        vacancies_found_quantity = answer['found']
        for vacancy in resp_json_list:
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
        resp_json_list = answer['objects']
        vacancies_found_quantity = answer['total']
        for vacancy in resp_json_list:
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


def get_stats_vacancies_hh(url, langs_list, api_page=20):
    vacancies = {}
    for lang in langs_list:
        average_salary, vacancies_processed, vacancies_found = predict_rub_salary_hh(url, f'программист {lang}',
                                                                                     api_page)
        vacancies[lang] = {'vacancies_found': vacancies_found, 'vacancies_processed': vacancies_processed,
                           'average_salary': average_salary}
    return vacancies


def get_stats_vacancies_sj(url, langs_list, app_code=None, app_key=None, api_page=5):
    vacancies = {}
    for lang in langs_list:
        average_salary, vacancies_processed, vacancies_found = predict_rub_salary_sj(url, f'программист {lang}',
                                                                                     app_code, app_key, api_page)
        vacancies[lang] = {'vacancies_found': vacancies_found, 'vacancies_processed': vacancies_processed,
                           'average_salary': average_salary}
    return vacancies


def draw_table(user_dictionary, title):
    table_data_list = []
    heading = ['Язык программирования', 'Вакансий найдено ', 'Вакансий обработано', 'Средняя зарплата ']
    table_data_list.append(heading)
    for key in user_dictionary:
        table_data_list.append([item for item in user_dictionary[key].values()])
        table_data_list[-1].insert(0, key)
    title = title
    table = AsciiTable(table_data_list, title).table
    return table
