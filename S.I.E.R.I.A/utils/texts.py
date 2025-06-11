from config import LANGUAGE

TEXTS = {
    'en': {
        'termux_only': "This script can only be run in Termux.",
        'warning': "Warning! This tool is for educational purposes only.",
        'press_enter': "Press Enter to continue...",
        'exit': "Exiting the program.",
        'error': "Invalid option. Please try again.",
        'menu_title': "MAIN MENU",
        'card_generator': "Card Generator",
        'fake_transfer': "Fake Transfer",
        'phishing': "Phishing",
        'ip_tools': "IP Tools",
        'bruteforce': "Bruteforce",
        'vulnerability_scanner': "Vulnerability Scanner",
        'malware_generator': "Malware Generator",
        'network_attacks': "Network Attacks",
        'exploits': "Exploits",
        'darknet_tools': "Darknet Tools",
        'enter_choice': "Enter your choice: ",
        'bruteforce_menu': "Bruteforce Menu",
        'phishing_menu': "Phishing Menu",
        'malware_menu': "Malware Generator Menu",
        'attack_menu': "Network Attacks Menu",
        'ip_menu': "IP Tools Menu",
        'darknet_menu': "Darknet Tools Menu",
        'ip_info': "Local IP: {0}\nPublic IP: {1}\nCountry: {2}\nRegion: {3}\nCity: {4}\nISP: {5}\nLocation: {6}",
        'log_saved': "Log saved to {0}",
        'choose': "Choose option: "
    },
    'ru': {
        'termux_only': "Этот скрипт работает только в Termux.",
        'warning': "Внимание! Инструмент предназначен только для обучения.",
        'press_enter': "Нажмите Enter для продолжения...",
        'exit': "Выход из программы.",
        'error': "Неверная опция. Попробуйте снова.",
        'menu_title': "ГЛАВНОЕ МЕНЮ",
        'card_generator': "Генератор карт",
        'fake_transfer': "Фейковый перевод",
        'phishing': "Фишинг",
        'ip_tools': "Инструменты IP",
        'bruteforce': "Брутфорс",
        'vulnerability_scanner': "Сканер уязвимостей",
        'malware_generator': "Генератор вредоносов",
        'network_attacks': "Сетевые атаки",
        'exploits': "Эксплойты",
        'darknet_tools': "Инструменты даркнета",
        'enter_choice': "Введите ваш выбор: ",
        'bruteforce_menu': "Меню брутфорса",
        'phishing_menu': "Меню фишинга",
        'malware_menu': "Меню генератора вредоносов",
        'attack_menu': "Меню сетевых атак",
        'ip_menu': "Меню IP-инструментов",
        'darknet_menu': "Меню даркнет-инструментов",
        'ip_info': "Локальный IP: {0}\nПубличный IP: {1}\nСтрана: {2}\nРегион: {3}\nГород: {4}\nПровайдер: {5}\nКоординаты: {6}",
        'log_saved': "Лог сохранён в {0}",
        'choose': "Выберите опцию: "
    }
}

def t(key):
    return TEXTS[LANGUAGE][key]

def select_language():
    global LANGUAGE
    print("Select language / Выберите язык:")
    print("1. English")
    print("2. Русский")
    choice = input("Choice / Выбор: ")
    LANGUAGE = 'en' if choice == '1' else 'ru'