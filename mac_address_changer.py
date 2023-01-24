import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Name of interface to change its MAC")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (values, arguments) = parser.parse_args()

    if not values.interface:
        parser.error("[-] Please specify the name of the interface, use --help for more information")
    elif not values.new_mac:
        parser.error("[-] Please specify the new MAC address to replace the current, use --help for more information")
    else:
        return values

def get_mac_address(interface):
    ifconfig_result = subprocess.check_output(["ifconfig",interface])
    mac_address = re.search(r"\ww:\ww:\ww:\ww:\ww:\ww", str(ifconfig_result))

    if mac_address:
        return str(mac_address.group(0))
    else:
        return ""

def change_mac_address(values):
    subprocess.call(["ifconfig", values.interface, "down"])
    subprocess.call(["ifconfig", values.interface, "hw", "ether", values.new_mac])
    subprocess.call(["ifconfig", values.interface, "up"])

def validate_mac_change(interface, new_mac):
    current_mac = get_mac_address(interface)

    if current_mac == new_mac:
        print("[+] MAC address for interface " + interface + " successfully changed!")
    else:
        print("[-] An error occured, MAC not changed!")

def main():
    values = get_arguments()
    current_mac = get_mac_address(values.interface)

    if current_mac != "":
        print("[+] The current MAC address for interface " + values.interface + " is: " + current_mac)

        print("[+] Attempting to change MAC address of given interface")

        change_mac_address(values)

        current_mac = get_mac_address(values.interface)

        validate_mac_change(values.interface, current_mac)
    else:
        print("[-] Unable to read current MAC, choose interface with a MAC address")

if __name__ == '__main__':
    main()