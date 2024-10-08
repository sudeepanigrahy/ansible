# This is the ansible base file that shows how to interface
# with the Ansible linux box that we have using netmiko, specially when we wanna
# execute an ad-hoc/playbook command which then also requires a password to be sent 
import sys
import time
from netmiko import ConnectHandler
#import logging
#logging.basicConfig(filename='test2.log', level=logging.DEBUG)
#logger = logging.getLogger("netmiko")

kwargs = {
        'device_type': 'linux',
        'ip': '******',
        'username': '*******',
        'password': '*******',
        'port': 22,
        'verbose':True
        }

connection = ConnectHandler(**kwargs)

# When the ssh connection with the ansible box is first established,
# the prompt is actually the bash prompt, hence we first need to become the root
# user by doing the 'sudo -i'.
connection.send_command(command_string="sudo -i",
                       expect_string='#',
                       strip_prompt=False,
                       strip_command=False)


command = "ansible-playbook -i /root/hosts getmac.yml -u ***username**** -k | grep -v 'Gi1/1/1\|CPU\|Te1/1/3\|Te1/0/1'"
#command = 'ansible ******switchname******* -m raw -a "show version | i uptime" -u ******** -k'
#command = 'ansible ******** -m raw -a "show version | i uptime" -u ******** -k'
#

# This 'send_command_timing()' method from netmiko is used when
# we have to execute multiple commands one after the other on a switch's/server's cli

#output = connection.send_multiline_timing(['ansible ***switchname****** -m raw -a "show version | i uptime" -u ******* -k', '****password****'])
try:
    output = connection.send_command_timing(command_string="cd playbooks",
        strip_prompt=True,
        strip_command=True)

    output = connection.send_command_timing(command_string=command,
        strip_prompt=True,
        strip_command=True)

    output += connection.send_command_timing(command_string=r"****password*****",                              
        strip_prompt=True,
        strip_command=True)
except:
    print(sys.exc_info()[0])

print(output)
connection.disconnect()

