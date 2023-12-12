# This is the ansible base file for interfacing with the
# ansible box that we have using paramiko

import paramiko
import time

ssh_client=paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

kwargs = { 
        'hostname':'******',
        'port':'22',
        'username':'*********',
        'password':'********'
          }

ssh_client.connect(**kwargs, look_for_keys=False, allow_agent=False)
if ssh_client.get_transport().is_active()==True: print(f"SSH Connection to {kwargs['hostname']} is Established...")
shell=ssh_client.invoke_shell()

shell.send('sudo -i\n')
time.sleep(1)
shell.send('ansible localhost -m ping\n')
time.sleep(1)
output=shell.recv(10000)
output=output.decode('utf-8')
print(output)

ssh_client.close()
