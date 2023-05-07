from netmiko import ConnectHandler
# ip_list = ['192.168.1.200','192.168.1.212']
File = open("Run_Output.txt", "w") # Declares File variable to written to later

ip_list = [ip.strip() for ip in open("IPS.txt", 'r')] # Reads data from .txt file line by line and adds to list

for ip in ip_list: # for loop that runs for each ip in list
    cisco_01 = { # privledged connection info for netmiko
        "device_type": "cisco_ios",
        "host": (ip),
        "username": "admin",
        "password": "root",
        "secret": "love"  # Enable password
    }

    connection = ConnectHandler(**cisco_01) # Calls connection SSH connection using Netmiko
    connection.enable() # Enable method

    which_prompt = connection.find_prompt() # Find prompt method
    print(which_prompt) # Print the prompt

    output = connection.send_command('show run') # Send command
    print(output) # Prints output to viewing screen
    File.write(output) # writes output to file variable declared earlier

print('Closing Connection')
connection.disconnect()
