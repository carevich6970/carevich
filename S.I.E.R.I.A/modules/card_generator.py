
import random
from colorama import Fore, Style
from utils.texts import t
from utils.helpers import clear_screen
from config import BANKS

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def generate_valid_card(prefix, length=16):
    while True:
        card = prefix
        while len(card) < (length - 1):
            card += str(random.randint(0, 9))
        
        for digit in range(10):
            candidate = card + str(digit)
            if luhn_checksum(candidate):
                return candidate

def card_generator():
    clear_screen()
    print(f"\n{Fore.MAGENTA}{t('card_generator')}{Style.RESET_ALL}")
    print("Available banks:")
    for i, bank in enumerate(BANKS.keys(), 1):
        print(f"{i}. {bank}")
    
    bank_choice = int(input("\n> Select bank: "))
    bank_name = list(BANKS.keys())[bank_choice-1]
    prefix = BANKS[bank_name]
    
    card_number = generate_valid_card(prefix)
    expiry = f"{random.randint(1,12):02d}/{random.randint(23,30)}"
    cvv = f"{random.randint(0,999):03d}"
    
    print(f"\n{Fore.GREEN}Bank: {bank_name}")
    print(f"Card: {card_number}")
    print(f"Expiry: {expiry}")
    print(f"CVV: {cvv}{Style.RESET_ALL}")
    
    input(f"\n{t('press_enter')}")