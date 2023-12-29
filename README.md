# Verslag Ethical Hacking toolkit
Als eindproject voor het python gedeelte van Ethical Hacking werd er verwacht om een toolkit te schrijven die we als basis konden gebruiken voor pentesting. Ik heb geprobeerd om zeker een stabiele basis te voorzien in deze toolkit. Het aanspreken van de toolkit en het loggen heeft een structuur die ervoor zorgt dat ik hier eenvoudig nieuwe code aan toe kan voegen.
De toolkit is opgedeeld in twee stukken, het scan gedeelte en het aanval gedeelte. Bij het gebruiken van de toolkit moet een van deze vlaggen, `--attack` (`-a` in het kort) of `--scan` (`-s` in het kort), altijd aanwezig zijn.


## Argumenten
Om het parsen van de argumenten in mijn toolkit eenvoudig te maken gebruik ik de `argparse` library. Alle code rond het parsen van argumenten staat in het `/argumenten.py` bestand. De logica rond het parsen van argumenten is zo volledig afgezonderd van de rest van de code. Bij het toevoegen van een argument is er zo maar één plaats waar je moet zoeken in de code.

## Logging
Standaard wordt informatie naar de stdout van de CMD gestuurd om dit te tonen. Hiervoor gebruik ik de `rich` module, zo kan ik de output door het gebruik van kleuren, duidelijker maken. Via het  `--output` ( of `-o` in het kort) argument is het mogelijk om de informatie die gegenereerd wordt door de toolkit naar een bestand weg te schrijven. In het `/log.py` bestand zijn verschillende algemene functies die gebruikt kunnen worden bij het loggen van informatie.
* `log_init` functie wordt gebruikt bij het opstarten van het programma
* `log_error` indien er een error is
* `log_info` als er nuttige informatie is dat getoond moet worden
* `log_json` om JSON-data te loggen

Weer is deze logica afgezonderd, bij het toevoegen van een nieuwe scan of aanval kunnen deze functies gebruikt worden zonder dat de gebruiker zich zorgen moet maken over de `--output` of `-o` argumenten. De algemene functies bevatten logica die hier rekening mee houdt. Zo probeer ik de mogelijkheid tot uitbreiden eenvoudiger te maken.


## Scans
Momenteel zijn er 4 scans die mijn toolkit kunnen doen. Deze zitten allemaal in de `/scans` map, ook als ik een nieuwe toevoeg komt deze hier te staan.

### Ping
Door gebruik te maken van de `scapy` module stuur ik hiermee een ping verzoek over ICMP. Deze scan is heel eenvoudig en heb ik toegevoegd om het gebruik van de toolkit te testen.

Om de target `192.168.0.1` te pingen gebruik je het volgende commando.
`sudo python3 main.py -s ping -t 192.168.0.1`

Het volgende is een voorbeeld van de output van dit programma. Merk op dat op het einde de duratie van het programma wordt getoond.
```
[SYS] scan mode
[SYS] pinging host 192.168.0.1
[INFO] host: 192.168.0.1 is up
[INFO] Finished after 0.03 secs
```

### OS detection
Deze scan detecteert het besturingssysteem van de meegegeven host. Dit werkt via de `nmap` module. De scan is redelijk eenvoudig maar is stiekem toch heel leuk om te gebruiken. Bijkomend scant deze ook de poorten van de host.

Voorbeeld input om host 192.168.0.1 te scannen.
`sudo python3 main.py -s 192.168.0.1`

De output via de CMD ziet er als volgend uit. Indien de `-o` of `--output` vlag mee is gegeven wordt alleen het JSON-object in een bestand gezet.
```
[SYS] scan mode
╭─────────────────────╮
│ {                   │
│   "tcp": [          │
│     {               │
│       "80": true    │
│     },              │
│     {               │
│       "443": true   │
│     },              │
│     {               │
│       "8081": false │
│     },              │
│     {               │
│       "8082": true  │
│     },              │
│     {               │
│       "8888": false │
│     }               │
│   ],                │
│   "os": "FreeBSD"   │
│ }                   │
╰─────────────────────╯
[INFO] Finished after 13.15 secs
```

### Data link laag sniff
De 3e scan die ik heb toegevoegd scant op de datalinklaag (laag 2) naar pakketten. Deze toont de MAC en IP-adressen in de pakketten, laag2 protocol en laag 3 protocol dat wordt gebruikt.

Om te sniffen op ethernetkaart en1 gebruik je het volgende commando.
`sudo python3 main.py -s layer2 -c en1`

Output ziet er als volgend uit, standaard stop deze niet vanzelf en blijft het programma scannen.
```
[SYS] scan mode
[SYS] scanning layer2 on en1
[INFO] Src MAC: 08:b0:55:21:fc:57, Dst MAC: 5c:1b:f4:e3:e4:0e Ether / IP / TCP 193.191.187.198:https > 192.168.0.38:49175 SA
[INFO] Src MAC: 5c:1b:f4:e3:e4:0e, Dst MAC: 08:b0:55:21:fc:57 Ether / IP / TCP 192.168.0.38:49175 > 193.191.187.198:https A / Raw
[INFO] Src MAC: 08:b0:55:21:fc:57, Dst MAC: 5c:1b:f4:e3:e4:0e Ether / IP / TCP 142.250.179.162:https > 192.168.0.38:65456 FA
[INFO] Src MAC: 08:b0:55:21:fc:57, Dst MAC: 5c:1b:f4:e3:e4:0e Ether / IP / TCP 142.250.102.84:https > 192.168.0.38:65463 FA
[INFO] Src MAC: 5c:1b:f4:e3:e4:0e, Dst MAC: 08:b0:55:21:fc:57 Ether / IP / TCP 192.168.0.38:65456 > 142.250.179.162:https A
[INFO] Src MAC: 5c:1b:f4:e3:e4:0e, Dst MAC: 08:b0:55:21:fc:57 Ether / IP / TCP 192.168.0.38:65449 > 172.217.168.202:https A
[INFO] Src MAC: 08:b0:55:21:fc:57, Dst MAC: 5c:1b:f4:e3:e4:0e Ether / IP / TCP 193.191.187.198:https > 192.168.0.38:49175 PA / Raw
[INFO] Src MAC: 5c:1b:f4:e3:e4:0e, Dst MAC: 08:b0:55:21:fc:57 Ether / IP / TCP 192.168.0.38:49175 > 193.191.187.198:https A
[INFO] Src MAC: 5c:1b:f4:e3:e4:0e, Dst MAC: 08:b0:55:21:fc:57 Ether / IP / TCP 192.168.0.38:49175 > 193.191.187.198:https PA / Raw
[INFO] Src MAC: 5c:1b:f4:e3:e4:0e, Dst MAC: 84:2b:2b:9b:74:95 Ether / IP / UDP / DNS Qry "b'accounts.google.com.'"
[INFO] Src MAC: 5c:1b:f4:e3:e4:0e, Dst MAC: 84:2b:2b:9b:74:95 Ether / IP / UDP / DNS Qry "b'accounts.google.com.'"
```

### SSL
De laatste scan vraagt een domeinnaam, hierna worden hier certificaten van opgehaald en zo veel mogelijk informatie uit de certificaten gehaald.

om `google.com` te scannen.
`sudo python3 main.py -s cert -t google.com`

output:
```
[SYS] scan mode
[SYS] scanning google.com
╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ {                                                                                                                                                                                                                                            │
│   "subject": {                                                                                                                                                                                                                               │
│     "commonName": "*.google.com"                                                                                                                                                                                                             │
│   },                                                                                                                                                                                                                                         │
│   "issuer": {                                                                                                                                                                                                                                │
│     "countryName": "US",                                                                                                                                                                                                                     │
│     "organizationName": "Google Trust Services LLC",                                                                                                                                                                                         │
│     "commonName": "GTS CA 1C3"                                                                                                                                                                                                               │
│   },                                                                                                                                                                                                                                         │
│   "serialNumber": "6A5846FCCDDE402E10C94C5ACA9214B7",                                                                                                                                                                                        │
│   "notAfter": "Feb 12 08:02:54 2024 GMT",                                                                                                                                                                                                    │
│   "notBefore": "Nov 20 08:02:55 2023 GMT",                                                                                                                                                                                                   │
│   "version": 3,                                                                                                                                                                                                                              │
│   "cert": "-----BEGIN                                                                                                                                                                                                                        │
│ CERTIFICATE-----MIIOcTCCDVmgAwIBAgIQalhG/M3eQC4QyUxaypIUtzANBgkqhkiG9w0BAQsFADBGMQswCQYDVQQGEwJVUzEiMCAGA1UEChMZR29vZ2xlIFRydXN0IFNlcnZpY2VzIExMQzETMBEGA1UEAxMKR1RTIENBIDFDMzAeFw0yMzExMjAwODAyNTVaFw0yNDAyMTIwODAyNTRaMBcxFTATBgNVBAMMDCou │
│ Z29vZ2xlLmNvbTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABHoPGkE6IqzFZ5fwWMjZ0Y3ZYLSXQczdd1QQtzZfti+nGQCizZu4f4wBc4+jpb22mdwMAGbD4qWWXfdG+GjK4fCjggxTMIIMTzAOBgNVHQ8BAf8EBAMCB4AwEwYDVR0lBAwwCgYIKwYBBQUHAwEwDAYDVR0TAQH/BAIwADAdBgNVHQ4EFgQUYlkUKb4f │
│ DgXAjmrnViKxLBOyHlowHwYDVR0jBBgwFoAUinR/r4XN7pXNPZzQ4kYU83E1HScwagYIKwYBBQUHAQEEXjBcMCcGCCsGAQUFBzABhhtodHRwOi8vb2NzcC5wa2kuZ29vZy9ndHMxYzMwMQYIKwYBBQUHMAKGJWh0dHA6Ly9wa2kuZ29vZy9yZXBvL2NlcnRzL2d0czFjMy5kZXIwggoDBgNVHREEggn6MIIJ9oIMKi5n │
│ b29nbGUuY29tghYqLmFwcGVuZ2luZS5nb29nbGUuY29tggkqLmJkbi5kZXaCFSoub3JpZ2luLXRlc3QuYmRuLmRldoISKi5jbG91ZC5nb29nbGUuY29tghgqLmNyb3dkc291cmNlLmdvb2dsZS5jb22CGCouZGF0YWNvbXB1dGUuZ29vZ2xlLmNvbYILKi5nb29nbGUuY2GCCyouZ29vZ2xlLmNsgg4qLmdvb2dsZS5j │
│ by5pboIOKi5nb29nbGUuY28uanCCDiouZ29vZ2xlLmNvLnVrgg8qLmdvb2dsZS5jb20uYXKCDyouZ29vZ2xlLmNvbS5hdYIPKi5nb29nbGUuY29tLmJygg8qLmdvb2dsZS5jb20uY2+CDyouZ29vZ2xlLmNvbS5teIIPKi5nb29nbGUuY29tLnRygg8qLmdvb2dsZS5jb20udm6CCyouZ29vZ2xlLmRlggsqLmdvb2ds │
│ ZS5lc4ILKi5nb29nbGUuZnKCCyouZ29vZ2xlLmh1ggsqLmdvb2dsZS5pdIILKi5nb29nbGUubmyCCyouZ29vZ2xlLnBsggsqLmdvb2dsZS5wdIISKi5nb29nbGVhZGFwaXMuY29tgg8qLmdvb2dsZWFwaXMuY26CESouZ29vZ2xldmlkZW8uY29tggwqLmdzdGF0aWMuY26CECouZ3N0YXRpYy1jbi5jb22CD2dvb2ds │
│ ZWNuYXBwcy5jboIRKi5nb29nbGVjbmFwcHMuY26CEWdvb2dsZWFwcHMtY24uY29tghMqLmdvb2dsZWFwcHMtY24uY29tggxna2VjbmFwcHMuY26CDiouZ2tlY25hcHBzLmNughJnb29nbGVkb3dubG9hZHMuY26CFCouZ29vZ2xlZG93bmxvYWRzLmNughByZWNhcHRjaGEubmV0LmNughIqLnJlY2FwdGNoYS5uZXQu │
│ Y26CEHJlY2FwdGNoYS1jbi5uZXSCEioucmVjYXB0Y2hhLWNuLm5ldIILd2lkZXZpbmUuY26CDSoud2lkZXZpbmUuY26CEWFtcHByb2plY3Qub3JnLmNughMqLmFtcHByb2plY3Qub3JnLmNughFhbXBwcm9qZWN0Lm5ldC5jboITKi5hbXBwcm9qZWN0Lm5ldC5jboIXZ29vZ2xlLWFuYWx5dGljcy1jbi5jb22CGSou │
│ Z29vZ2xlLWFuYWx5dGljcy1jbi5jb22CF2dvb2dsZWFkc2VydmljZXMtY24uY29tghkqLmdvb2dsZWFkc2VydmljZXMtY24uY29tghFnb29nbGV2YWRzLWNuLmNvbYITKi5nb29nbGV2YWRzLWNuLmNvbYIRZ29vZ2xlYXBpcy1jbi5jb22CEyouZ29vZ2xlYXBpcy1jbi5jb22CFWdvb2dsZW9wdGltaXplLWNuLmNv │
│ bYIXKi5nb29nbGVvcHRpbWl6ZS1jbi5jb22CEmRvdWJsZWNsaWNrLWNuLm5ldIIUKi5kb3VibGVjbGljay1jbi5uZXSCGCouZmxzLmRvdWJsZWNsaWNrLWNuLm5ldIIWKi5nLmRvdWJsZWNsaWNrLWNuLm5ldIIOZG91YmxlY2xpY2suY26CECouZG91YmxlY2xpY2suY26CFCouZmxzLmRvdWJsZWNsaWNrLmNughIq │
│ LmcuZG91YmxlY2xpY2suY26CEWRhcnRzZWFyY2gtY24ubmV0ghMqLmRhcnRzZWFyY2gtY24ubmV0gh1nb29nbGV0cmF2ZWxhZHNlcnZpY2VzLWNuLmNvbYIfKi5nb29nbGV0cmF2ZWxhZHNlcnZpY2VzLWNuLmNvbYIYZ29vZ2xldGFnc2VydmljZXMtY24uY29tghoqLmdvb2dsZXRhZ3NlcnZpY2VzLWNuLmNvbYIX │
│ Z29vZ2xldGFnbWFuYWdlci1jbi5jb22CGSouZ29vZ2xldGFnbWFuYWdlci1jbi5jb22CGGdvb2dsZXN5bmRpY2F0aW9uLWNuLmNvbYIaKi5nb29nbGVzeW5kaWNhdGlvbi1jbi5jb22CJCouc2FmZWZyYW1lLmdvb2dsZXN5bmRpY2F0aW9uLWNuLmNvbYIWYXBwLW1lYXN1cmVtZW50LWNuLmNvbYIYKi5hcHAtbWVh │
│ c3VyZW1lbnQtY24uY29tggtndnQxLWNuLmNvbYINKi5ndnQxLWNuLmNvbYILZ3Z0Mi1jbi5jb22CDSouZ3Z0Mi1jbi5jb22CCzJtZG4tY24ubmV0gg0qLjJtZG4tY24ubmV0ghRnb29nbGVmbGlnaHRzLWNuLm5ldIIWKi5nb29nbGVmbGlnaHRzLWNuLm5ldIIMYWRtb2ItY24uY29tgg4qLmFkbW9iLWNuLmNvbYIU │
│ Z29vZ2xlc2FuZGJveC1jbi5jb22CFiouZ29vZ2xlc2FuZGJveC1jbi5jb22CHiouc2FmZW51cC5nb29nbGVzYW5kYm94LWNuLmNvbYINKi5nc3RhdGljLmNvbYIUKi5tZXRyaWMuZ3N0YXRpYy5jb22CCiouZ3Z0MS5jb22CESouZ2NwY2RuLmd2dDEuY29tggoqLmd2dDIuY29tgg4qLmdjcC5ndnQyLmNvbYIQKi51 │
│ cmwuZ29vZ2xlLmNvbYIWKi55b3V0dWJlLW5vY29va2llLmNvbYILKi55dGltZy5jb22CC2FuZHJvaWQuY29tgg0qLmFuZHJvaWQuY29tghMqLmZsYXNoLmFuZHJvaWQuY29tggRnLmNuggYqLmcuY26CBGcuY2+CBiouZy5jb4IGZ29vLmdsggp3d3cuZ29vLmdsghRnb29nbGUtYW5hbHl0aWNzLmNvbYIWKi5nb29n │
│ bGUtYW5hbHl0aWNzLmNvbYIKZ29vZ2xlLmNvbYISZ29vZ2xlY29tbWVyY2UuY29tghQqLmdvb2dsZWNvbW1lcmNlLmNvbYIIZ2dwaHQuY26CCiouZ2dwaHQuY26CCnVyY2hpbi5jb22CDCoudXJjaGluLmNvbYIIeW91dHUuYmWCC3lvdXR1YmUuY29tgg0qLnlvdXR1YmUuY29tghR5b3V0dWJlZWR1Y2F0aW9uLmNv │
│ bYIWKi55b3V0dWJlZWR1Y2F0aW9uLmNvbYIPeW91dHViZWtpZHMuY29tghEqLnlvdXR1YmVraWRzLmNvbYIFeXQuYmWCByoueXQuYmWCGmFuZHJvaWQuY2xpZW50cy5nb29nbGUuY29tghtkZXZlbG9wZXIuYW5kcm9pZC5nb29nbGUuY26CHGRldmVsb3BlcnMuYW5kcm9pZC5nb29nbGUuY26CGHNvdXJjZS5hbmRy │
│ b2lkLmdvb2dsZS5jboIaZGV2ZWxvcGVyLmNocm9tZS5nb29nbGUuY26CGHdlYi5kZXZlbG9wZXJzLmdvb2dsZS5jbjAhBgNVHSAEGjAYMAgGBmeBDAECATAMBgorBgEEAdZ5AgUDMDwGA1UdHwQ1MDMwMaAvoC2GK2h0dHA6Ly9jcmxzLnBraS5nb29nL2d0czFjMy96ZEFUdDBFeF9Gay5jcmwwggEEBgorBgEEAdZ5 │
│ AgQCBIH1BIHyAPAAdQDuzdBk1dsazsVct520zROiModGfLzs3sNRSFlGcR+1mwAAAYvr9/waAAAEAwBGMEQCID9I2n8NMuW1FzELcE7P9sHblVs55lAY8A6D7V6BQ0LnAiBYkt0j/1BZvc1UnUXRVDPmKbrMm7IbpxzfFGBgrW3+YAB3ADtTd3U+LbmAToswWwb+QDtn2E/D9Me9AA0tcm/h+tQXAAABi+v3/CwAAAQD │
│ AEgwRgIhAOYrscD5NsF+dt+0biySzR8rsOaEe2Swe4/dP2L6EROvAiEAstqe1TBeB5k9AKGqjMydJbjpysfDhK9uW8LqkdqrZ5wwDQYJKoZIhvcNAQELBQADggEBALziHpe+3YavEmr4wjPiI62LsmHxZ0D7xQxqxT86dcLA/6eAcbDN3F5GQz3l9eVIcpNjDv2wc+x83VJywwqxh97qg4CWRxHN897S+dnVCKiTotaQ │
│ pN08p6vQvz8B7c1nF98G2RGDCZCL3XqkABCeVomXdVFXIBwnKC1dtYAwjrIj8wSjNQRhPCiGo0+3DmcUwnQLcY1X+Z+hUtCj65o256jt1jc3l/N4DIe2wX0YTnz4D0egop2vswvK8zr/GyMMFM7ejX5wPACWA+Ad7tFwkSpsZUL+Mm+/hnQjhMurPyYpDyAKJFIWPh4hjdmajrUfWoT54nTQ/52cnmuqGLPRZMQ=---- │
│ -END CERTIFICATE-----",                                                                                                                                                                                                                      │
│   "hostname": "google.com"                                                                                                                                                                                                                   │
│ }                                                                                                                                                                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
[INFO] Finished after 0.29 sec
```

## Attacks
In de toolkit zitten er tot nu toe maar 2 soorten aanvallen in.

### Deauth
De eerste aanval is een wifi deauth attack. Deze zorgt ervoor dat de target die mee is gegeven zichzelf loskoppelt van de verbonden access point. Wanneer een access point wil dat een client niet meer verbonden is met hem stuurt deze een deauth frame, zo verbreekt een AP de connectie tussen zichzelf en de client. In dit geval zijn wij degene die de deauth frame sturen, zo zorgen we ervoor dat een target denkt dat een AP geen connectie meer wil. In python voeren we de aanval uit via de `scapy` module.

Om de 192.168.0.10 host te deauthen gebruik je het volgende commando.
`sudo python3 main.py -a deauth -t 192.168.0.10`

```
[SYS]  attack mode
[INFO] default gateway: 192.168.0.1     08:b0:55:21:fc:57
[INFO] target:          192.168.0.10    00:60:34:0f:c2:db
[INFO] Sending deauth frames
[INFO] Done
[INFO] Finished after 6.95 secs
```
### Man in the middle
Als laatste heb ik een man in the middle aanval toegevoegd. Deze aanval hebben we gezien in de labo's, hier heb ik ook mijn inspiratie vandaan gehaald. Deze stuurt ARP-bericht op een manier waardoor dat de default gateway en de target denken dat ze met elkaar aan het praten zijn maar eigenlijk zit onze machine ertussen.

Als we een target hebben met IP-adres 192.168.0.15, een defaultgateway met IP-adres 192.168.0.1 en een host hebben met 192.168.0.38 als IP-adres kun je met het volgende commando een man in the middle aanval doen.
`sudo python3 main.py -a mitm -t 192.168.0.15 -g 192.168.0.1 --host 192.168.0.38`

Deze output volgt, het programma gaat hierna oneindig lang ARP-berichten blijven uitzenden.
```
[SYS]  attack mode
[INFO] Finished after 0.01 secs
[INFO] starting spoofer 192.168.0.15 -> 192.168.0.1
[INFO] starting spoofer 192.168.0.1 -> 192.168.0.15
```

Via de target machine surfte ik naar google.com. Als we via onze machine via tcpdump kijken zien we dit allemaal voorbijkomen. Merk op dat het 216.58.208.110 een IP-adres is van google.com.
```
$ sudo tcpdump host 216.58.208.110
tcpdump: data link type PKTAP
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on pktap, link-type PKTAP (Apple DLT_PKTAP), snapshot length 524288 bytes
17:02:06.812742 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [.], ack 2599122621, win 301, length 0
17:02:06.815656 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.63180: quic, initial, scid ebf00308a72e45a7, length 1232
17:02:06.817493 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.63180: quic, handshake, scid ebf00308a72e45a7, length 1233
17:02:06.821672 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [P.], seq 39:104, ack 640, win 312, length 65
17:02:06.821673 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [P.], seq 104:135, ack 640, win 312, length 31
17:02:06.821674 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [P.], seq 135:174, ack 640, win 312, length 39
17:02:06.926361 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [P.], seq 135:174, ack 640, win 312, length 39
17:02:07.083227 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [.], ack 640, win 312, options [nop,nop,sack 1 {4294967229:640}], length 0
17:02:07.123136 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.63180: quic, initial, scid ebf00308a72e45a7, length 1232
17:02:07.123140 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.63180: quic, handshake, scid ebf00308a72e45a7, length 775, protected
17:02:07.182397 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [P.], seq 0:174, ack 640, win 312, length 174
17:02:11.621626 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [.], ack 640, win 312, options [nop,nop,sack 1 {4294967229:640}], length 0
17:02:14.373979 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [.], ack 640, win 312, options [nop,nop,sack 1 {4294967228:4294967229}], length 0
17:02:14.816385 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [P.], seq 0:174, ack 640, win 312, length 174
17:02:16.427285 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [.], ack 640, win 312, options [nop,nop,sack 1 {4294967229:640}], length 0
17:02:16.821114 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.40447: Flags [F.], seq 174, ack 692, win 312, length 0
17:02:16.823110 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.63180: quic, protected
17:02:19.754907 IP ams17s08-in-f14.1e100.net.https > 192.168.0.15.63180: quic, protected
```