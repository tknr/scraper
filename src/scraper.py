#!/usr/bin/python
import sys
import os
import time
import json

from get_chrome_driver import GetChromeDriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def showUsage():
    print("usage: %s [url] " % os.path.basename(__file__))


args = sys.argv
args_length = len(args)
if args_length == 1:
    showUsage()
    exit()

URL = args[1]

get_driver = GetChromeDriver()
get_driver.install()

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--remote-debugging-port=9222')  # Specify a port
options.add_argument('--disable-setuid-sandbox')

options.add_argument("--incognito")
options.add_argument("--disable-application-cache")
options.add_argument("--enable-do-not-track")
options.add_argument("--disable-popup-blocking")

options.binary_location = '/usr/bin/google-chrome'

options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

driver = webdriver.Chrome(options=options)
driver.get(URL)
time.sleep(3)

if args[2] == "html" or args[2] == "HTML" : 
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)
elif args[2] == "logs" or args[2] == "LOGS" :
    logs = driver.get_log('performance')
    for entry in logs:
        message_data = json.loads(entry['message'])['message']['params']
    
        # リクエスト情報が存在する場合のみ処理
        if 'request' in message_data:
            request_data = message_data['request']
            request_url = request_data['url']
            request_headers = request_data['headers']

            # ボディを取得
            if 'postData' in request_data:
                post_data = request_data['postData']
            else:
                post_data = None

            # クッキーはSeleniumのメソッドを利用して取得
            cookies = driver.get_cookies()

            print(f"URL: {request_url}")
            print(f"Headers: {request_headers}")
            print(f"Cookies: {cookies}")
            print(f"Body: {post_data}")
            print("-" * 50)

driver.quit()


