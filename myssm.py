import paramiko
import yaml
from PyInquirer import prompt, Separator

# Load the YAML file containing the host information
with open('./hosts.yaml', 'r') as f:
    hosts = yaml.safe_load(f)
# Create a list of host groups
host_groups = list(hosts.keys())


# Create a list of host names for each group
host_choices = []
for group, group_hosts in hosts.items():
    host_choices.append(Separator(f'--- {group} ---'))
    host_choices.extend([{'name': host['name']} for host in group_hosts])

# Use PyInquirer to create the interactive menu
host_selection = prompt([{
    'type': 'list',
    'name': 'selected_host',
    'message': 'Select a host:',
    'choices': host_choices
}])

# Get the host information for the selected host
selected_host_name = host_selection['selected_host']
for group, group_hosts in hosts.items():
    for host in group_hosts:
        if host['name'] == selected_host_name:
            host_info = host
            break

#connect to the host
try:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host_info['hostname'], port=host_info['port'], username=host_info['username'])
    while True:
        try:
            cmd = input("$> ")
            if cmd == "exit": break
            stdin, stdout, stderr = client.exec_command(cmd)
            print (stdout.read().decode())
        except KeyboardInterrupt:
            break
    client.close()
except Exception as err:
    print(str(err))