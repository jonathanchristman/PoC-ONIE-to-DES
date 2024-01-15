# Source Code for the Project

The code is in this section is broken up in distinct pieces, as each component may or may not be needed in an a delpoyment scenario. The inidivual pieces can be chained together to provide a full solution that converts an Dell switch running OS10 to SONiC.

These components are specifically for converting a Dell OS10 switch to SONiC, but could be adapted as needed for converting another ONIE-capable switch to SONiC:

1. A simple scipt that will parse csv inventory file to generate an inventory file for the script to interact with hosts, a DHCP config file that will be used to initialize new switches, and an ansible hosts file for post-processing.
2. A scipt that connects to an OS10 switch and ONIE uninstalls the OS, preparing it for installation of a new NOS.
3. A docker compose yml file for loading optionally: a DHCP and/or HTTP server that are used for the switch boot and image transfer process.
4. A script for checking on the status of the installations
5. A simple ansible playbook example for checking the SONiC version