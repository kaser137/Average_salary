# Analysing vacancies

## What is this?

This project gets vacancies from HeadHunter and SuperJob, and then calculate average salary for each. 

## How it works?

For working with this project, you have to copy all files in the working directory at your choice.  Create in working 
directory subdirectory "venv" and file ".env" in this subdirectory. In this file, you have to write 2 lines like this:
```python
SUPERJOB_CODE=2274
SUPERJOB_KEY=b4.g.137247650.6ff21dd5bbeea257bda70ng7kdf6efc84f856b88.f8dsa5a6aa5f0ca040f107ded2673feeb3e7bc8e
```
(presented values is not correct, it's just for example).

Where SUPERJOB_CODE is your code for API SuperJob, SUPERJOB_KEY is your Secret key for API SuperJob, this code and key
you can take after registration at address: https://api.superjob.ru/register/, you may use for registration address of
any site,  it will be correctly.

Python3 should  already be installed. Then use pip (or pip3, if there is a conflict with Python2) to install
dependencies: `pip install -r requirements.txt`

Start file `main.py`, it makes 2 tables in your console, first table is info from HeadHunter, second - from SuperJob.
Program analyse vacancies for programmers in Moscow, if you want to change region change value of 'area' according to 
tree of areas at address https://api.hh.ru/areas, and value of 'town' which you can find at address 
https://api.superjob.ru/2.0/towns/, all info presented in JSON format. All changes you have to do in variable "payload"
of function `predict_rub_salary(api_url, target_vacancy, app_code=None, app_key=None, api_page=1)`, which is in file
`service_file.py` at string №27.

You also can start program only for HeadHunter, or only forSuperJob, you have to start files `hh.py` or `superjob.py`
respectively.



Код написан в образовательных целях на курсах для веб-разработчиков [dvmn.org](https://dvmn.org/).