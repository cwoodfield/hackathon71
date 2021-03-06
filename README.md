# hackathon71

Addressing scheme for lab. Note this is an INCREDIBLY WASTEFUL
addressing setup that I hope no one emulates in a real environment. :)

VMX7/8/9 run IS-IS on "backbone" lines, and peer via iBGP to loopbacks
over both IPv4 and IPv6, advertising 0/0 to each spine, which is separated
into DCA (spine1/2) and DCB (spine3/4).

DCA/DCB speak EBGP internally, and advertise datacenter aggregates
to the upstream VMXes.

host1/2/3/4 are reachable via /etc/host entries on the jumphost; IPs below
are specific to the DC fabric itself (use these if you set up host-leaf BGP,
for example).

![Lab Diagram](./hackathon_lab_diagram_asns.png)

``` 
VMX7/8/9 backbone: AS 65000
IPv4:
  10.255.0.0/24 - VMX Loopbacks
  10.1.0.0/16 - PtP addresses
IPv6:
  2001:db8::10:255/80 - VMX Loopbacks
  2001:db8::10:1/80 - PtP addresses

SPINE/LEAF 1/2 - DCA: AS 65001 (spine), 65011/65012 (leaf1/2)
IPv4:
  10.16.0.0/16 - DCA Aggregate
    10.16.1.0/24 - PtP
    10.16.32.0/24 - Loopbacks
    10.16.128.0/24 - Rack1
      10.16.128.100 - Host1
    10.16.129.0/24 - Rack2
      10.16.129.100 - Host2
IPv6:
  2001:db8:1::10:16/80 -  DCA Aggregate
    2001:db8:1::10:16:32/96 - PtP
    2001:db8:1::10:16:33/96 - Loopbacks
    2001:db8:1:128::/64 - Rack1
      2001:db8:1:128::100 - Host1
    2001:db8:1:129::/64 - Rack2
      2001:db8:1:129::100 - Host2

SPINE/LEAF 3/4 - DCB: AS 65002 (spine), 65021/65022 (leaf1/2)
IPv4:
  10.17.0.0/16 - DCB Aggregate
    10.17.1.0/24 - PtP
    10.17.32.0/24 - Loopbacks
    10.17.128.0/24 - Rack3
      10.17.128.100 - Host3
    10.17.129.0/24 - Rack4
      10.17.129.100 - Host4
IPv6:
  2001:db8:2::10:16/80 -  DCB Aggregate
    2001:db8:2::10:16:32/96 - PtP
    2001:db8:2::10:16:33/96 - Loopbacks
    2001:db8:2:128::/64 - Rack3
      2001:db8:2:128::100 - Host3
    2001:db8:2:129::/64 - Rack4
      2001:db8:2:129::100 - Rack4
```
