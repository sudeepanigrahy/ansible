# This is the ansible base file for interfacing with the
# ansible linux box we have using netmiko, specially when we just wanna
# execute an ansible command which wont ask us a password when we 
# execute it, and will just give us the output.

from netmiko import ConnectHandler

kwargs = {
        'device_type': 'linux',
        'ip': '10.70.85.211',
        'username': 'spanigrahy',
        'password': 'Sueme@0128',
        'port': 22,
        'verbose':True
        }

connection = ConnectHandler(**kwargs)

# When the ssh connection with the ansible box is first established,
# the prompt is actually the bash prompt, hence we first need to become the root
# user by doing the 'sudo -i'( actually ansible commands run from the bash too,
# but its better to run them as root, as i've set it up to be used from the root)
connection.send_command(command_string="sudo -i",
                       expect_string='#',
                       strip_prompt=False,
                       strip_command=False)

output = connection.send_command("ansible localhost -m ping")

print(output)
