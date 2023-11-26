from selenium import webdriver
import subprocess
import logging

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import platform
import traceback
import os
import time

def can_connect_to_chrome():
    try:
        # use selenium
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "debuggerAddress", "127.0.0.1:9222")
        chrome_driver = "./chromedriver"
        service = Service(executable_path=chrome_driver)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(5)
        driver.implicitly_wait(5)

        print('--------------------------title', driver.title)
        return True
    except:
        traceback.print_exc()
        return False


def create_chrome():

    params = ['--remote-debugging-port=9222',
              '--user-data-dir="./chrome-data"',
              '--no-first-run',
              '--no-default-browser-check',
              ]

    # 判断当前环境
    # 如果是windows，使用chrome.exe
    if platform.system() == 'Windows':
        chrome_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

    elif platform.system() == 'Linux':
        chrome_path = r'/usr/bin/google-chrome'
    elif platform.system() == 'Darwin':
        chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    else:
        print('Unknown system type!')
        exit(1)

    os.makedirs('chrome-data', exist_ok=True)
    command = [chrome_path] + params
    subprocess.Popen(command)
    time.sleep(2)
    logging.info('start check chrome success')
    if not can_connect_to_chrome():
        return False
    else:
        logging.info('chrome start success')
    return True


def start_chrome():
    logging.info('start chrome')
    if not can_connect_to_chrome():
        create_chrome()
