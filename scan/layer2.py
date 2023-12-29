from scapy.all import sniff
from log import log_info

def packet_callback(packet):
    if packet.haslayer('Ether'):
        src_mac = packet['Ether'].src
        dst_mac = packet['Ether'].dst
        # print(packet.summary())
        log_info(f"Src MAC: {src_mac}, Dst MAC: {dst_mac} {packet.summary()}")

def sniff_layer_2( card: str ):
    sniff(iface=card, prn=packet_callback)
