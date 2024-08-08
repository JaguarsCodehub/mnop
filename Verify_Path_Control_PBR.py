Configuration and Verification of Path Control Using PBR
Topology Overview
This setup involves four routers (R1, R2, R3, and R4) connected via serial interfaces with varying bandwidths. The aim is to configure Policy-Based Routing (PBR) on R3 to control the path for specific traffic from R4.

Step 1: Configure Loopbacks and Assign Addresses
Clear Previous Configurations

Ensure that all routers are reset to default settings.

erase startup-config
reload
Configure Loopback Interfaces and Serial Interfaces

Router R1 Configuration

interface Lo1
description R1 LAN
ip address 192.168.1.1 255.255.255.0
exit
interface S1/0
description R1 --> R2
ip address 172.16.12.1 255.255.255.248
clock rate 128000
bandwidth 128
no shutdown
exit
interface S1/3
description R1 --> R3
ip address 172.16.13.1 255.255.255.248
bandwidth 64
no shutdown
exit

Router R2 Configuration

interface Lo2
description R2 LAN
ip address 192.168.2.1 255.255.255.0
exit
interface S1/0
description R2 --> R1
ip address 172.16.12.2 255.255.255.248
bandwidth 128
no shutdown
exit
interface S1/1
description R2 --> R3
ip address 172.16.23.2 255.255.255.248
clock rate 128000
bandwidth 128
no shutdown
exit

Router R3 Configuration

interface Lo3
description R3 LAN
ip address 192.168.3.1 255.255.255.0
exit
interface S1/3
description R3 --> R1
ip address 172.16.13.3 255.255.255.248
clock rate 64000
bandwidth 64
no shutdown
exit
interface S1/1
description R3 --> R2
ip address 172.16.23.3 255.255.255.248
bandwidth 128
no shutdown
exit
interface S1/2
description R3 --> R4
ip address 172.16.34.3 255.255.255.248
clock rate 64000
bandwidth 64
no shutdown
exit

Router R4 Configuration

interface Lo4
description R4 LAN A
ip address 192.168.4.1 255.255.255.128
exit
interface Lo5
description R4 LAN B
ip address 192.168.4.129 255.255.255.128
exit
interface S1/2
description R4 --> R3
ip address 172.16.34.4 255.255.255.248
bandwidth 64
no shutdown
exit

Verification Commands
Use the following commands to verify the configuration:

show ip interface brief | include up
show interfaces description | include up

Step 3: Configure Basic EIGRP
Implement EIGRP on all Routers

Router R1

router eigrp 1
network 192.168.1.0
network 172.16.12.0 0.0.0.7
network 172.16.13.0 0.0.0.7
no auto-summary

Router R2

router eigrp 1
network 192.168.2.0
network 172.16.12.0 0.0.0.7
network 172.16.23.0 0.0.0.7
no auto-summary

Router R3

router eigrp 1
network 192.168.3.0
network 172.16.13.0 0.0.0.7
network 172.16.23.0 0.0.0.7
network 172.16.34.0 0.0.0.7
no auto-summary

Router R4

router eigrp 1
network 192.168.4.0
network 172.16.34.0 0.0.0.7
no auto-summary

Verify EIGRP Connectivity:
show ip eigrp neighbors

Use the following Tcl script to verify connectivity:

tclsh
foreach address {
172.16.12.1
172.16.12.2
172.16.13.1
172.16.13.3
172.16.23.2
172.16.23.3
172.16.34.3
172.16.34.4
192.168.1.1
192.168.2.1
192.168.3.1
192.168.4.1
192.168.4.129
} { ping $address }

Step 5: Verify the Current Path

Check the Routing Table on R1

show ip route | begin Gateway

Perform Traceroute from R4

traceroute 192.168.1.1 source 192.168.4.1
traceroute 192.168.1.1 source 192.168.4.129

Check the Routing Table on R3:
show ip route | begin Gateway

Verify the Interface Bandwidth on R3

show interfaces S1/3
show interfaces S1/1

Check EIGRP Topology on R3

show ip eigrp topology 192.168.1.0

Step 6: Configure Policy-Based Routing (PBR)

Create a Standard Access List on R3:

ip access-list standard PBR-ACL
remark ACL matches R4 LAN B traffic
permit 192.168.4.128 0.0.0.127
exit

Create a Route Map on R3

route-map R3-to-R1 permit
description RM to forward LAN B traffic to R1
match ip address PBR-ACL
set ip next-hop 172.16.13.1
exit

Apply the Route Map to the Interface on R3:

interface S1/2
ip policy route-map R3-to-R1
end

Verify the Route Map

show route-map

Step 7: Test the Policy

Create an ACL to Match R4 LAN Traffic on R3

access-list 1 permit 192.168.4.0 0.0.0.255
exit

Enable PBR Debugging on R3:
debug ip policy 1

Test the Policy from R4
Traceroute from R4 LAN A:

traceroute 192.168.1.1 source 192.168.4.1

Traceroute from R4 LAN B

traceroute 192.168.1.1 source 192.168.4.129

Verify Route Map Matches

show route-map