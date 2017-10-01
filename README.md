# hackathon71

Addressing scheme for lab. Note this is an INCREDIBLY WASTEFUL
addressing setup that I hope no one emulates in a real environment. :)
 
VMX7/8/9 backbone: AS 65000
IPv4:
  10.255.0.0/24 - VMX Loopbacks
  10.1.0.0/16 - PtP addresses
IPv6:
  2001:db8::10:255/80 - VMX Loopbacks
  2001:db8::10:1/80 - PtP addresses

SPINE/LEAF 1/2 - DCA: AS 65011
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
    2001:db8:1:10:128::/64 - Rack1
      2001:db8:1:10:128:::100 - Host1
    2001:db8:1:10:129::/64 - Rack2
      2001:db8:1:10:129:::100 - Host2

SPINE/LEAF 3/4 - DCB: AS 65021
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
    2001:db8:2:10:128::/64 - Rack3
      2001:db8:2:10:128::100 - Host3
    2001:db8:2:10:129::/64 - Rack4
      2001:db8:2:10:129::100 - Rack4


