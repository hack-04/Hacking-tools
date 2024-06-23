import scapy.all as scapy
import optparse


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    clients_list =[]
    for element in answered_list:
        clients_dict = {"IP": element[1].psrc, "MAC": element[1].hwsrc}
        clients_list.append(clients_dict)
    return clients_list


def print_result(result_list):
    print("IP\t\t\tMAC\n--------------------------------------")
    for client in result_list:
        print(client["IP"] + "\t\t" + client["MAC"])


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="Target uchun argumentlar")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-t] Iltimos, ma'lumotlarni kiriting")
    return options


options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)
