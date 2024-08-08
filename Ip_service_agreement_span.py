Part 1: Initial Configuration
Step 1: Configure Loopbacks and Assign Addresses

DLS1 Configuration

conf t
DLS1(config)# interface vlan 99
DLS1(config-if)# ip address 172.16.99.1 255.255.255.0
DLS1(config-if)# no shutdown
DLS1(config-if)# exit
DLS1(config)# enable secret class
DLS1(config)# line vty 0 15
DLS1(config-line)# no login
DLS1(config-line)# privilege level 15

ALS1 Configuration

ALS1# conf t
ALS1(config)# hostname ALS1
ALS1(config)# interface vlan 99
ALS1(config-if)# ip address 172.16.99.1 255.255.255.0
ALS1(config-if)# no shutdown
ALS1(config-if)# exit
ALS1(config)# enable secret class
ALS1(config)# line vty 0 15
ALS1(config-line)# no login
ALS1(config-line)# privilege level 15

ALS2 Configuration

ALS2# conf t
ALS2(config)# interface vlan 99
ALS2(config-if)# ip address 172.16.99.1 255.255.255.0
ALS2(config-if)# no shutdown
ALS2(config-if)# exit
ALS2(config)# enable secret class
ALS2(config)# line vty 0 15
ALS2(config-line)# no login
ALS2(config-line)# privilege level 15
ALS2(config)# ip default-gateway 172.16.99.1

Step 2: Configure Host PCs

Host A:

> ip 172.16.100.101/24 172.16.100.1
Host B:
shell
Copy code
> ip 172.16.200.101/24 172.16.200.1

Part 2: Cisco IOS IP SLA Configuration

Step 1: Configure Cisco IOS IP SLA Responders

ALS1 Configuration

ALS1(config)# ip sla responder
ALS1(config)# ip sla responder udp-echo ipaddress 172.16.99.1 port 5000

ALS2 Configuration

ALS2(config)# ip sla responder
ALS2(config)# ip sla responder udp-echo ipaddress 172.16.99.1 port 5000

Step 2: Configure IP SLA Source

DLS1 Configuration

DLS1(config)# ip sla 1
DLS1(config-ip-sla)# icmp-echo 172.16.100.101
DLS1(config-ip-sla-echo)# exit
DLS1(config)# ip sla 2
DLS1(config-ip-sla)# icmp-echo 172.16.200.101
DLS1(config-ip-sla-echo)# exit
DLS1(config)# ip sla 3
DLS1(config-ip-sla)# udp-jitter 172.16.99.101 5000
DLS1(config-ip-sla-jitter)# exit
DLS1(config)# ip sla 4
DLS1(config-ip-sla)# udp-jitter 172.16.99.102 5000
DLS1(config-ip-sla-jitter)# exit

Step 3: Monitor IP SLAs Operations

Commands to Check Configuration

DLS1# show ip sla configuration 1
DLS1# show ip sla configuration 3
DLS1# show ip sla application
ALS1# show ip sla responder
DLS1# show ip sla statistics 1
DLS1# show ip sla statistics 3

Part 3: Switch Port Analyzer (SPAN) Feature

Step 1: Configure Remote SPAN (RSPAN)

DLS1 Configuration

DLS1(config)# vlan 300
DLS1(config-vlan)# name REMOTE_SPAN
DLS1(config-vlan)# remote-span

ALS1 Configuration

ALS1(config)# monitor session 1 source interface Fa0/6
ALS1(config)# monitor session 1 destination remote vlan 300

ALS2 Configuration

ALS2(config)# monitor session 10 source remote vlan 300
ALS2(config)# monitor session 10 destination interface Fa0/6

