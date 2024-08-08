Step 1: IP Addressing and OSPF Configuration

Router R1:
    
hostname R1
interface Loopback0
ip address 1.1.1.1 255.255.255.255
ip ospf 1 area 0

interface FastEthernet0/0
ip address 10.0.0.1 255.255.255.0
no shutdown
ip ospf 1 area 0

Router R2:

hostname R2
interface Loopback0
ip address 2.2.2.2 255.255.255.255
ip ospf 1 area 0

interface FastEthernet0/0
ip address 10.0.0.2 255.255.255.0
no shutdown
ip ospf 1 area 0

interface FastEthernet0/1
ip address 10.0.1.2 255.255.255.0
no shutdown
ip ospf 1 area 0

Router R3:

hostname R3
interface Loopback0
ip address 3.3.3.3 255.255.255.255
ip ospf 1 area 0

interface FastEthernet0/1
ip address 10.0.1.3 255.255.255.0
no shutdown
ip ospf 1 area 0

Verification:
    
On R1:

ping 3.3.3.3 source Loopback0

Step 2: Configure LDP on All Interfaces

Router R1:

router ospf 1
mpls ldp autoconfig

Router R2:

router ospf 1
mpls ldp autoconfig

Router R3:

router ospf 1
mpls ldp autoconfig

Verification:
    
On R2:

show mpls interface
show mpls ldp neighbor
trace 3.3.3.3
Step 3: MPLS BGP Configuration

Router R1:
    
router bgp 1
neighbor 3.3.3.3 remote-as 1
neighbor 3.3.3.3 update-source Loopback0
no auto-summary

address-family vpnv4
neighbor 3.3.3.3 activate

Router R3:
    
router bgp 1
neighbor 1.1.1.1 remote-as 1
neighbor 1.1.1.1 update-source Loopback0
no auto-summary

address-family vpnv4
neighbor 1.1.1.1 activate

Verification:
On R1:

show bgp vpnv4 unicast all summary

Step 4: Add Routers and Create VRFs

Router R4:

interface Loopback0
ip address 4.4.4.4 255.255.255.255
ip ospf 2 area 2

interface FastEthernet0/1
ip address 192.168.1.4 255.255.255.0
ip ospf 2 area 2
no shutdown

Router R1:
    
interface FastEthernet0/1
ip address 192.168.1.1 255.255.255.0
no shutdown

ip vrf RED
rd 4:4
route-target both 4:4

interface FastEthernet0/1
ip vrf forwarding RED
ip address 192.168.1.1 255.255.255.0

Verification:
On R1:

show ip route
show ip route vrf RED

Router R5:
    
interface Loopback0
ip address 6.6.6.6 255.255.255.255
ip ospf 2 area 2

interface FastEthernet0/0
ip address 192.168.2.6 255.255.255.0
ip ospf 2 area 2
no shutdown

Router R3:
    
interface FastEthernet0/0
ip address 192.168.2.1 255.255.255.0
no shutdown

ip vrf RED
rd 4:4
route-target both 4:4

interface FastEthernet0/0
ip vrf forwarding RED
ip address 192.168.2.1 255.255.255.0

Verification:
    
On R3:

show ip route vrf RED
Redistribute OSPF into BGP

Router R1:

router bgp 1
address-family ipv4 vrf RED
redistribute ospf 2

Router R3:
    
router bgp 1
address-family ipv4 vrf RED
redistribute ospf 2

Verification:
On R1:

show ip bgp vpnv4 vrf RED

On R3:

show ip bgp vpnv4 vrf RED

Final Verification:
On R4:

show ip route

ping 6.6.6.6
trace 6.6.6.6