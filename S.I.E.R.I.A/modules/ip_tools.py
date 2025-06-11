import socket
import requests
import nmap
from colorama import Fore, Style
from utils.texts import t
from utils.helpers import clear_screen

def get_ip_info():
    try:
        external_ip = requests.get('https://api.ipify.org').text
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        
        geo_data = requests.get(f'https://ipinfo.io/{external_ip}/json').json()
        
        print(f"\n{Fore.GREEN}{t('ip_info').format(
            local_ip,
            external_ip,
            geo_data.get('country', 'N/A'),
            geo_data.get('region', 'N/A'),
            geo_data.get('city', 'N/A'),
            geo_data.get('org', 'N/A'),
            geo_data.get('loc', 'N/A')
        )}")
        
        with open("ip_info.txt", "w") as f:
            f.write(f"Local IP: {local_ip}\n")
            f.write(f"Public IP: {external_ip}\n")
            f.write(f"Country: {geo_data.get('country', 'N/A')}\n")
            f.write(f"Region: {geo_data.get('region', 'N/A')}\n")
            f.write(f"City: {geo_data.get('city', 'N/A')}\n")
            f.write(f"ISP: {geo_data.get('org', 'N/A')}\n")
            f.write(f"Location: {geo_data.get('loc', 'N/A')}\n")
        
        print(f"{Fore.YELLOW}\n{t('log_saved').format('ip_info.txt')}")
        
    except Exception as e:
        print(f"{Fore.RED}{t('error')}: {e}")

def port_scan(target_ip, ports):
    nm = nmap.PortScanner()
    scan_range = ','.join(str(port) for port in ports)
    print(f"{Fore.YELLOW}[+] Scanning {target_ip}...{Style.RESET_ALL}")
    nm.scan(target_ip, arguments=f'-p {scan_range}')
    
    open_ports = []
    for host in nm.all_hosts():
        print(f"\n{Fore.CYAN}Results for {host}:{Style.RESET_ALL}")
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                state = nm[host][proto][port]['state']
                if state == 'open':
                    print(f"{Fore.GREEN}[+] Port {port}/tcp open{Style.RESET_ALL}")
                    open_ports.append(port)
                else:
                    print(f"{Fore.RED}[-] Port {port}/tcp closed{Style.RESET_ALL}")
    return open_ports

def ip_tools():
    while True:
        clear_screen()
        print(f"\n{Fore.MAGENTA}{t('ip_menu')}{Style.RESET_ALL}")
        print("01. Get My IP Info")
        print("02. Port Scan")
        print("03. Connection Test")
        print("00. Back")
        choice = input(t("choose"))
        
        if choice == '01': 
            get_ip_info()
            input(f"\n{t('press_enter')}")
            
        elif choice == '02':  
            target_ip = input("> Target IP: ")
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389]
            print(f"{Fore.YELLOW}[+] Scanning ports on {target_ip}...{Style.RESET_ALL}")
            open_ports = port_scan(target_ip, ports)
            print(f"{Fore.CYAN}[+] Open ports: {open_ports}{Style.RESET_ALL}")
            input(f"\n{t('press_enter')}")
            
        elif choice == '03': 
            target_ip = input("> Target IP: ")
            port = int(input("> Port: "))
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(3)
                s.connect((target_ip, port))
                print(f"{Fore.GREEN}[+] Connection successful!{Style.RESET_ALL}")
                s.close()
            except:
                print(f"{Fore.RED}[-] Connection failed{Style.RESET_ALL}")
            input(f"\n{t('press_enter')}")
            
        elif choice == '00':
            break
            
        else:
            print(t("error"))
            time.sleep(1)