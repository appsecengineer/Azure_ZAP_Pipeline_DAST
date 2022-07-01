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

    def zap_export_report(self, export_file, export_format, report_title, report_author,proxy_host='localhost',proxy_port='8090'):
        

        url = "http://{0}:{1}/JSON/exportreport/action/generate/".format(proxy_host,proxy_port)
        export_path = export_file
        extension = export_format
        report_time = datetime.now().strftime("%I:%M%p on %B %d, %Y")
        source_info = "{0};{1};ZAP Team;{2};{3};v1;v1;{4}".format(
            report_title, report_author, report_time, report_time, report_title
        )
        alert_severity = "t;t;t;t"
        alert_details = "t;t;t;t;t;t;t;t;t;t"
        data = {
            "absolutePath": export_path,
            "fileExtension": extension,
            "sourceDetails": source_info,
            "alertSeverity": alert_severity,
            "alertDetails": alert_details,
        }

        r = requests.post(url, data=data)
        if r.status_code == 200:
            pass
        else:
            raise Exception("Unable to generate report")

    def zap_shutdown(self):
        self.zap.core.shutdown()
