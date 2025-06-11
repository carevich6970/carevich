from colorama import Fore

# Глобальные настройки
LANGUAGE = "en"
COLORS = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
current_color_idx = 0
color_change_active = True

# Банковские префиксы
BANKS = {
    "Visa": "4",
    "MasterCard": "5",
    "American Express": "34",
    "Discover": "6",
    "JCB": "35"
}