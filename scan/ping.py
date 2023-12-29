from scapy.all import *

def ping_host(host):
    ans, _unans = sr(IP(dst=host)/ICMP(), timeout=2, verbose=0)
    return len(ans) != 0
