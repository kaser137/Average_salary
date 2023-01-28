from service_file import get_stats_vacancies_hh, draw_table


def main():
    url = 'https://api.hh.ru/vacancies'
    langs = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go',
             'Shell', 'Objective-C', 'Scala', 'Swift', 'TypeScript']
    vacancies_stats = get_stats_vacancies_hh(url, langs, api_page=20)
    print(draw_table(vacancies_stats, 'Analysing vacancies. HeadHunter. Moscow'))


if __name__ == '__main__':
    main()
