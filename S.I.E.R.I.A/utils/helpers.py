import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    menu = f"""
    {t('menu_title')}
    01. {t('card_generator')}
    02. {t('fake_transfer')}
    03. {t('phishing')}
    04. {t('ip_tools')}
    05. {t('bruteforce')}
    06. {t('vulnerability_scanner')}
    07. {t('malware_generator')}
    08. {t('network_attacks')}
    09. {t('exploits')}
    10. {t('darknet_tools')}
    11. {t('usb_attack')}
    00. {t('exit')}
    """
    print(menu)
    return input(t('enter_choice'))
