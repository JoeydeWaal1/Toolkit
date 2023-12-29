# warning messages suppressen
import logging

from scan.cert import scan_cert
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import os
from time import time
from arguments import get_arguments
from attack.deauth import deauth
from attack.mitm import mitm
from scan.layer2 import sniff_layer_2
from scan.os import scan_os
from scan.ping import ping_host
from log import *

if __name__ == "__main__":
    start = time()
    args = get_arguments()
    set_q(args.output)
    if not os.geteuid() == 0:
        log_error("Geen root rechten")
        log_info(f"Finished after {round(time() - start, 2)} secs")
        exit(1)

    # sniffen
    if args.scan:
        type_of_scan = args.scan
        log_init("scan mode")

        # --scan layer2 --card en1
        if type_of_scan.lower() == "layer2" and args.card:
            interface = args.card
            log_init(f"scanning {type_of_scan} on {interface}")

            sniff_layer_2(interface)

        # --scan ping --target 192.0....
        elif type_of_scan.lower() == "ping" and args.target:
            target = args.target

            log_init("pinging host " + target)
            if ping_host(target):
                log_info(f"host: {target} is [green]up[/green]")
            else:
                log_info(f"host: {target} is [red]down[/red]")

        # --scan --target google.com
        elif type_of_scan.lower() == "cert" and args.target:
            scan_cert(args.target)


        # --scan 192.168.0.1
        # grote scan doen
        elif args.scan:
            scan_os(args.scan)


    # attack
    elif args.attack:
        log_init("attack mode")
        attack = args.attack.lower()
        target = args.target
        gateway = args.gateway
        host = args.host

        # --attack mitm --target 192.168.0.5 --gateway 192.168.0.1 --host 192.168.0.20
        if attack == "mitm" and target and gateway and host:
            mitm(target, gateway, host)

        # --attack deauth --target 192.168.0.5
        elif attack == "deauth" and target:
            deauth(target)

    log_info(f"Finished after {round(time() - start, 2)} secs")
