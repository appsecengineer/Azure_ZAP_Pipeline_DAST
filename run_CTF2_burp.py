from RoboBurp2 import *
import time
url_list = "http://134.209.146.136/"
burp_handler = RoboBurp2(url_list)
scanId = ''

def run_burp_in_headless_mode():
    try:
        print("Initiate Burp")
        path = "/burpsuite_pro_v2.0.11beta.jar"
        user_config = "user_options.json"
        project_config = "project.json"
        burp_handler.start_headless_burpsuite(path,user_config=user_config,project_config=project_config)
        sleep(60)
    except Exception as e:
        print(e)

def run_burp_active_scan():
    try:
        auth_dict = {"username": "bruce.banner@we45.com", "password": "secdevops"}
        #scanID = burp_handler.initiate_crawl_and_scan_against_target(auth_logins=auth_dict,config_name="Audit coverage - thorough")
        scanID = burp_handler.initiate_scan_against_target(config_name="Audit coverage - thorough")
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
        burp_handler.stop_burpsuite()
    except Exception as e:
        print(e)

run_burp_in_headless_mode()
run_burp_active_scan()
#kill_burp()
