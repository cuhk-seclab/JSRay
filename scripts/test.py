import os
import shutil
import sys
import time
from lib2to3.pgen2 import driver
from urllib.parse import urlparse

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

# python3 main.py port sitefile logfile

version = '96.0.4664.35'

website = ['https://google.com']
# comment these for single test
with open(sys.argv[1], 'r') as f:
    website = f.readlines()


def NewDriver():
    options = Options()
    options.headless = True
    options.binary_location = '/path/to/chrome'
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--user-data-dir=profile')
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager(version=version, chrome_type=ChromeType.CHROMIUM).install()), options=options)
    driver.set_page_load_timeout(30)
    return driver


for url in website:
    try:
        os.remove('out.log')
    except Exception as e:
        pass
    try:
        os.remove('script.log')
    except Exception as e:
        pass
    try:
        shutil.rmtree('profile')
    except Exception as e:
        pass
    url = url.strip()
    print('Running', url, flush=True)
    try:
        driver = NewDriver()
        driver.get(url)
        time.sleep(10)
        try:
            driver.quit()
        except Exception as e:
            pass
        os.rename('script.log',
                  f'./log/script/{url.removeprefix("https://")}.log')
        os.rename('out.log', f'./log/{url.removeprefix("https://")}.log')
    except TimeoutException as e:
        print('Timeout', flush=True)
        try:
            driver.quit()
        except Exception as e:
            pass
        os.rename('script.log',
                  f'./log/script/{url.removeprefix("https://")}.log')
        os.rename('out.log', f'./log/{url.removeprefix("https://")}.log')
    except Exception as e:
        print('Error', flush=True)
        try:
            driver.quit()
        except Exception as e:
            pass
    time.sleep(2)

print('Finish', flush=True)
