import os
import sys
import time
import threading
from colorama import init, Fore, Style
from utils.logo import get_siera_logo, animate_logo
from utils.texts import t, select_language
from utils.helpers import clear_screen, show_menu

def main():
    # Запуск анимации логотипа
    color_thread = threading.Thread(target=animate_logo, daemon=True)
    color_thread.start()
    
    # Проверка на Kali Linux
    if not os.path.exists("/etc/os-release") or "kali" not in open("/etc/os-release").read().lower():
        print(f"{Fore.RED}This tool requires Kali Linux!{Style.RESET_ALL}")
        sys.exit(1)
    
    select_language()
    print(f"\n{Fore.RED}{t('warning')}{Style.RESET_ALL}\n")
    input(t("press_enter"))
    
    # Импорт модулей
    from modules import (
        card_generator, fake_transfer, phishing, ip_tools, bruteforce,
        vulnerability_scanner, malware_generator, network_attacks,
        exploits, darknet_tools, usb_attack
    )
    
    while True:
        clear_screen()
        choice = show_menu()
        
        # Меню функций
        modules_map = {
            '01': card_generator,
            '02': fake_transfer,
            '03': phishing,
            '04': ip_tools,
            '05': bruteforce,
            '06': vulnerability_scanner,
            '07': malware_generator,
            '08': network_attacks,
            '09': exploits,
            '10': darknet_tools,
            '11': usb_attack,
            '00': sys.exit
        }
        
        if choice in modules_map:
            if choice == '00':
                print(f"{Fore.RED}{t('exit')}")
                time.sleep(0.6)
                modules_map[choice](0)
            else:
                modules_map[choice]()
        else:
            print(t("error"))
            time.sleep(1)

if __name__ == "__main__":
    init(autoreset=True)
    main()