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
 ██▓ ███▄    █   █████▒▒█████  
▓██▒ ██ ▀█   █ ▓██   ▒▒██▒  ██▒
▒██▒▓██  ▀█ ██▒▒████ ░▒██░  ██▒
░██░▓██▒  ▐▌██▒░▓█▒  ░▒██   ██░
░██░▒██░   ▓██░░▒█░   ░ ████▓▒░
░▓  ░ ▒░   ▒ ▒  ▒ ░   ░ ▒░▒░▒░ 
 ▒ ░░ ░░   ░ ▒░ ░       ░ ▒ ▒░ 
 ▒ ░   ░   ░ ░  ░ ░   ░ ░ ░ ▒  
 ░           ░            ░ ░  
                               
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════╗
{Colors.CYAN}║                         KENZ MULTI TOOLS v1.0                          ║
{Colors.CYAN}║                       Professional Tool Collection                     ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

def print_contact_info():
    """Print contact information"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║             CONTACT INFORMATION            ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[📢] {Colors.WHITE}DISCORD SERVER")
    print(f"{Colors.PURPLE}    🔗 {Colors.WHITE}https://discord.gg/amGTb4WT")
    
    print(f"\n{Colors.CYAN}[👤] {Colors.WHITE}CONTACT (Discord Username)")
    print(f"{Colors.PURPLE}    👑 {Colors.WHITE}kenzzzz11._64163")
    
    print(f"\n{Colors.CYAN}[📱] {Colors.WHITE}TELEGRAM")
    print(f"{Colors.YELLOW}    ⏳ {Colors.WHITE}Coming Soon...")
    
    print(f"\n{Colors.CYAN}[💎] {Colors.WHITE}DONATE / SUPPORT")
    print(f"{Colors.YELLOW}    ⏳ {Colors.WHITE}Coming Soon...")
    
    print(f"\n{Colors.CYAN}[⚡] {Colors.WHITE}PREMIUM TOOLS")
    print(f"{Colors.YELLOW}    ⏳ {Colors.WHITE}Coming Soon...")

def print_social_links():
    """Print social media links"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║              SOCIAL LINKS                 ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    socials = [
        ("Discord Server", "https://discord.gg/amGTb4WT", "💬"),
        ("Contact (Discord)", "kenzzzz11._64163", "👤"),
        ("Telegram", "Coming Soon", "📱"),
        ("Donate", "Coming Soon", "💎"),
        ("Premium Tools", "Coming Soon", "⚡")
    ]
    
    for name, link, emoji in socials:
        print(f"{Colors.CYAN}{emoji} {Colors.WHITE}{name}:")
        print(f"    {Colors.PURPLE}🔗 {Colors.WHITE}{link}")

def main():
    """Main program"""
    while True:
        print_banner()
        
        print(f"{Colors.CYAN}[*] Welcome to Kenz Multi Tools v1.0{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] For educational purposes only{Colors.RESET}")
        
        print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
        print(f"{Colors.LIGHT_PURPLE}║                 MENU                      ║")
        print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}[1] {Colors.WHITE}📞 View Contact Information")
        print(f"{Colors.CYAN}[2] {Colors.WHITE}🔗 View Social Links")
        print(f"{Colors.CYAN}[3] {Colors.WHITE}ℹ️  About This Tool")
        print(f"{Colors.CYAN}[0] {Colors.WHITE}🚪 Exit")
        
        choice = input(f"\n{Colors.LIGHT_PURPLE}[?] Select option (0-3): {Colors.WHITE}")
        
        if choice == '0':
            print(f"\n{Colors.GREEN}[✓] Thank you for using Kenz Multi Tools!{Colors.RESET}")
            print(f"{Colors.PURPLE}[❤] Goodbye!{Colors.RESET}\n")
            break
        
        elif choice == '1':
            print_banner()
            print_contact_info()
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '2':
            print_banner()
            print_social_links()
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '3':
            print_banner()
            print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
            print(f"{Colors.LIGHT_PURPLE}║               ABOUT TOOL                  ║")
            print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
            
            about_text = f"""
{Colors.CYAN}[🎯] {Colors.WHITE}Kenz Multi Tools v1.0
{Colors.PURPLE}────────────────────────────────────────────

{Colors.CYAN}[📝] {Colors.WHITE}DESCRIPTION:
{Colors.WHITE}    Professional collection of hacking and security tools
{Colors.WHITE}    Created for educational and research purposes
{Colors.WHITE}    All tools are open source and free to use

{Colors.CYAN}[⚡] {Colors.WHITE}FEATURES:
{Colors.WHITE}    • Discord tools (Webhooks, Tokens, Servers)
{Colors.WHITE}    • IP tools (Generator, Checker)
{Colors.WHITE}    • Network tools
{Colors.WHITE}    • Security testing tools
{Colors.WHITE}    • Multi-threaded operations

{Colors.CYAN}[⚠️] {Colors.WHITE}DISCLAIMER:
{Colors.RED}    • For educational purposes only
{Colors.RED}    • Unauthorized use is illegal
{Colors.RED}    • Use only on systems you own
{Colors.RED}    • The developer is not responsible for misuse

{Colors.CYAN}[👑] {Colors.WHITE}DEVELOPER:
{Colors.WHITE}    • Name: kenzzzz11
{Colors.WHITE}    • Discord: kenzzzz11._64163
{Colors.WHITE}    • Experience: 3+ years in cybersecurity

{Colors.CYAN}[📅] {Colors.WHITE}VERSION:
{Colors.WHITE}    • Current: v1.0
{Colors.WHITE}    • Release: {time.strftime('%Y-%m-%d')}
{Colors.WHITE}    • Status: Active Development
"""
            print(about_text)
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