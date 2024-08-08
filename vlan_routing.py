Configuration for Router R1:

conf t
interface FastEthernet0/0
no ip address
no shutdown
exit

interface FastEthernet0/0.1
encapsulation dot1Q 10
ip address 10.0.0.1 255.255.255.0
exit

interface FastEthernet0/0.2
encapsulation dot1Q 20
ip address 20.0.0.1 255.255.255.0
exit

Configuration for Switch ESW1:

vlan database
vlan 10 name IT
vlan 20 name HR
exit

conf t
interface FastEthernet1/2
switchport mode access
switchport access vlan 10
exit

interface FastEthernet1/3
switchport mode access
switchport access vlan 20
exit

interface FastEthernet1/1
switchport mode trunk
switchport trunk encapsulation dot1Q
exit

Configuration for PC1:

ip 10.0.0.2 255.255.255.0 10.0.0.1
save
ping 10.0.0.1

Configuration for PC2:

ip 20.0.0.2 255.255.255.0 20.0.0.1
save
ping 20.0.0.1

Result Verification:
To check VLAN configuration on ESW1:

show vlan  