Step 1: Configure the Routers and Assign Addresses  (virtual routing and forwading)

1.1. Clear Existing Configurations and Reload Routers

1.2. Configure IP Addresses and VRFs

Router R1:

conf t
ip vrf custA
exit
ip vrf custB
exit

interface FastEthernet0/0
ip vrf forwarding custA
ip address 10.10.10.1 255.255.255.0
no shutdown

interface Serial1/1
ip vrf forwarding custA
ip address 10.12.12.1 255.255.255.0
no shutdown

interface Ethernet2/0
ip vrf forwarding custB
ip address 10.12.12.2 255.255.255.0
no shutdown

interface Ethernet2/0
ip vrf forwarding custB
ip address 10.10.10.2 255.255.255.0
no shutdown

interface Serial1/0
ip vrf forwarding custB
ip address 10.12.12.2 255.255.255.0
no shutdown

Router R2:

conf t
ip vrf custA
exit
ip vrf custB
exit

interface FastEthernet0/0
ip vrf forwarding custA
ip address 10.20.20.2 255.255.255.0
no shutdown

interface Serial1/1
ip vrf forwarding custA
ip address 10.12.12.2 255.255.255.0
no shutdown

interface Ethernet2/0
ip vrf forwarding custB
ip address 10.20.20.3 255.255.255.0
no shutdown

interface Serial1/0
ip vrf forwarding custB
ip address 10.12.12.3 255.255.255.0
no shutdown

Router R3:

interface FastEthernet0/0
ip address 10.10.10.3 255.255.255.0
no shutdown

interface Loopback0
ip address 10.1.1.3 255.255.255.0
no shutdown

Router R4:
    
interface Ethernet1/0
ip address 10.10.10.5 255.255.255.0
no shutdown

interface Loopback0
ip address 10.1.1.5 255.255.255.0
no shutdown

Router R5:
    
interface FastEthernet0/0
ip address 10.20.20.4 255.255.255.0
no shutdown

interface Loopback0
ip address 10.2.2.4 255.255.255.0
no shutdown

Router R6:
    
interface FastEthernet0/0
ip address 10.20.20.6 255.255.255.0
no shutdown

interface Loopback0
ip address 10.2.2.6 255.255.255.0
no shutdown

Step 2: Configure EIGRP

Routers R3, R4, R5, R6:

router eigrp 100
no auto-summary
network 10.0.0.0
exit

Router R1:

router eigrp 1
address-family ipv4 vrf custA
autonomous-system 100
no auto-summary
network 10.0.0.0
address-family ipv4 vrf custB
autonomous-system 100
no auto-summary
network 10.0.0.0
exit

Router R2:
    
router eigrp 1
address-family ipv4 vrf custA
autonomous-system 100
no auto-summary
network 10.0.0.0
address-family ipv4 vrf custB
autonomous-system 100
no auto-summary
network 10.0.0.0
exit

Verification

Router R1:
    
show ip route
show ip route vrf custA
show ip int brief
ping vrf custA 10.1.1.3
ping vrf custB 10.1.1.5

Router R3:
    
show ip int brief
ping 10.2.2.4

Router R2:
    
show ip route vrf custB
