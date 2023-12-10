# The python script will have to be executed from cli, and
# the switch and cli_command will have to be passed, in that order,
# inside of double-quotes, from the cli itself, two examples are:
# >python .\findswitchinfo_raw_playbook.py "sg209-b1rm5x-as6-cn240.sing.micron.com" "sh ip int br" "| additional grepping if you'd like"
# >python .\findswitchinfo_raw_playbook.py "sg209-b1rm5x-as6-cn240.sing.micron.com" "get mac address-table" "| grep -v 'CPU\|Gi1/1/1'"
import sys
import time
from netmiko import ConnectHandler
import logging
logging.basicConfig(filename='test.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

def switch_info_finder(connection, switch, command, grepping):

    connection.send_command(command_string="sudo -i",
                       expect_string='#',
                       strip_prompt=False,
                       strip_command=False)
    time.sleep(200/1000)

    connection.send_command(command_string=f"echo {switch} > hosts1",
                            expect_string='#',
                            strip_prompt=False,
                            strip_command=False)
    #time.sleep(100/1000)

    if command=="sh ip int br":
        ansible_command = f"ansible-playbook -i /root/hosts1 shipintbr_raw.yml -u spanigrahy -k  {grepping}"
    elif command=="sh ver" or command=="sh version":
        ansible_command = f"ansible-playbook -i /root/hosts1 shver_raw.yml -u spanigrahy -k  {grepping}"
    elif command=="sh int status":
        ansible_command = f"ansible-playbook -i /root/hosts1 shintstatus_raw.yml -u spanigrahy -k  {grepping}"
    elif 'mac' in command or 'address-table' in command:
        ansible_command = f"ansible-playbook -i /root/hosts1 getmac_raw.yml -u spanigrahy -k  {grepping}"
    elif 'cdp' in command or 'nei' in command or 'neighbors' in command or 'neighbor' in command:
        ansible_command = f"ansible-playbook -i /root/hosts1 shcdpnei_raw.yml -u spanigrahy -k  {grepping}"
    else: print("Type the command clearly..")

    print(f"\nExecuting on Ansible: {ansible_command}\n")


    try:
        output = connection.send_command_timing(command_string="cd playbooks/",
        strip_prompt=True,
        strip_command=True)

        output = connection.send_command_timing(command_string=ansible_command,
        strip_prompt=True,
        strip_command=True)

        output += connection.send_command_timing(command_string=r"Sueme@0128",                              
        strip_prompt=True,
        strip_command=True)
    except:
        print(f"Error Encountered: {sys.exc_info()[0]}")

    print(output)

if __name__=="__main__":
    args = sys.argv

    kwargs = {
        'device_type': 'linux',
        'ip': '10.70.85.211',
        'username': 'spanigrahy',
        'password': 'Sueme@0128',
        'port': 22,
        'verbose':True
        }

    connection = ConnectHandler(**kwargs)
    switch_info_finder(connection, args[1], args[2], args[3])
