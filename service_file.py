import requests
from terminaltables import AsciiTable


def choice_for_average_salary(vac_attr_list, pay_from, pay_to):
    if vac_attr_list['currency'] in ("RUR", 'rub', None):
        if vac_attr_list[pay_from] and vac_attr_list[pay_to]:
            salary = (vac_attr_list[pay_from] + vac_attr_list[pay_to]) / 2
        elif vac_attr_list[pay_from]:
            salary = vac_attr_list[pay_from] * 1.2
        elif vac_attr_list[pay_to]:
            salary = vac_attr_list[pay_to] * 0.8
        else:
            salary = None
    else:
        salary = None
    return salary


def predict_rub_salary(api_url, target_vacancy, app_code=None, app_key=None, api_page=1):
    vac_number = 0
    total_sum = 0
    page = 0
    vac_found_number = 0
    url = api_url
    while page < api_page:
        payload = {'code': app_code, 'app_key': app_key, 'town': 4, 'count': 100, 'keyword': f'{target_vacancy}',
                   'page': f'{page}', 'per_page': 100, 'area': 1, 'vacancy_search_fields': 'name',
                   'text': f'{target_vacancy}'}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        if app_code:
            resp_json_list = response.json()['objects']
            vac_found_number = response.json()['total']
            pay_from = 'payment_from'
            pay_to = 'payment_to'
        else:
            resp_json_list = response.json()['items']
            vac_found_number = response.json()['found']
            pay_from = 'from'
            pay_to = 'to'
        for vacancy in resp_json_list:
            if not app_code:
                if vacancy['salary']:
                    vac_attr_list = vacancy['salary']
                else:
                    vac_attr_list = None
            else:
                vac_attr_list = vacancy
            if vac_attr_list:
                salary = choice_for_average_salary(vac_attr_list, pay_from, pay_to)
                if salary:
                    total_sum += salary
                    vac_number += 1
        page += 1
    if vac_number:
        return int(total_sum / vac_number), vac_number, vac_found_number
    else:
        return 0, 0, vac_found_number


def get_stats_vacancies(url, langs_list, app_code=None, app_key=None, api_page=1):
    vacancies = {}
    for lang in langs_list:
        average_salary, vacancies_processed, vacancies_found = predict_rub_salary(url, f'программист {lang}', app_code,
                                                                                  app_key, api_page)
        vacancies[lang] = {'vacancies_found': vacancies_found, 'vacancies_processed': vacancies_processed,
                           'average_salary': average_salary}
    return vacancies


def draw_table(user_dictionary, title):
    table_data = []
    heading = ['Язык программирования', 'Вакансий найдено ', 'Вакансий обработано', 'Средняя зарплата ']
    table_data.append(heading)
    for key in user_dictionary:
        table_data.append([item for item in user_dictionary[key].values()])
        table_data[-1].insert(0, key)
    title = title
    table = AsciiTable(table_data, title)
    print('\n', table.table)
