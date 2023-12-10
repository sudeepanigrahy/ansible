# The python script will have to be executed from cli, and
# the switch and cli_command will have to be passed, in that order,
# inside of double-quotes, from the cli itself, an example is:
# >python findswitchinfo_adhoc.py "10.x.x.x" "sh ip int br" 

import sys
import time
from netmiko import ConnectHandler

def switch_info_finder(connection, switch, command):

    connection.send_command(command_string="sudo -i",
                       expect_string='#',
                       strip_prompt=False,
                       strip_command=False)
    time.sleep(300/1000)

    connection.send_command(command_string=f"echo {switch} > hosts1",
                            expect_string='#',
                            strip_prompt=False,
                            strip_command=False)
    #time.sleep(300/1000)

    ansible_command = f'ansible -i /root/hosts1 {switch} -m raw -a "{command}" -u ******** -k'

    output = connection.send_command_timing(command_string=ansible_command,
    strip_prompt=False,
    strip_command=False)

    output += connection.send_command_timing(command_string=r"***password*****",                              
    strip_prompt=False,
    strip_command=False)

    print(output)
    connection.disconnect()



if __name__=="__main__":
    args = sys.argv

    kwargs = {
        'device_type': 'linux',
        'ip': '10.x.x.x',
        'username': '*******',
        'password': '*******',
        'port': 22,
        'verbose':True
        }

    connection = ConnectHandler(**kwargs)
    switch_info_finder(connection, args[1], args[2])

