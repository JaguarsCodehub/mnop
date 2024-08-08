Here's a step-by-step guide to complete your practical on securing the management plane on the routers (R1, R2, R3):

Step 1: Configure Loopbacks and Assign Addresses

R1 Configuration:

R1 Console
hostname R1
int lo0
description R1 LAN
ip address 192.168.1.1 255.255.255.0
exit
int s1/0
description R1 --> R2
ip address 10.1.1.1 255.255.255.252
clock rate 128000
no shutdown
exit

R2 Configuration:

R2 Console
hostname R2
int s1/0
description R2 --> R1
ip address 10.1.1.2 255.255.255.252
no shutdown
exit
int s1/1
description R2 --> R3
ip address 10.2.2.1 255.255.255.252
clock rate 128000
no shutdown
exit

R3 Configuration:

R3 Console
hostname R3
int lo0
description R3 LAN
ip address 192.168.3.1 255.255.255.0
exit
int s1/1
description R3 --> R2
ip address 10.2.2.2 255.255.255.252
no shutdown
exit

Step 2: Configure Static Routes

R1 Static Route:

R1 Console
ip route 0.0.0.0 0.0.0.0 10.1.1.2

R3 Static Route:

R3 Console
ip route 0.0.0.0 0.0.0.0 10.2.2.1

R2 Static Routes:

R2 Console
ip route 192.168.1.0 255.255.255.0 10.1.1.1
ip route 192.168.3.0 255.255.255.0 10.2.2.2

R1 Verification (Tcl Script):

R1 Console
tclsh
foreach address {
    192.168.1.1
    10.1.1.1
    10.1.1.2
    10.2.2.1
    10.2.2.2
    192.168.3.1
} { ping $address }

Step 3: Secure Management Access

Set Minimum Password Length (R1):

R1 Console
security passwords min-length 10

Configure Enable Secret Password (R1):

enable secret class12345

Configure Console Password and Settings (R1):

line console 0
password ciscoconpass
exec-timeout 5 0
login
logging synchronous
exit

Configure VTY Line Password (R1):

line vty 0 4
password ciscovtypass
exec-timeout 5 0
login
exit

Disable AUX Port (R1):

line aux 0
no exec
end

Encrypt Passwords (R1):

service password-encryption

Configure MOTD Banner (R1):

banner motd $Unauthorized access strictly prohibited!$
exit

Repeat steps 3a through 3k on R3.

Step 4: Configure Enhanced Username Password Security

Create Local Database Entries (R1):

username JR-ADMIN secret class12345
username ADMIN secret class54321

Set Console Line to Use Local Database (R1):

line console 0
login local
exit

Set VTY Lines to Use Local Database (R1):

line vty 0 4
login local
end

Repeat steps 4a to 4c on R3.

Verify by Telnetting from R1 to R3:

R1 Console
telnet 10.2.2.2

Step 5: Enable AAA RADIUS Authentication with Local User for Backup

Enable AAA on R1:
aaa new-model

Configure RADIUS Server 1 (R1):

radius server RADIUS-1
address ipv4 192.168.1.101
key RADIUS-1-pa55w0rd
exit

Configure RADIUS Server 2 (R1):

radius server RADIUS-2
address ipv4 192.168.1.102
key RADIUS-2-pa55w0rd
exit

Assign RADIUS Servers to Group (R1):

aaa group server radius RADIUS-GROUP
server name RADIUS-1
server name RADIUS-2
exit

Enable Default AAA Authentication (R1):

aaa authentication login default group RADIUS-GROUP local

Enable AAA Authentication for Telnet Login (R1):

aaa authentication login TELNET-LOGIN group RADIUS-GROUP local-case

Set VTY Lines to Use TELNET-LOGIN (R1):

line vty 0 4
login authentication TELNET-LOGIN
exit

Repeat steps 5a to 5g on R3.

Verify by Telnetting from R1 to R3:

R1 Console
telnet 10.2.2.2
Step 6: Enable Secure Remote Management Using SSH

Configure Domain Name (R1):
R1(config)# ip domain-name ccnasecurity.com

Erase Existing RSA Keys (Optional):
R1(config)# crypto key zeroize rsa

Generate RSA Keys:
R1(config)# crypto key generate rsa general-keys modulus 1024

Configure SSH Version 2:
R1(config)# ip ssh version 2

Restrict VTY Lines to SSH Only:
R1(config)# line vty 0 4
transport input ssh
end

Verify SSH Configuration:
R1# show ip ssh

Repeat steps 6a to 6f on R3.

SSH from R1 to R3:
R1# ssh -l ADMIN 10.2.2.2


This completes your practical on securing the management plane across the routers in your topology.
