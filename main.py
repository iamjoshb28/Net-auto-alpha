from netmiko import ConnectHandler

ip_list = ['192.168.1.200','192.168.1.212']
File = open("New_File2.txt", "w")



for ip in ip_list:
    cisco_01 = {
        "device_type": "cisco_ios",
        "host": (ip),
        "username": "cool",
        "password": "guy",
        "secret": "love"  # Enable password
    }

    connection = ConnectHandler(**cisco_01)
    
    output = connection.send_command('show int status')
    print(output + "\n")
    File.write(output + "\n")



print('Closing Connection')
connection.disconnect()