# This is the ansible base file for interfacing with the
# ansible box that we have using paramiko, when we wanna execute 
# a command on a server's cli thats gonna ask for a passsword
# This is not working..need to figure out why...

import paramiko
import time

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

kwargs = { 
        'hostname':'10.x.x.x',
        'port':'22',
        'username':'*********',
        'password':'********'
          }

ssh_client.connect(**kwargs, look_for_keys=False, allow_agent=False)
if ssh_client.get_transport().is_active()==True: print(f"SSH Connection to {kwargs['hostname']} is Established...")

"""
shell=ssh_client.invoke_shell()

shell.send('sudo -i\n')
time.sleep(1)
shell.send("ansible 10.x.x.x -m raw -a 'show version | i uptime' -u ****** -k\n")
time.sleep(1)
shell.send('********\n')
time.sleep(1)
output=shell.recv(20000)
output=output.decode('utf-8')
print(output)
"""
stdin, stdout, stderr = ssh_client.exec_command("sudo -i\n")
stdin, stdout, stderr = ssh_client.exec_command("ansible 10.x.x.x -m raw -a 'show version | i uptime' -u ********* -k\n")
stdin.write("*******\n")
time.sleep(2)

output = stdout.read()
#output = output.decode()
print(output)

ssh_client.close()
