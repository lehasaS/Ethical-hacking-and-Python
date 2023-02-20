import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)
import scapy.all as scapy
import requests
import argparse

def get_ip_range():
    parser = argparse.ArgumentParser(prog='network_scanner.py', description="Scans for devices connected in the network")
    parser.add_argument("-t", "--target", dest="target", help="Enter the target IP address or IP address range", type=str)
    values = parser.parse_args()

    if not values.target:
        parser.error("[-] Please specify the target IP address or IP address range, use --help for more information")
    else:
        return values

def get_clients(ip_address):
    request_ip = scapy.ARP(pdst=ip_address)
    broadcast_mac = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_packet = broadcast_mac/request_ip
    print(arp_request_packet.show())
    answered_list = scapy.srp(arp_request_packet, timeout=20, verbose=False)[0]

    clients_list=[]
    for client in answered_list:
        client_dict={"ip":client[1].psrc, "mac":client[1].hwsrc}
        clients_list.append(client_dict)

    return clients_list

def get_vendor(mac):
    try:
        return requests.get('http://api.macvendors.com/' + mac).text
    except:
        return Exception("Vendor Not Found")

def print_clients(clients_list):
    print("IP\t\t\tMAC Address\t\t\tVendor\n-------------------------------------")

    for client in clients_list:
        vendor = get_vendor(client["mac"])
        print(client["ip"]+"\t\t"+client["mac"]+"\t\t"+vendor)

def main():
    ip_address = get_ip_range()
    clients = get_clients(ip_address.target)
    print_clients(clients)

if __name__ == '__main__':
    main()

