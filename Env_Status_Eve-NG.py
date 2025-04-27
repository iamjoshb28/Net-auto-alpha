import requests
import json

login_url = 'http://192.168.138.133/api/auth/login'
cred = '{"username":"admin","password":"eve"}'
headers = {'Accept':'application/json'}

login = requests.post(url=login_url, data=cred)
cookies = login.cookies
print(cookies)

status_url = 'http://192.168.138.133/api/status'

status_api =requests.get(url=status_url,cookies=cookies,headers=headers)
response = status_api.json()
disk_usage = response['data']['disk']
cpu_usage = response['data']['cpu']
mem_usage = response['data']["mem"]
print(f"Disk Usage:{disk_usage}\nCPU Usage:{cpu_usage}\nMemory Usage:{mem_usage}")