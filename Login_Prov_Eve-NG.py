import requests
import json
import re
import time
from pprint import pprint
from telnetlib import Telnet

def create_instance(instance_name):
    login_url = 'http://192.168.138.133/api/auth/login'
    cred = '{"username":"admin","password":"eve","html5": "-1"}'
    headers = {'Accept':'application/json'}

    login = requests.post(url=login_url, data=cred)
    cookies = login.cookies
    print(cookies)
    

    ios_data = {"template":"iol","type":"iol","count":"1","image":"L2-ADVENTERPRISE-M-15.1-20140814.bin","name":f"SW_{instance_name}","icon":"Switch.png","nvram":"1024","ram":"1024","ethernet":"1","serial":"0","config":"0","delay":"0","left":"610","top":"215","postfix":0}

    ios_data = json.dumps(ios_data)

    create_url = 'http://192.168.138.133/api/labs/first.unl/nodes'

    create_api = requests.post(url=create_url,data=ios_data,cookies=cookies,headers=headers)
    response =create_api.json()
    print(response)
    device_id = response['data']['id']
    print(f"Created Instance ID is: {device_id}")

    ######## Management Interface Creation

    print(f"Connecting Management Interface")
    mgmt_int_url = f"http://192.168.138.133/api/labs/first.unl/nodes/{device_id}/interfaces"
    int_data = '{"0":"2"}'
    connect_api = requests.put(url=mgmt_int_url,data=int_data,cookies=cookies,headers=headers)
    print(connect_api.json())

    ######## Starting Instance(s)

    print(f'Booting Instance: {device_id}')
    boot_url = f"http://192.168.138.133/api/labs/first.unl/nodes/{device_id}/start"
    boot_api = requests.get(url=boot_url,cookies=cookies,headers=headers)
    print(boot_api.json())

    ######### Get Telnet Port

    node_info_url = f"http://192.168.138.133/api/labs/first.unl/nodes"
    node_info_api = requests.get(url=node_info_url,cookies=cookies,headers=headers)
    data = node_info_api.json()
    node_dict = data['data']
    port_details = node_dict[f"{device_id}"]['url']
    # Print port details
    port_pattern = re.compile(r'telnet.+:(\d+)')
    port_output = int((port_pattern.search(port_details).group(1)))
    print(node_info_api)
    return port_output

def telnet_init(telnet_port):
    TELNET_TIMEOUT = 10
    tn = Telnet(host='192.168.138.133',port=telnet_port,timeout=TELNET_TIMEOUT)


def device_conf(device_name,telnet_port):
    TELNET_TIMEOUT = 10
    tn = Telnet(host='192.168.138.133',port=telnet_port,timeout=TELNET_TIMEOUT)
    with open(f"{device_name}.conf", 'r') as cmd_file:
        for cmd in cmd_file.readlines():
            cmd = cmd.strip('\r\n')
            tn.write(cmd.encode()+ b'\r')
            time.sleep(1)



def provision(device_name):
    telnet_port = create_instance(device_name)
    print(f"Telent Port: {telnet_port}")
    print("Intiating sleep for 15s")
    time.sleep(15)
    print("Finished Sleep")
    telnet_init(telnet_port)
    print("Initialization Finshed")
    device_conf(device_name, telnet_port)
    print("Finished with device setup")

provision('L2-SW')
