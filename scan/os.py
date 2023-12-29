import nmap
from log import log_json,log_error, write_json

def scan_os(ip: str):
    nmScan = nmap.PortScanner()
    machine = nmScan.scan(ip, arguments='-O')

    result = dict()
    for host in nmScan.all_hosts():
     for proto in nmScan[host].all_protocols():
         result[proto] = []
         lport = nmScan[host][proto].keys()
         for port in lport:
             result[proto].append({ port:nmScan[host][proto][port]['state'] == "open"})
    try:
        os = machine['scan'][ip]['osmatch'][0]['osclass'][0]['osfamily']
        result["os"] = os

        log_json(result)
    except:
        log_error( str(ip) + " not found")


