import paramiko
import mytools
import sys
import time
import yaml

with open("network.yaml") as f:
 network=yaml.safe_load(f)


username_tacacs,password_tacacs = mytools.get_credentials()
for pop in network:
    print('Processing', pop)
    number_of_devices = len(network[pop])

    id_device=0
    while id_device < number_of_devices:
        print('Number of devices',number_of_devices)
        print('index device',id_device)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        authentication_expections = (paramiko.ssh_exception.SSHException, paramiko.ssh_exception.BadAuthenticationType,paramiko.ssh_exception.AuthenticationException)
        print("Connecting to device:",network[pop][id_device]["id"])

        try:
    #        print('Authent 1')
    #        client.connect(network[pop][id_device]["id"], username=username_tacacs, password=password_tacacs)
    #    except authentication_expections as e:
            print('Authent 2')
            client.connect(network[pop][id_device]["id"], username='admin', password='arista')
        except authentication_expections as e:
            print('Authent 3')
            client.connect(network[pop][id_device]["id"], username='admin', password='admin')
        except:
            print('Other Exception')

        number_of_cmd = len(network[pop][id_device]) - 1
        print('number of command:', number_of_cmd)

        cmd_id = 1

        output=""

        chan=client.invoke_shell()

        while cmd_id <= number_of_cmd:
            print("Command id:", cmd_id)
            cmd = "cmd"+str(cmd_id)
            print('Command is: ', network[pop][id_device][cmd] )
            chan.send(network[pop][id_device][cmd]+"\n")
            time.sleep(1)
            output += chan.recv(65535)
            print(output)


            cmd_id+=1

        chan.close()
        client.close()
        id_device+=1
