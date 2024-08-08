Step 0: Basic Router Setup

Ensure each router is correctly configured with basic settings, including the disabling of domain lookups and console logging. This is essential for a smooth lab environment.

Router(config)# no ip domain-lookup
Router(config)# line con 0
Router(config-line)# logging synchronous
Router(config-line)# exec-timeout 0 0

Step 1: Configure Interface Addresses

Assign IP addresses to the loopback interfaces and serial interfaces on all routers according to the provided topology.

R1 (ISP) Console

int lo0
ip add 192.168.100.1 255.255.255.0
exit
int s1/0
ip add 192.168.1.5 255.255.255.252
clock rate 128000
no shut
exit
int s1/1
ip add 192.168.1.1 255.255.255.252
no shut
end

R2 (SanJose1) Console

int lo0
ip add 172.16.64.1 255.255.255.0
exit
int s1/0
ip add 192.168.1.6 255.255.255.252
no shut
exit
int s1/1
ip add 172.16.1.1 255.255.255.0
clock rate 128000
no shut
end

R3 (SanJose2) Console

int lo0
ip add 172.16.32.1 255.255.255.0
exit
int s1/0
ip add 192.168.1.2 255.255.255.252
clock rate 128000
no shut
exit
int s1/1
ip add 172.16.1.2 255.255.255.0
no shut
end

Verify connectivity between routers using ping commands.

Step 2: Configure EIGRP Between SanJose Routers

R2 & R3 Console

router eigrp 1
network 172.16.0.0

Step 3: Configure IBGP and Verify BGP Neighbors

R2 Console

router bgp 64512
neighbor 172.16.32.1 remote-as 64512
neighbor 172.16.32.1 update-source lo0

R3 Console

router bgp 64512
neighbor 172.16.64.1 remote-as 64512
neighbor 172.16.64.1 update-source lo0

Verify IBGP neighbors using the show ip bgp neighbors command on R2 and R3.

Step 4: Configure EBGP and Verify BGP Neighbors

R1 (ISP) Console

router bgp 200
neighbor 192.168.1.6 remote-as 64512
neighbor 192.168.1.2 remote-as 64512
network 192.168.100.0

Create a discard static route for the 172.16.0.0/16 network:

R2 & R3 Console
ip route 172.16.0.0 255.255.0.0 null0

Step 5: View BGP Summary Output

Use the show ip bgp summary command to verify the status of BGP neighbors.

Step 6: Verify Traffic Path

Clear BGP sessions and use ping to test reachability and verify BGP routes using the show ip bgp command.

Step 7: Configure BGP Next-Hop-Self

R2 Console

router bgp 64512
neighbor 172.16.32.1 next-hop-self

R3 Console

router bgp 64512
neighbor 172.16.64.1 next-hop-self

Clear BGP sessions and verify with show ip bgp on SanJose2.

Step 8: Set BGP Local Preference

R2 Console

route-map PRIMARY_T1_IN permit 10
set local-preference 150
exit
router bgp 64512
neighbor 192.168.1.5 route-map PRIMARY_T1_IN in

R3 Console

route-map SECONDARY_T1_IN permit 10
set local-preference 125
exit
router bgp 64512
neighbor 192.168.1.1 route-map SECONDARY_T1_IN in

Clear BGP sessions and verify.

Step 9: Set BGP MED

R2 Console

route-map PRIMARY_T1_MED_OUT permit 10
set metric 50
exit
router bgp 64512
neighbor 192.168.1.5 route-map PRIMARY_T1_MED_OUT out

R3 Console

route-map SECONDARY_T1_MED_OUT permit 10
set metric 75
exit
router bgp 64512
neighbor 192.168.1.1 route-map SECONDARY_T1_MED_OUT out

Clear BGP sessions and verify the return path.

Step 10: Establish a Default Route

R1 Console

router bgp 200
neighbor 192.168.1.6 default-originate
neighbor 192.168.1.2 default-originate
exit
int lo10
ip address 10.0.0.1 255.255.255.0

Verify the default route using show ip route and traceroute on R2 and R3.