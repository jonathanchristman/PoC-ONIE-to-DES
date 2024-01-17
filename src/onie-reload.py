import paramiko
import time

def ssh_command(ip, port, username, password, command):
    try:
        # Create SSH client
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the switch
        ssh_client.connect(hostname=ip, port=port, username=username, password=password)

        # Get the shell
        ssh_shell = ssh_client.invoke_shell()
        time.sleep(1)

        # Send the command
        ssh_shell.send(command + "\n")
        time.sleep(2)

        # Send the confirmation 'yes'
        ssh_shell.send("yes\n")
        time.sleep(2)

        # Receive data
        output = ssh_shell.recv(65535).decode('utf-8')
        print(output)

        # Close the connection
        ssh_client.close()

    except Exception as e:
        print(f"Connection failed: {e}")

def read_ip_addresses(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error reading IP addresses from file: {e}")
        return []
    
# Switch credentials and details
ip_address = '192.168.1.105' # replace with your switch's IP address
file_path = 'ip_addresses.txt'
port = 22
username = 'admin'
password = 'admin'
command = 'reload onie uninstall'

# Run the command
# Read IP addresses from file
ip_addresses = read_ip_addresses(file_path)

if not ip_addresses:
    print("No IP addresses to process.")
else:
    for ip_address in ip_addresses:
        print(f"Connecting to {ip_address}")
        ssh_command(ip_address, port, username, password, command)


