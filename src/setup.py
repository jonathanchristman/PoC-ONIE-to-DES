import csv
from jinja2 import Template

def csv_to_dhcp_config(csv_file, config_file):
    with open('variable_file.txt', 'r') as f, open(csv_file, newline='') as csvfile, open(config_file, 'w') as conf:
        for line in f:
            if 'ENABLE_DHCP' in line:
                enable_dhcp = line.split('=')[1].strip()
            elif 'DHCP_SRV_IP' in line:
                dhcp_srv_ip = line.split('=')[1].strip()
            elif 'HTTP_SRV_IP' in line:
                http_srv_ip = line.split('=')[1].strip()
            elif 'DHCP_SUBNET' in line:
                dhcp_subnet = line.split('=')[1].strip()
            elif 'DHCP_MASK' in line:
                dhcp_subnet_mask = line.split('=')[1].strip()
            elif 'DEF_GATEWAY' in line:
                routers = line.split('=')[1].strip()
            elif 'NOS_IMAGE' in line:
                nos_image = line.split('=')[1].strip()
                
        conf.write("ddns-update-style interim;\n")
        conf.write("option ztp_json_url code 67 = text;\n\n")
        conf.write("max-lease-time 86400;\n")
        conf.write("min-lease-time 60;\n")
        conf.write("default-lease-time 86400;\n")
        conf.write("option netbios-node-type 8;\n\n")
        
        if 'dhcp_subnet' in locals() and 'dhcp_subnet_mask' in locals():
            conf.write(f"subnet {dhcp_subnet} netmask {dhcp_subnet_mask} {{\n")
            conf.write(f"option subnet-mask  {dhcp_subnet_mask};\n\n")
        if 'routers' in locals():    
            conf.write(f"option routers  {routers};\n\n")    
        reader = csv.reader(csvfile)
        for row in reader:
            if not row[0].startswith('#'):
                if len(row) != 3:
                    continue  # Skip rows with incorrect number of columns

                mac, ip, hostname = row
                conf.write(f"host {hostname} {{\n")
                conf.write(f"    hardware ethernet {mac};\n")
                conf.write(f"    fixed-address {ip};\n")
                if 'http_srv_ip' in locals():   
                    conf.write(f"    option ztp_json_url \"http://{http_srv_ip}/ztp_data.json;\n")
                conf.write("}\n\n")
        conf.write("}\n")
    if 'nos_image' in locals() and 'http_srv_ip' in locals():
        with open('ztp_data.j2', 'r') as f:
            template = Template(f.read())

        # Render the template with the IP address and image name
        rendered = template.render(ip_address='192.168.1.100', image_name='Enterprise_SONiC_OS_4.1.0_Enterprise_Premium')

        # Write the rendered template to a file
        with open('ztp_data.json', 'w') as f:
            f.write(rendered)


# Main
csv_to_dhcp_config('input.csv', 'dhcpd.conf')
