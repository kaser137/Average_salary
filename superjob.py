import os
import dotenv
from pathlib import Path
from service_file import get_stats_vacancies_sj, draw_table


def main():
    dotenv.load_dotenv(Path('venv', '.env'))
    app_key = os.environ['SUPERJOB_KEY']
    app_code = os.environ['SUPERJOB_CODE']
    url = 'https://api.superjob.ru/2.0/vacancies/'
    langs = ['JavaScript', 'Java', 'Python', 'Ruby', 'PHP', 'C++', 'C#', 'C', 'Go',
             'Shell', 'Objective-C', 'Scala', 'Swift', 'TypeScript']
    vacancies_stats = get_stats_vacancies_sj(url, langs, app_code, app_key, 5)
    print(draw_table(vacancies_stats, 'Analysing vacancies. SuperJob. Moscow'))


if __name__ == '__main__':
    main()
