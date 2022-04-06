import os
from zapv2 import ZAPv2 as ZAP
import time
import subprocess
from robot.api import logger
import base64
import uuid
import json
import requests
from datetime import datetime
import six
import sys

reload(sys)
sys.setdefaultencoding('UTF8')


class RoboZapImportScanPolicy(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, proxy, port):
        '''
        ZAP Library can be imported with one argument
        Arguments:
            - ``proxy``: Proxy is required to initialize the ZAP Proxy at that location. This MUST include the port specification as well
            - ``port``: This is a portspecification that will be used across the suite
        Examples:
        | = Keyword Definition =  | = Description =  |
        | Library `|` RoboZap  | proxy | port |
        '''
        self.zap = ZAP(proxies={'http': proxy, 'https': proxy})
        self.port = port

    def start_headless_zap(self, path):
        """
        Start OWASP ZAP without a GUI
        Examples:
        | start gui zap  | path | port |
        """
        try:
            cmd = path + 'zap.sh -daemon -config api.disablekey=true -port {0}'.format(self.port)
            print(cmd)
            subprocess.Popen(cmd.split(' '), stdout=open(os.devnull, 'w'))
            time.sleep(10)
        except IOError as e:
        	print(e)
        	print('ZAP Path is not configured correctly')


    def import_scan_policy(self,policy_file):
    	try:
            self.zap.ascan.add_scan_policy(policy_file)
            print("scan policy imported")
    	except Exception as e:
    		print(e)

    def exclude_context_urls(self,context_name,exluded_urls):
        try:
            for url in exluded_urls:
                self.zap.context.exclude_from_context(context_name,url)
        except Exception as e:
            print(e)

    def set_context_to_scope(self,context_name):
        try:
            self.zap.context.set_context_in_scope(context_name,True)
        except Exception as e:
            raise e

    def context_exclude_technology(self,context_name,exclude_tech):
        try:
            for tech in exclude_tech:
                self.zap.context.exclude_context_technologies(context_name,tech)
        except Exception as e:
            raise e

    def context_include_technology(self,context_name,include_tech):
        try:
            for tech in include_tech:
                self.zap.context.include_context_technologies(context_name,tech)
        except Exception as e:
            raise e

    def import_html_report(self,file_name):
        try:
            f1=open('/zap_results/{0}'.format(file_name), 'w+')
            f1.write(self.zap.core.htmlreport())
            f1.close()
            print("html report generated")
        except Exception as e:
            print(e)

    def get_scan_status(self,scan_id):
        try:
            return self.zap.ascan.status(scan_id)
        except Exception as e:
            raise e
