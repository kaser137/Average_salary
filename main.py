import hh
import superjob
import requests
import time


try:
    hh.main()
except requests.exceptions.ConnectionError:
    time.sleep(10)
    hh.main()
try:
    superjob.main()
except requests.exceptions.ConnectionError:
    time.sleep(10)
    superjob.main()
