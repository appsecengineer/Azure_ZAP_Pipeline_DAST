# coding: utf-8
from RoboBurp2 import *
import time
url_list = ["http://134.209.146.136/"]
scanId = ''


def run_burp_in_headless_mode():
    try:
        burp_handler = RoboBurp2(url_list)
        print("Initiate Burp")
        path = "/burpsuite_pro_v2.0.11beta.jar"
        user_config = "user_options.json"
        project_config = "project.json"
        burp_handler.start_headless_burpsuite(path,user_config=user_config,project_config=project_config)
        #burp_handler.start_headless_burpsuite(path,user_config=user_config)
        sleep(60)
    except Exception as e:
        print(e)

def run_burp_active_scan():
    try:
        burp_handler = RoboBurp2(url_list)
        url_list = list(dict.fromkeys(url_list))
        print(url_list)
        auth_dict = {"username": "betty.ross@we45.com", "password": "secdevops"}
        auth_sequence = '''[
              {
                "name": "Burp Suite Navigation Recorder",
                "version": "1.3.5",
                "eventType": "start"
              },
              {
                "date": "2022-04-17T14:25:21.473Z",
                "timestamp": 1650205521473,
                "eventType": "goto",
                "url": "http://134.209.146.136/login",
                "triggersNavigation": true,
                "fromAddressBar": true
              },
              {
                "date": "2022-04-17T14:25:24.170Z",
                "timestamp": 1650205524170,
                "windowInnerWidth": 1200,
                "windowInnerHeight": 667,
                "uniqueElementID": "49u1ruv2xf7-xs8focsx21g-kd2lg8qy0y",
                "tagName": "INPUT",
                "eventType": "click",
                "placeholder": "email",
                "tagNodeIndex": 1,
                "className": "form-control",
                "name": "email_id",
                "id": "username",
                "textContent": "",
                "innerHTML": "",
                "value": "",
                "elementType": "email",
                "xPath": "/html/body/div/div/section/form/div/input",
                "triggersNavigation": false,
                "triggersWithinDocumentNavigation": false,
                "characterPos": null
              },
              {
                "date": "2022-04-17T14:25:24.695Z",
                "timestamp": 1650205524695,
                "windowInnerWidth": 1200,
                "windowInnerHeight": 667,
                "uniqueElementID": "didg5a6k6gi-p3fxn17cez-9vo309byzzs",
                "tagName": "INPUT",
                "eventType": "typing",
                "placeholder": "email",
                "tagNodeIndex": 1,
                "className": "form-control",
                "name": "email_id",
                "id": "username",
                "textContent": "",
                "innerHTML": "",
                "value": "",
                "elementType": "email",
                "xPath": "/html/body/div/div/section/form/div/input",
                "triggersNavigation": false,
                "triggersWithinDocumentNavigation": false,
                "typedValue": "betty.ross@we45.com"
              },
              {
                "date": "2022-04-17T14:25:30.640Z",
                "timestamp": 1650205530640,
                "eventType": "keyboard",
                "shiftKey": false,
                "ctrlKey": false,
                "altKey": false,
                "key": "Tab",
                "charCode": 0
              },
              {
                "date": "2022-04-17T14:25:31.011Z",
                "timestamp": 1650205531011,
                "windowInnerWidth": 1200,
                "windowInnerHeight": 667,
                "uniqueElementID": "cff7jm1qhcm-69tain6k866-i3zn81deem",
                "tagName": "INPUT",
                "eventType": "typing",
                "placeholder": "password",
                "tagNodeIndex": 2,
                "className": "form-control",
                "name": "password",
                "id": "password",
                "textContent": "",
                "innerHTML": "",
                "value": "",
                "elementType": "password",
                "xPath": "/html/body/div/div/section/form/div[2]/input",
                "triggersNavigation": false,
                "triggersWithinDocumentNavigation": false,
                "typedValue": "secdevops"
              },
              {
                "date": "2022-04-17T14:25:32.717Z",
                "timestamp": 1650205532717,
                "eventType": "keyboard",
                "shiftKey": false,
                "ctrlKey": false,
                "altKey": false,
                "key": "Enter",
                "charCode": 0,
                "causesFormSubmission": true,
                "triggersNavigation": true
              },
              {
                "date": "2022-04-17T14:25:32.906Z",
                "timestamp": 1650205532906,
                "eventType": "userNavigate",
                "url": "http://134.209.146.136/dashboard/"
              }
        ]'''
        scanID = burp_handler.initiate_crawl_and_scan_against_target(auth_logins=auth_sequence,config_name="Audit coverage - thorough")
        #scanID = burp_handler.initiate_scan_against_target(config_name="Audit coverage - thorough")
        print('Start Active scan. Scan ID equals ' + scanID)
        while (burp_handler.get_burp_scan_status_for_id(scanID).get("scan_status") != "succeeded"):
            print('Active Scan progress: ' + burp_handler.get_burp_scan_status_for_id(scanID).get("scan_status"))
            time.sleep(5)
        print('Active Scan completed')
        burp_handler.get_burp_scan_results_for_id(scanID,"CTF2_burp_results.json")
    except Exception as e:
        print("active scan bug",e)

def kill_burp():
    try:
        burp_handler = RoboBurp2(url_list)
        burp_handler.stop_burpsuite()
    except Exception as e:
        print(e)

from selenium import webdriver
from selenium.webdriver.common.proxy import *
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import ElementNotVisibleException,NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import *
import shutil
from selenium.webdriver.firefox.options import Options
options=Options()
options.headless=True

fp = FirefoxProfile()
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png,")
fp.set_preference('startup.homepage_welcome_url', 'about:blank')
fp.set_preference("browser.startup.page", "0")
fp.set_preference("browser.startup.homepage", "about:blank")
fp.set_preference("browser.safebrowsing.malware.enabled", "false")
fp.set_preference("startup.homepage_welcome_url.additional", "about:blank")
#fp.set_preference("network.proxy.type", 1)
#fp.set_preference("network.proxy.http", 'localhost')
#fp.set_preference("network.proxy.http_port", 8080)
#fp.set_preference("network.proxy.ssl", 'localhost')
#fp.set_preference("network.proxy.ssl_port", 8080)
fp.set_preference("network.proxy.no_proxies_on", "*.googleapis.com,*.google.com,*.gstatic.com,*.googleapis.com,*.mozilla.net,*.mozilla.com,ocsp.pki.goog")
fp.update_preferences()

def log_exception(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("[ + ]  Line no :{0} Exception {1}".format(exc_traceback.tb_lineno,e))

def get_driver():
    driver = Firefox(fp,options=options)
    print("Initialized firefox driver")
    driver.maximize_window()    
    driver.implicitly_wait(120)
    return driver

def auth(driver,target):
    try:
        print("[+] Initialized firefox driver")
        driver.maximize_window()
        print("maximized window")
        driver.implicitly_wait(120)
        print("[+] ================ Implicit Wait is Set =================")
        # url = self.target
        driver.get('{0}'.format(target))
        print('[+] ' + driver.current_url)
        driver.implicitly_wait(5)
        # Clicks on 'About'
        try:
            driver.get('{0}/about/'.format(target))
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/appointment/add'.format(target))
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.implicitly_wait(5)
            time.sleep(10)
            # Name
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[1]/div/div/input').clear()
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[1]/div/div/input').send_keys('selenium test')
            driver.implicitly_wait(5)
            # Phone number
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[1]/div/div/input').clear()
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[1]/div/div/input').send_keys('0011223344')
            driver.implicitly_wait(5)
            # Gender
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[1]/div/div/select').click()
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[1]/div/div/select/option[2]').click()
            driver.implicitly_wait(5)
            # Health Plan
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select').click()
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select/option[3]').click()
            driver.implicitly_wait(5)
            # Select Health Plan
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select').click()
            driver.implicitly_wait(10)
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select/option[2]').click()
            driver.implicitly_wait(7)
            # Appointment reason
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[6]/div[1]/div/div/textarea').clear()
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[6]/div[1]/div/div/textarea').send_keys('Selenium Test')
            # Email
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[2]/div/div/input').clear()
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[2]/div/div/input').send_keys('selenium@test.com')
            driver.implicitly_wait(5)
            # Date of Birth
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[2]/div/div/input').clear()
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[2]/div/div/input').send_keys('1989-01-04')
            driver.implicitly_wait(5)
            # Address
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[2]/div/div/textarea').clear()
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[2]/div/div/textarea').send_keys('Selenium Test')
            driver.implicitly_wait(5)
            # Appointment Date
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[5]/div[2]/div/div/input').clear()
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[5]/div[2]/div/div/input').send_keys('2021/01/04')
            driver.implicitly_wait(5)
            # Submit
            driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[7]/div/div/input').click()
            driver.implicitly_wait(5)
            time.sleep(10)
            driver.get('{0}/contact_us/'.format(target))
            print( '[+] ' + driver.current_url)
            time.sleep(10)
        except BaseException as e:
            pass

        try:
            driver.get('{0}/login/'.format(target))
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            time.sleep(10)
            driver.find_element_by_xpath('/html/body/div/div/section/form/div[1]/input').clear()
            driver.find_element_by_xpath('/html/body/div/div/section/form/div[1]/input').send_keys('betty.ross@we45.com')
            driver.find_element_by_xpath('/html/body/div/div/section/form/div[2]/input').clear()
            driver.find_element_by_xpath('/html/body/div/div/section/form/div[2]/input').send_keys('secdevops')
            driver.find_element_by_xpath('/html/body/div/div/section/form/div[3]/button').click()
            time.sleep(10)
            print('[+] ' + driver.current_url)
            driver.implicitly_wait(10)
            time.sleep(10)
            print('[+] ' + driver.current_url)
            driver.implicitly_wait(10)
            time.sleep(10)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/technicians/'.format(target))
            time.sleep(10)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/appointment/plan'.format(target))
            time.sleep(10)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/appointment/doctor'.format(target))
            time.sleep(10)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/secure_tests/'.format(target))
            time.sleep(10)
            # Sends keys and clicks on 'Search'
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
            driver.implicitly_wait(5)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/tests/'.format(target))
            time.sleep(10)
            # Sends keys and clicks on 'Search'
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
            driver.implicitly_wait(5)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/plans/'.format(target))
            time.sleep(10)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
            driver.get('{0}/password_change'.format(target))
            time.sleep(10)
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[1]/div[2]/div/div/input').send_keys('secdevops')
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[2]/div[2]/div/div/input').send_keys('secdevops')
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[3]/button').click()
            driver.implicitly_wait(5)
            print('[+] ' + driver.current_url)
            driver.get('{0}/password_change_secure'.format(target))
            time.sleep(10)
            driver.implicitly_wait(5)
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[1]/div[2]/div/div/input').send_keys('secdevops')
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[2]/div[2]/div/div/input').send_keys('secdevops')
            driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[3]/button').click()
            driver.implicitly_wait(5)
            print('[+] ' + driver.current_url)
            url_list.append(str(driver.current_url))
        except BaseException as e:
            print(e)
    except BaseException as e:
        log_exception(e)


class Wecarescript_walkthrough_burp(object):

    def __init__(self, proxy_host = 'localhost', proxy_port = '8080', target = 'http://134.209.146.136'):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.target = target

    def run_script(self):
        try:
            driver = get_driver()
            driver.maximize_window()
            auth(driver,self.target)
        except BaseException as e:
            print("[ + ] Error !!!!!!!!!!!!",e)


s = Wecarescript_walkthrough_burp()
s.run_script()
run_burp_in_headless_mode()
run_burp_active_scan()
