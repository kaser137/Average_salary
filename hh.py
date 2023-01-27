from service_file import get_stats_vacancies_hh, draw_table


def main():
    url = 'https://api.hh.ru/vacancies'
    langs_list = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go',
                  'Shell', 'Objective-C', 'Scala', 'Swift', 'TypeScript']
    vacancies = get_stats_vacancies_hh(url, langs_list, api_page=20)
    print(draw_table(vacancies, 'Analysing vacancies. HeadHunter. Moscow'))


if __name__ == '__main__':
    main()
