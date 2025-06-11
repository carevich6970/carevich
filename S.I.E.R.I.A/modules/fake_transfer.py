import random
import time
from colorama import Fore, Style
from utils.texts import t
from utils.helpers import clear_screen

def create_fake_transfer(bank, amount, sender, receiver):
    transaction_id = ''.join(random.choices('0123456789ABCDEF', k=16))
    date = time.strftime("%d.%m.%Y %H:%M:%S")
    
    return f"""
{Fore.CYAN}=== FAKE TRANSFER RECEIPT ==={Style.RESET_ALL}
Bank: {bank}
Amount: {amount} RUB
From: {sender}
To: {receiver}
Transaction ID: {transaction_id}
Date: {date}

{Fore.YELLOW}This is a simulated transaction for educational purposes only!
No real money has been transferred.{Style.RESET_ALL}
"""

def transfer_menu():
    clear_screen()
    print(f"\n{Fore.MAGENTA}{t('fake_transfer')}{Style.RESET_ALL}")
    
    bank = input("> Bank name: ")
    amount = input("> Amount: ")
    sender = input("> Sender name: ")
    receiver = input("> Receiver name: ")
    
    receipt = create_fake_transfer(bank, amount, sender, receiver)
    print(receipt)
    
    filename = f"transfer_{time.strftime('%Y%m%d%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(receipt)
    
    print(f"{Fore.GREEN}Receipt saved to {filename}{Style.RESET_ALL}")
    input(f"\n{t('press_enter')}")