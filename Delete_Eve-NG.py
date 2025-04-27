import requests
import json

def delete_instance(*args):
    login_url = 'http://192.168.138.133/api/auth/login'
    cred = '{"username":"admin","password":"eve"}'
    headers = {'Accept':'application/json'}

    login = requests.post(url=login_url, data=cred)
    cookies = login.cookies
    print(cookies)
    for instance_id in args:
        delete_url = f'http://192.168.138.133/api/labs/first.unl/nodes/{instance_id}'
        delete_api = requests.delete(url=delete_url,cookies=cookies,headers=headers)
        response = delete_api.json()
        output = response['status']
        print(f'Delete Status:{output}')


ids = input("Please enter the ID's of the instance you would like deleted: ").split(',')
delete_instance(*ids) 