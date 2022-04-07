# coding: utf-8
from RoboZap import *
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
from RoboZapImportScanPolicy import *
zap_handler = RoboZap('127.0.0.1:8090','8090')
context_id = ''
s = RoboZapImportScanPolicy('127.0.0.1:8090','8090')

from selenium.webdriver.firefox.options import Options
options=Options()
options.headless=True

def set_policy():
    s.import_scan_policy()

def run_zap_in_headless_mode():
    try:
        print("Initiate ZAP")
        path = "/ZAP_2.7.0/"
        zap_handler.start_headless_zap(path)
    except Exception as e:
        print(e)

fp = FirefoxProfile()
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "image/png,")
fp.set_preference('startup.homepage_welcome_url', 'about:blank')
fp.set_preference("browser.startup.page", "0")
fp.set_preference("browser.startup.homepage", "about:blank")
fp.set_preference("browser.safebrowsing.malware.enabled", "false")
fp.set_preference("startup.homepage_welcome_url.additional", "about:blank")
fp.set_preference("network.proxy.type", 1)
fp.set_preference("network.proxy.http", 'localhost')
fp.set_preference("network.proxy.http_port", 8090)
fp.set_preference("network.proxy.ssl", 'localhost')
fp.set_preference("network.proxy.ssl_port", 8090)
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
            driver.get('{0}/about'.format(target))
            print('[+] ' + driver.current_url)
            driver.get('{0}/appointment/add'.format(target))
            print('[+] ' + driver.current_url)
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
#             # Select Health Plan
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select').click()
#             driver.implicitly_wait(10)
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[4]/div[1]/div/div/select/option[2]').click()
#             driver.implicitly_wait(7)
#             # Appointment reason
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[6]/div[1]/div/div/textarea').clear()
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[6]/div[1]/div/div/textarea').send_keys('Selenium Test')
#             # Email
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[2]/div/div/input').clear()
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[1]/div[2]/div/div/input').send_keys('selenium@test.com')
#             driver.implicitly_wait(5)
#             # Date of Birth
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[2]/div/div/input').clear()
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[2]/div[2]/div/div/input').send_keys('1989-01-04')
#             driver.implicitly_wait(5)
#             # Address
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[2]/div/div/textarea').clear()
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[3]/div[2]/div/div/textarea').send_keys('Selenium Test')
#             driver.implicitly_wait(5)
#             # Appointment Date
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[5]/div[2]/div/div/input').clear()
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[5]/div[2]/div/div/input').send_keys('2021/01/04')
#             driver.implicitly_wait(5)
#             # Submit
#             driver.find_element_by_xpath('/html/body/div[2]/div/div/form/div[7]/div/div/input').click()
#             driver.implicitly_wait(5)
#             time.sleep(10)
#             driver.get('{0}/contact_us/'.format(target))
#             print( '[+] ' + driver.current_url)
#             time.sleep(10)
        except BaseException as e:
            pass

#         try:
#             driver.get('{0}/login/'.format(target))
#             print('[+] ' + driver.current_url)
#             time.sleep(10)
#             driver.find_element_by_xpath('/html/body/div/div/section/form/div[1]/input').clear()
#             driver.find_element_by_xpath('/html/body/div/div/section/form/div[1]/input').send_keys('bruce.banner@we45.com')
#             driver.find_element_by_xpath('/html/body/div/div/section/form/div[2]/input').clear()
#             driver.find_element_by_xpath('/html/body/div/div/section/form/div[2]/input').send_keys('secdevops')
#             driver.find_element_by_xpath('/html/body/div/div/section/form/div[3]/button').click()
#             time.sleep(10)
#             print('[+] ' + driver.current_url)
#             driver.implicitly_wait(10)
#             time.sleep(10)
#             print('[+] ' + driver.current_url)
#             driver.implicitly_wait(10)
#             time.sleep(10)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/technicians/'.format(target))
#             time.sleep(10)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/appointment/plan'.format(target))
#             time.sleep(10)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/appointment/doctor'.format(target))
#             time.sleep(10)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/secure_tests/'.format(target))
#             time.sleep(10)
#             # Sends keys and clicks on 'Search'
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
#             driver.implicitly_wait(5)
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
#             driver.implicitly_wait(5)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/tests/'.format(target))
#             time.sleep(10)
#             # Sends keys and clicks on 'Search'
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').clear()
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[1]').send_keys('selenium test')
#             driver.implicitly_wait(5)
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/form/div/input[2]').click()
#             driver.implicitly_wait(5)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/plans/'.format(target))
#             time.sleep(10)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/password_change'.format(target))
#             time.sleep(10)
#             driver.implicitly_wait(5)
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[1]/div[2]/div/div/input').send_keys('secdevops')
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[2]/div[2]/div/div/input').send_keys('secdevops')
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[3]/button').click()
#             driver.implicitly_wait(5)
#             print('[+] ' + driver.current_url)
#             driver.get('{0}/password_change_secure'.format(target))
#             time.sleep(10)
#             driver.implicitly_wait(5)
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[1]/div[2]/div/div/input').send_keys('secdevops')
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[2]/div[2]/div/div/input').send_keys('secdevops')
#             driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[3]/button').click()
#             driver.implicitly_wait(5)
#             print('[+] ' + driver.current_url)
#         except BaseException as e:
#             print(e)
    except BaseException as e:
        log_exception(e)





class Wecarescript_walkthrough(object):

    def __init__(self, proxy_host = 'localhost', proxy_port = '8090', target = 'http://134.209.146.136'):
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

def context_zap_results():
    try:
        context_id = zap_handler.zap_define_context("CTF_CONTEXT","http://134.209.146.136")
    except Exception as e:
        print(e)

def run_zap_active_scan():
    try:
        s = RoboZapImportScanPolicy('127.0.0.1:8090','8090')
        scanId = zap_handler.zap_start_ascan(context_id,'http://134.209.146.136','Default Policy')
        print('Start Active scan. Scan ID equals ' + scanId)
        while (int(s.get_scan_status(scanId)) < 100):
            print('Active Scan progress: ' + s.get_scan_status(scanId) + '%')
            time.sleep(5)
        print('Active Scan completed')
        export_zap_report_of_scan()
        #get_html_report()
    except Exception as e:
        print(e)

def export_zap_report_of_scan():
    try:
        zap_handler.zap_export_report("/zap_results/CTF_walkthrough_zap_scan_result.xml","xml","CTF_walkthrough_zap_scan_result.xml","Vishnuwe45")
        zap_handler.zap_export_report("/zap_results/CTF_walkthrough_zap_scan_result.json","json","CTF_walkthrough_zap_scan_result.json","Vishnuwe45")
    except Exception as e:
        print(e)

def get_html_report():
    try:
        s = RoboZapImportScanPolicy('127.0.0.1:8090','8090')
        s.import_html_report("CTF_walkthrough_zap_scan_result.html")
    except Exception as e:
        print(e)

def kill_zap():
    try:
        zap_handler.shutdown()
    except Exception as e:
        print(e)

run_zap_in_headless_mode()
# set_policy()
s = Wecarescript_walkthrough()
s.run_script()
context_zap_results()
run_zap_active_scan()
