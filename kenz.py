import os
import sys
import subprocess
import ctypes

# Windows terminal başlığını değiştir
def set_windows_title():
    if os.name == 'nt':  # Windows
        ctypes.windll.kernel32.SetConsoleTitleW("KENZ MULTI TOOLS | Made by Kenz")

# Ana kodun en başına ekle
set_windows_title()

# ===== COLORS =====
PURPLE = "\033[95m"
PURPLE_BRIGHT = "\033[35m"
MAGENTA = "\033[35m"
VIOLET = "\033[38;5;99m"
LAVENDER = "\033[38;5;183m"
PINK = "\033[38;5;213m"
RESET = "\033[0m"
BOLD = "\033[1m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(LAVENDER + BOLD)
    print(""" 
 ██ ▄█▀▓█████  ███▄    █ ▒███████▒ ███▄ ▄███▓▓█████  ███▄    █  █    ██ 
 ██▄█▒ ▓█   ▀  ██ ▀█   █ ▒ ▒ ▒ ▄▀░▓██▒▀█▀ ██▒▓█   ▀  ██ ▀█   █  ██  ▓██▒
▓███▄░ ▒███   ▓██  ▀█ ██▒░ ▒ ▄▀▒░ ▓██    ▓██░▒███   ▓██  ▀█ ██▒▓██  ▒██░
▓██ █▄ ▒▓█  ▄ ▓██▒  ▐▌██▒  ▄▀▒   ░▒██    ▒██ ▒▓█  ▄ ▓██▒  ▐▌██▒▓▓█  ░██░
▒██▒ █▄░▒████▒▒██░   ▓██░▒███████▒▒██▒   ░██▒░▒████▒▒██░   ▓██░▒▒█████▓ 
▒ ▒▒ ▓▒░░ ▒░ ░░ ▒░   ▒ ▒ ░▒▒ ▓░▒░▒░ ▒░   ░  ░░░ ▒░ ░░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ 
░ ░▒ ▒░ ░ ░  ░░ ░░   ░ ▒░░░▒ ▒ ░ ▒░  ░      ░ ░ ░  ░░ ░░   ░ ▒░░░▒░ ░ ░ 
░ ░░ ░    ░      ░   ░ ░ ░ ░ ░ ░ ░░      ░      ░      ░   ░ ░  ░░░ ░ ░ 
░  ░      ░  ░         ░   ░ ░           ░      ░  ░         ░    ░     
                         ░                                              
""")
    print("   K E N Z   M U L T I   T O O L S")
    print("   ================================\n" + RESET)

def pad(text, width=20):
    return text.ljust(width)

def run_script(script_name):
    """Run Python script"""
    script_path = f"data/{script_name}"
    if os.path.exists(script_path):
        print(f"\n{LAVENDER}[+] Running: {script_name}{RESET}")
        subprocess.run([sys.executable, script_path])
    else:
        print(f"\n{MAGENTA}[!] Error: {script_name} not found in data/ folder!{RESET}")

def main():
    while True:
        clear()
        banner()

        # Başlıkları yazdır - Bonus daha uzakta
        print(PURPLE + BOLD +
              pad("[GENERATORS]") +
              pad("[DISCORD]") +
              pad("[NETWORK]") +
              pad("[PREMIUM]") +
              "    " + pad("[BONUS]"))
        print("-" * 105 + RESET)

        # Düzenli satırlar - Bonus sütunu daha uzakta
        rows = [
            ["1. Token Gen",       "6. Account Amount",   "11. DDoS",          "16. Kenz Gen Premium", "    19. Info"],
            ["2. Nitro Gen",       "7. Token Info",       "12. Humanizer",     "17. Nitro Gen Premium", ""],
            ["3. Spotify Gen",     "8. Token Login",      "13. Webhook Spammer", "18. Discord Bot Premium", ""],
            ["4. IP Generator",    "9. Server Lookup",    "14. IP Checker",    "", ""],
            ["5. Kenz Generator",  "10. Webhook Info",    "15. Webhook Spammer", "", ""]
        ]

        for row in rows:
            line = ""
            for i, item in enumerate(row):
                if i == 4:  # Bonus sütunu
                    color = PINK  # Pembe renk
                elif i == 0:  # Generators sütunu
                    color = PURPLE_BRIGHT  # Parlak mor
                else:  # Diğer sütunlar
                    color = PURPLE  # Normal mor
                line += color + pad(item) + RESET
            print(line)

        print(f"\n{LAVENDER}0. Exit{RESET}")
        print("-" * 50)
        
        try:
            choice = int(input(f"\n{VIOLET}Select > {RESET}"))
        except ValueError:
            input(f"\n{MAGENTA}[!] Invalid selection! Press Enter to try again...{RESET}")
            continue

        # Script mapping
        if choice == 0:
            print(f"\n{LAVENDER}[+] Exiting... Goodbye!{RESET}")
            sys.exit(0)
        elif choice == 1:
            run_script("kenzgen.py")  # Token Gen
        elif choice == 2:
            run_script("nitrogen.py")  # Nitro Gen
        elif choice == 3:
            run_script("Spotifygenerator.py")  # Spotify Gen
        elif choice == 4:
            run_script("ipGenerator.py")  # IP Generator
        elif choice == 5:
            run_script("kenzjoiner.py")  # Kenz Generator
        elif choice == 6:
            run_script("account_amount.py")  # Account Amount
        elif choice == 7:
            run_script("tokeninfo.py")  # Token Info
        elif choice == 8:
            run_script("TokenLogin.py")  # Token Login
        elif choice == 9:
            run_script("Server_Lookup.py")  # Server Lookup
        elif choice == 10:
            run_script("WebhookInfo.py")  # Webhook Info
        elif choice == 11:
            run_script("ddos.py")  # DDoS
        elif choice == 12:
            run_script("huminazer.py")  # Humanizer
        elif choice == 13:
            run_script("WebhookSpammer.py")  # Webhook Spammer
        elif choice == 14:
            run_script("ipchecker.py")  # IP Checker
        elif choice == 15:
            run_script("WebhookSpammer.py")  # Webhook Spammer (duplicate)
        elif choice == 16:
            run_script("kenzgenspremium.py")  # Kenz Gen Premium
        elif choice == 17:
            run_script("NitroGenPremium.py")  # Nitro Gen Premium
        elif choice == 18:
            run_script("DiscordBotPremium.py")  # Discord Bot Premium
        elif choice == 19:
            run_script("info.py")  # Info (BONUS section)
        else:
            print(f"\n{MAGENTA}[!] Invalid selection! Please choose 0-19.{RESET}")
        
        input(f"\n{VIOLET}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    # Check data folder
    if not os.path.exists("data"):
        print(f"{MAGENTA}[!] Error: 'data' folder not found!{RESET}")
        print(f"{LAVENDER}[+] Please make sure all scripts are in the 'data' folder.{RESET}")
        sys.exit(1)
    
    main()