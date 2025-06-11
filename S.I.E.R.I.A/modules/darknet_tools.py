import os
import requests
from stem import Signal
from stem.control import Controller
from colorama import Fore, Style
from utils.texts import t
from utils.helpers import clear_screen

def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }
    return session

def renew_tor_connection():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        return True
    except:
        print(f"{Fore.RED}Tor control port error. Start Tor service first!{Style.RESET_ALL}")
        return False

def darknet_search(query):
    if not renew_tor_connection():
        return
        
    try:
        session = get_tor_session()
        url = f"http://darkfailllnkf4vf.onion/search?q={query}"
        response = session.get(url, timeout=30)
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Found {len(response.text)} bytes of data{Style.RESET_ALL}")
            
            onions = []
            for part in response.text.split():
                if part.endswith(".onion") and 16 <= len(part) <= 56:
                    onions.append(part)
            
            if onions:
                print(f"{Fore.CYAN}\n[+] Found .onion links:{Style.RESET_ALL}")
                for onion in set(onions[:10]):
                    print(onion)
            else:
                print(f"{Fore.YELLOW}[-] No .onion links found{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Request error: {response.status_code}{Style.RESET_ALL}")
    
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

def darknet_tools():
    while True:
        clear_screen()
        print(f"\n{Fore.MAGENTA}{t('darknet_menu')}{Style.RESET_ALL}")
        print("01. Search Darknet")
        print("02. Find Services")
        print("03. Find Documents")
        print("00. Back")
        choice = input(t("choose"))
        
        if choice == '01':  
            query = input("> Search query: ")
            darknet_search(query)
            input(f"\n{t('press_enter')}")
            
        elif choice == '02': 
            query = input("> Service type: ")
            darknet_search(f"{query} service")
            input(f"\n{t('press_enter')}")
            
        elif choice == '03': 
            query = input("> Document keywords: ")
            darknet_search(f"{query} filetype:pdf OR filetype:doc")
            input(f"\n{t('press_enter')}")
            
        elif choice == '00':
            break
            
        else:
            print(t("error"))
            time.sleep(1)