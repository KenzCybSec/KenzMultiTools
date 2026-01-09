import os
import sys
import time
from colorama import Fore, Back, Style, init

# Initialize colors
init(autoreset=True)

# Purple color palette
class Colors:
    PURPLE = '\033[95m'
    LIGHT_PURPLE = '\033[95m'
    DARK_PURPLE = '\033[35m'
    CYAN = '\033[96m'
    LIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def cls():
    """Clear screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Main Banner"""
    cls()
    banner = f"""{Colors.LIGHT_PURPLE}
██╗  ██╗███████╗███╗   ██╗███████╗     ██╗ ██████╗ ██╗███╗   ██╗███████╗██████╗ 
██║ ██╔╝██╔════╝████╗  ██║╚══███╔╝     ██║██╔═══██╗██║████╗  ██║██╔════╝██╔══██╗
█████╔╝ █████╗  ██╔██╗ ██║  ███╔╝      ██║██║   ██║██║██╔██╗ ██║█████╗  ██████╔╝
██╔═██╗ ██╔══╝  ██║╚██╗██║ ███╔╝  ██   ██║██║   ██║██║██║╚██╗██║██╔══╝  ██╔══██╗
██║  ██╗███████╗██║ ╚████║███████╗╚█████╔╝╚██████╔╝██║██║ ╚████║███████╗██║  ██║
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝ ╚════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝                                                                                

{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════╗
{Colors.CYAN}║                      PREMIUM PAID TOOLS v1.0                           ║
{Colors.CYAN}║                 Contact Owner for Purchase & Access                   ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def print_purchase_info():
    """Print purchase information"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║           PURCHASE INFORMATION             ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    print(f"\n{Colors.RED}[⚠️] {Colors.WHITE}THIS IS A PREMIUM PAID TOOL!")
    print(f"{Colors.YELLOW}[🔒] {Colors.WHITE}This tool requires purchase for access")
    
    print(f"\n{Colors.CYAN}[📢] {Colors.WHITE}TO PURCHASE THIS TOOL:")
    print(f"{Colors.PURPLE}    1. {Colors.WHITE}Join our Discord Server")
    print(f"{Colors.PURPLE}    2. {Colors.WHITE}Contact the owner for pricing")
    print(f"{Colors.PURPLE}    3. {Colors.WHITE}Make payment")
    print(f"{Colors.PURPLE}    4. {Colors.WHITE}Receive tool access")
    
    print(f"\n{Colors.CYAN}[💳] {Colors.WHITE}PAYMENT METHODS:")
    print(f"{Colors.YELLOW}    • {Colors.WHITE}Crypto (BTC, ETH, USDT)")
    print(f"{Colors.YELLOW}    • {Colors.WHITE}PayPal (Available)")

def print_contact_details():
    """Print contact details"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║           CONTACT FOR PURCHASE            ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[💬] {Colors.WHITE}DISCORD SERVER")
    print(f"{Colors.PURPLE}    🔗 {Colors.WHITE}https://discord.gg/amGTb4WT")
    
    print(f"\n{Colors.CYAN}[👤] {Colors.WHITE}OWNER (Discord Username)")
    print(f"{Colors.PURPLE}    👑 {Colors.WHITE}kenzzzz11._64163")
    
    print(f"\n{Colors.CYAN}[📱] {Colors.WHITE}TELEGRAM")
    print(f"{Colors.YELLOW}    📞 {Colors.WHITE}Contact via Discord first")

def print_legal_notice():
    """Print legal notice"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║              LEGAL NOTICE                  ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    print(f"\n{Colors.RED}[⚠️] {Colors.WHITE}LEGAL NOTICE:")
    print(f"{Colors.YELLOW}    • {Colors.WHITE}This is a premium paid tool")
    print(f"{Colors.YELLOW}    • {Colors.WHITE}Unauthorized access is prohibited")
    print(f"{Colors.YELLOW}    • {Colors.WHITE}For educational purposes only")
    print(f"{Colors.YELLOW}    • {Colors.WHITE}Purchase required for full access")

def main():
    """Main program"""
    while True:
        print_banner()
        
        print(f"{Colors.CYAN}[*] Welcome to Premium Paid Tools v1.0{Colors.RESET}")
        print(f"{Colors.RED}[!] ⚠️  PURCHASE REQUIRED FOR ACCESS{Colors.RESET}")
        
        print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
        print(f"{Colors.LIGHT_PURPLE}║                 MENU                      ║")
        print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}[1] {Colors.WHITE}💰 Purchase Information")
        print(f"{Colors.CYAN}[2] {Colors.WHITE}📞 Contact Details")
        print(f"{Colors.CYAN}[3] {Colors.WHITE}⚠️  Legal Notice")
        print(f"{Colors.CYAN}[0] {Colors.WHITE}🚪 Exit")
        
        choice = input(f"\n{Colors.LIGHT_PURPLE}[?] Select option (0-3): {Colors.WHITE}")
        
        if choice == '0':
            print(f"\n{Colors.GREEN}[✓] Thank you for your interest!{Colors.RESET}")
            print(f"{Colors.PURPLE}[💎] Contact us to purchase premium tools!{Colors.RESET}\n")
            break
        
        elif choice == '1':
            print_banner()
            print_purchase_info()
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '2':
            print_banner()
            print_contact_details()
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '3':
            print_banner()
            print_legal_notice()
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        else:
            print(f"{Colors.RED}[✗] Invalid option!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        import colorama
    except ImportError:
        print(f"{Colors.RED}[✗] 'colorama' module not installed!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Please install: pip install colorama{Colors.RESET}")
        sys.exit(1)
    
    main()