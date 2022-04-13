# coding: utf-8
import json
from os import path
from datetime import datetime
from base64 import b64decode, b64encode
import sys
import os
import inspect

sev_dict = {
	"info": 0,
	"low":1,
	"medium":2,
	"high":3
}
burp_confidence_dict = {
    "Certain":3,
    "Firm":2,
    "Tentative":1,
}
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'burp_db.json')
result_file_path = os.path.join(script_dir, 'CTF2_burp_results.json')
cwe_dict = json.load(open(file_path,'r'))

def log_exception(e):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("[ + ]  Line no :{0} Exception {1}").format(exc_traceback.tb_lineno,e)

def parse_burp_json(json_file):
	"""
		parses the json file obtained by burp scanner and pushes the result
		to results to DB
	"""
	try:
		print("Burp json parsing initiated")
		total_vul_dict = []
		current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		with open(json_file) as fp:
			datafile = json.load(fp)
			vul_dict = {}
			unique_name_mutiple_evid = []
			for root_key in datafile:
				results = root_key.get('issue',[])
				set_names = set(unique_name_mutiple_evid)
				check_name_exists = results.get('name') in set_names
				evids = []
				cwe_present = cwe_dict.get(str(results.get('type_index')),'8389632')
				cwe = 0
				if cwe_present:
					cwe = int(cwe_present[0])
				if not check_name_exists:
					unique_name_mutiple_evid.append(results.get('name'))
					request_data = ''
					response_data = ''
					url = ''
					for vul_name_all_json in datafile:
						results_name = vul_name_all_json.get('issue',[])
						name = results.get('name',  '')
						if name == results_name.get('name',  ''):
							for request_response in results_name.get('evidence', ''):
								if request_response.get('request_response'):
									for key, value in request_response.get('request_response').items():
										if key == 'url':
											url = value
										if key == 'request':
											for request_info in value:
												data_request = request_info.get('data')
												if data_request is not None:
													decoded_data = str(b64decode(data_request))
													request_data += decoded_data
										if key == 'response':
											for response_info in value:
												data_response = response_info.get('data')
												if data_response is not None :
													decoded_data = str(b64decode(data_response))
													response_data += decoded_data
					evids.append({
							'url':url,
		                    'name':results.get('path', ''),
                                    'request':str(b64encode(request_data.encode('utf-8'))),
                                    'response': b64encode(response_data)
						})
					vul_dict = {
						'name':results.get('name',  ''),
						'is_false_positive':False,
						'is_remediated':False,
						'is_deleted':False,
						'confidence':burp_confidence_dict.get(results.get('confidence'), 3),
						'severity':sev_dict.get(results.get('severity'), 3),
						'description':results.get('description', ''),
						'vul_type':'Insecure Coding',
						'remediation':results.get('remediation', ''),
						'observations':'',
						'created_on':current_date,
					}
					vul_dict['evidences'] = evids
					vul_dict['cwe'] = cwe
					total_vul_dict.append(vul_dict)
			vuls = {
				"tool": "Burp",
				"vulnerabilities": total_vul_dict
			}
			with open('orchy_json_burp_results.json', 'w') as fp:
				json.dump(vuls,fp)
	except BaseException as e:
		log_exception(e)
	else:
		print('BURP JSON Parsing Completed')

parse_burp_json(result_file_path)
