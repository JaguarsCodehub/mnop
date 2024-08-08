Step 1: Prepare the Routers for the Lab
Cable the network according to the topology diagram.

Erase the startup configuration and reload each router:
erase startup-config
reload

Step 2: Configure the Hostname and Interface Addresses

Router R9 (SanJose) Configuration:

hostname SanJose
interface Loopback0
ip address 10.1.1.1 255.255.255.0
exit
interface S1/0
ip address 192.168.1.5 255.255.255.252
clock rate 128000
no shutdown
exit

Router R10 (ISP) Configuration:

hostname ISP
interface Loopback0
ip address 10.2.2.1 255.255.255.0
exit
interface S1/0
ip address 192.168.1.6 255.255.255.252
no shutdown
exit
interface S1/1
ip address 172.24.1.17 255.255.255.252
clock rate 128000
no shutdown
exit

Router R11 (CustRtr) Configuration:

hostname CustRtr
interface Loopback0
ip address 10.3.3.1 255.255.255.0
exit
interface S1/1
ip address 172.24.1.18 255.255.255.252
no shutdown
exit

Test Connectivity between directly connected routers using ping:

ping [IP Address of the directly connected interface]

Step 3: Configure BGP

Router R9 (SanJose) BGP Configuration:

router bgp 100
neighbor 192.168.1.6 remote-as 300
network 10.1.1.0 mask 255.255.255.0

Router R10 (ISP) BGP Configuration:

router bgp 300
neighbor 192.168.1.5 remote-as 100
neighbor 172.24.1.18 remote-as 65000
network 10.2.2.0 mask 255.255.255.0

Router R11 (CustRtr) BGP Configuration:

router bgp 65000
neighbor 172.24.1.17 remote-as 300
network 10.3.3.0 mask 255.255.255.0

Verify BGP Neighbors:
show ip bgp neighbors

Step 4: Remove the Private AS

SanJose Routing Table:
show ip route

Ping Tests from SanJose:

ping 10.3.3.1
ping 10.3.3.1 source 10.1.1.1

Check the BGP Table:
show ip bgp

Strip the Private AS on ISP:

router bgp 300
neighbor 192.168.1.5 remove-private-as

Clear BGP Sessions:
clear ip bgp *

Verify SanJose's BGP Table:
show ip bgp

Step 5: Use the AS_PATH Attribute to Filter Routes

Configure AS-PATH Access List on ISP:

ip as-path access-list 1 deny ^100$
ip as-path access-list 1 permit .*

Apply the AS-PATH Access List:
router bgp 300
neighbor 172.24.1.18 filter-list 1 out

Clear BGP Sessions:
clear ip bgp *

Verify the Routing Table on CustRtr:
show ip route

Verify the BGP Filter on ISP:
show ip bgp regexp ^100$
Tcl Script for Ping Test

Run the following Tcl script on all routers to verify connectivity:

tclsh
foreach address {
10.1.1.1
10.2.2.1
10.3.3.1
192.168.1.5
192.168.1.6
172.24.1.17
172.24.1.18 } { ping $address }

This should complete the lab with the AS_PATH filtering implemented and validated.