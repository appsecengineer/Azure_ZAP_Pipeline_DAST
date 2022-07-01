import os
from zapv2 import ZAPv2 as ZAP
import time
import subprocess
import base64
import uuid
import json
import requests
from datetime import datetime


class OwaspZAP(object):
    def __init__(self, proxy_host='localhost', proxy_port='8090'):
        print('in class')
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.zap = ZAP(proxies={
            "http": "http://{0}:{1}".format(self.proxy_host, self.proxy_port), 
            "https": "http://{0}:{1}".format(self.proxy_host, self.proxy_port)}
            )

    def start_headless_zap(self, zap_path, proxy_port):
        try:
            cmd = "{0}/zap.sh -daemon -config api.disablekey=true -port {1}".format(zap_path, proxy_port)
            print(cmd)
            subprocess.Popen(cmd.split(" "), stdout=open(os.devnull, "w"))
            time.sleep(10)
        except IOError:
            print("ZAP Path is not configured correctly")

    def zap_open_url(self, url):
        self.zap.urlopen(url)
        time.sleep(4)

    def zap_define_context(self, contextname, url):
        regex = "{0}.*".format(url)
        context_id = self.zap.context.new_context(contextname=contextname)
        time.sleep(1)
        self.zap.context.include_in_context(contextname, regex=regex)
        time.sleep(5)
        return context_id

    def zap_start_spider(self, contextname, url):
        try:
            spider_id = self.zap.spider.scan(url=url, contextname=contextname)
            time.sleep(2)
            return spider_id
        except Exception as e:
            print((e.message))

    def zap_spider_status(self, spider_id):
        while int(self.zap.spider.status(spider_id)) < 100:
            print("Spider running at {0}%".format(int(self.zap.spider.status(spider_id))))
            time.sleep(10)
        print("Spider Completed!")
        print(self.zap.core.urls())

    def zap_start_ascan(self, context, url, policy="Default Policy"):
        try:
            scan_id = self.zap.ascan.scan(contextid=context, url=url, scanpolicyname=policy)
            time.sleep(2)
            return scan_id
        except Exception as e:
            print(e.message)

    def zap_scan_status(self, scan_id):
        while int(self.zap.ascan.status(scan_id)) < 100:
            print("Scan running at {0}%".format(int(self.zap.ascan.status(scan_id))))
            time.sleep(10)
        print('Active Scan Complete!')
        print(self.zap.core.alerts())

    def zap_export_html_report(self, export_file):
        f1 = open('{0}'.format(export_file), 'w+')
        f1.write(self.zap.core.htmlreport())
        f1.close()
        print("HTML REPORT GENERATED")
    
    def zap_export_xml_report(self, export_file):
        f1 = open('{0}'.format(export_file), 'w+')
        f1.write(self.zap.core.xmlreport())
        f1.close()
        print("XML REPORT GENERATED")
        
    def zap_export_json_report(self, export_file):
        f1 = open('{0}'.format(export_file), 'w+')
        f1.write(self.zap.core.jsonreport())
        f1.close()
        print("JSON REPORT GENERATED")

    def zap_shutdown(self):
        self.zap.core.shutdown()
