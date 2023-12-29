from scapy.all import *

def arp(ip: str):# -> str:
    ans,_unans = arping(ip, verbose=0)
    if len(ans) == 0:
        raise Exception(f"geen mac addres gevonden voor ip: {ip}")

    mac =  ans[0][1][Ether].src
    return mac
