R1 Configuration:

hostname R1
int lo0
description R1 LAN
ip address 192.168.1.1 255.255.255.0
int s1/0
description R1 --> ISP1
ip address 209.165.201.2 255.255.255.252
clock rate 128000
bandwidth 128
no shut
int s1/1
description R1 --> ISP2
ip address 209.165.202.130 255.255.255.252
bandwidth 128
no shut

ISP1 (R2) Configuration:
    
hostname ISP1
int lo0
description Simulated Internet Web Server
ip address 209.165.200.254 255.255.255.255
int lo1
description ISP1 DNS Server
ip address 209.165.201.30 255.255.255.255
int s1/0
description ISP1 -->R1
ip address 209.165.201.1 255.255.255.252
bandwidth 128
no shut
int s1/2
description ISP1 --> ISP2
ip address 209.165.200.225 255.255.255.252
clock rate 128000
bandwidth 128
no shut

ISP2 (R3) Configuration:
    
hostname ISP2
int lo0
description Simulated Internet Web Server
ip address 209.165.200.254 255.255.255.255
int lo1
description ISP2 DNS Server
ip address 209.165.202.158 255.255.255.255
int s1/1
description ISP2 --> R1
ip address 209.165.202.129 255.255.255.252
clock rate 128000
bandwidth 128
no shut
int s1/2
description ISP2 --> ISP1
ip address 209.165.200.226 255.255.255.252
bandwidth 128
no shut

Verification Commands:
show int description

Static Routing on R1:
ip route 0.0.0.0 0.0.0.0 209.165.201.1

EIGRP Configuration on ISP1 (R2):
    
router eigrp 1
network 209.165.200.224 0.0.0.3
network 209.165.201.0 0.0.0.31
no auto-summary
exit
ip route 192.168.1.0 255.255.255.0 209.165.201.2

EIGRP Configuration on ISP2 (R3):
    
router eigrp 1
network 209.165.200.224 0.0.0.3
network 209.165.202.128 0.0.0.31
no auto-summary
exit
ip route 192.168.1.0 255.255.255.0 209.165.202.130

#-----R1#

Tcl Ping Script on R1:

tclsh
foreach address {
  209.165.200.254
  209.165.201.30
  209.165.202.158
} {
  ping $address source 192.168.1.1
}

Tcl Trace Script on R1:
    
tclsh
foreach address {
  209.165.200.254
  209.165.201.30
  209.165.202.158
} {
  trace $address source 192.168.1.1
}

IP SLA Probe Configuration on R1:
    
ip sla 11
icmp-echo 209.165.201.30
frequency 10
exit
ip sla schedule 11 life forever start-time now

ip sla 22
icmp-echo 209.165.202.158
frequency 10
exit
ip sla schedule 22 life forever start-time now

show ip sla configuration 11
show ip sla statistics 11

show ip sla configuration 22
show ip sla statistics 22

Tracking and Floating Static Routes on R1:
    
no ip route 0.0.0.0 0.0.0.0 209.165.201.1
ip route 0.0.0.0 0.0.0.0 209.165.201.1 5

track 1 ip sla 11 reachability
delay down 10 up 1
exit

show ip route

debug ip routing

ip route 0.0.0.0 0.0.0.0 209.165.201.1 2 track 1

track 2 ip sla 22 reachability
delay down 10 up 1
exit

ip route 0.0.0.0 0.0.0.0 209.165.202.129 3 track 2

show ip route

Verifying IP SLA Operation:
Disable the DNS loopback interface on ISP1:

int lo1
shutdown

Verify debug output on R1:
show ip route | begin Gateway

Verify IP SLA statistics:
show ip sla statistics

Trace to the web server:

trace 209.165.200.254 source 192.168.1.1

Re-enable the DNS loopback interface on ISP1:
int lo1
no shutdown

Verify IP SLA statistics and routing table:
show ip sla statistics
show ip route | begin Gateway