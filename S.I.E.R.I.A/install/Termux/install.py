#!/data/data/com.termux/files/usr/bin/python
import os
import sys
import subprocess
from colorama import init, Fore, Style

init(autoreset=True)

def termux_install():
    print(f"\n{Fore.CYAN}█▓▒­░⡷⠂ Установка Termux зависимостей ⠐⢾░▒▓█{Style.RESET_ALL}")
    packages = [
        'python', 'clang', 'make', 'cmake', 'libsodium', 
        'libffi', 'openssl', 'rust', 'git', 'tsu',
        'root-repo', 'nmap', 'tor', 'wget'
    ]
    
    for pkg in packages:
        print(f"{Fore.YELLOW}[~] Установка {pkg}...{Style.RESET_ALL}")
        subprocess.run(['pkg', 'install', '-y', pkg], check=True)
    
    # Настройка переменных окружения для Rust
    os.environ['CARGO_BUILD_TARGET'] = 'aarch64-linux-android'
    with open(os.path.expanduser("~/.bashrc"), 'a') as f:
        f.write('\nexport CARGO_BUILD_TARGET=aarch64-linux-android\n')
    
    print(f"{Fore.GREEN}[✓] Системные зависимости установлены!{Style.RESET_ALL}")

def python_install():
    print(f"\n{Fore.MAGENTA}█▓▒­░⡷⠂ Установка Python модулей ⠐⢾░▒▓█{Style.RESET_ALL}")
    modules = [
        'paramiko', 'requests', 'stem', 'python-nmap', 'scapy',
        'colorama', 'cryptography', 'pycryptodome', 'dnspython',
        'beautifulsoup4', 'pyfiglet', 'tqdm'
    ]
    
    for module in modules:
        print(f"{Fore.BLUE}[~] Установка {module}...{Style.RESET_ALL}")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--no-binary", ":all:", "--compile", module
        ], check=True)
    
    print(f"{Fore.GREEN}[✓] Python зависимости установлены!{Style.RESET_ALL}")

def clone_repo():
    print(f"\n{Fore.YELLOW}█▓▒­░⡷⠂ Клонирование репозитория S.I.E.R.I.A ⠐⢾░▒▓█{Style.RESET_ALL}")
    if not os.path.exists("S.I.E.R.I.A"):
        subprocess.run([
            'git', 'clone', 'https://github.com/ShadowDev7/S.I.E.R.I.A.git'
        ], check=True)
        print(f"{Fore.GREEN}[✓] Репозиторий успешно склонирован!{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}[i] Репозиторий уже существует{Style.RESET_ALL}")

def main():
    print(f"\n{Fore.RED}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
    print(f"{Fore.RED}█{Fore.WHITE}           S.I.E.R.I.A INSTALLER v2.0          {Fore.RED}█")
    print(f"{Fore.RED}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Style.RESET_ALL}")
    
    # Обновление пакетов
    print(f"{Fore.CYAN}\n[~] Обновление пакетов Termux...{Style.RESET_ALL}")
    subprocess.run(['pkg', 'update', '-y'], check=True)
    subprocess.run(['pkg', 'upgrade', '-y'], check=True)
    
    termux_install()
    python_install()
    clone_repo()
    
    print(f"\n{Fore.GREEN}▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄")
    print(f"{Fore.GREEN}█{Fore.WHITE} УСТАНОВКА ЗАВЕРШЕНА! Запустите: {Fore.YELLOW}cd S.I.E.R.I.A && python main.py {Fore.GREEN}█")
    print(f"{Fore.GREEN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Style.RESET_ALL}")

if __name__ == "__main__":
    main()