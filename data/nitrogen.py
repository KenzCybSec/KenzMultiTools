import os
import sys
import random
import string
import requests
import json
import time
import threading
from datetime import datetime
from colorama import Fore, Back, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Renkleri başlat - Mor tema
init(autoreset=True)

# Mor renk paleti
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
    RESET = '\033[0m'

def cls():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Nitro Generator Banner"""
    cls()
    banner = f"""
{Colors.LIGHT_PURPLE}
   ███╗   ██╗██╗████████╗██████╗  ██████╗ 
   ████╗  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗
   ██╔██╗ ██║██║   ██║   ██████╔╝██║   ██║
   ██║╚██╗██║██║   ██║   ██╔══██╗██║   ██║
   ██║ ╚████║██║   ██║   ██║  ██║╚██████╔╝
   ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ 
                                           
   ██████╗ ███████╗███╗   ██╗███████╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
   ██╔════╝ ██╔════╝████╗  ██║██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
   ██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██████╔╝███████║   ██║   ██║   ██║██████╔╝
   ██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║   ██║██╔══██╗
   ╚██████╔╝███████╗██║ ╚████║███████╗██║  ██║██║  ██║   ██║   ╚██████╔╝██║  ██║
    ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                                
{Colors.CYAN}
   ╔══════════════════════════════════════════════════════════╗
   ║               DISCORD NITRO GENERATOR           ║
   ║                   Made By Kenz                  ║            
   ╚══════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

class NitroGenerator:
    def __init__(self):
        self.valid_codes = []
        self.invalid_codes = []
        self.checking = False
        self.total_generated = 0
        self.valid_count = 0
        self.driver = None
        self.proxies = []
    
    def setup_driver(self):
        """Selenium WebDriver kurulumu"""
        try:
            print(f"{Colors.CYAN}[*] Setting up Chrome browser for checking...{Colors.RESET}")
            
            options = webdriver.ChromeOptions()
            
            # Anti-detection settings
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Optional: Run in headless mode (background)
            # options.add_argument('--headless')
            # options.add_argument('--no-sandbox')
            # options.add_argument('--disable-dev-shm-usage')
            
            # Disable notifications
            options.add_argument('--disable-notifications')
            
            # Use WebDriver Manager for automatic driver management
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Anti-detection scripts
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            print(f"{Colors.GREEN}[✓] Chrome browser ready for checking{Colors.RESET}")
            return True
            
        except Exception as e:
            print(f"{Colors.RED}[✗] Failed to setup browser: {e}{Colors.RESET}")
            return False
    
    def generate_nitro_code(self):
        """Nitro kodu oluştur"""
        # Discord nitro formatı: https://discord.gift/XXXXXXXXXXXX
        # X = harf veya rakam (büyük harf)
        characters = string.ascii_uppercase + string.digits
        code = ''.join(random.choices(characters, k=16))
        return f"https://discord.gift/{code}"
    
    def generate_batch(self, count=10):
        """Toplu nitro kodu oluştur"""
        print(f"{Colors.CYAN}[*] Generating {count} nitro codes...{Colors.RESET}")
        
        codes = []
        for i in range(count):
            code = self.generate_nitro_code()
            codes.append(code)
            print(f"{Colors.WHITE}[{i+1}/{count}] {code}{Colors.RESET}")
        
        print(f"{Colors.GREEN}[✓] Generated {len(codes)} nitro codes{Colors.RESET}")
        return codes
    
    def check_with_browser(self, code):
        """Tarayıcı ile nitro kodu kontrol et"""
        try:
            # Discord gift redeem sayfasına git
            self.driver.get("https://discord.com/login")
            time.sleep(2)
            
            # Gift sayfasına yönlendir
            gift_url = f"https://discord.com/billing/promotions/{code.split('/')[-1]}"
            self.driver.get(gift_url)
            time.sleep(3)
            
            # Sayfa içeriğini kontrol et
            page_source = self.driver.page_source.lower()
            
            # Valid nitro indicators
            valid_indicators = [
                "nitro",
                "nitro classic",
                "nitro basic",
                "nitro boost",
                "1 month",
                "3 months",
                "claimed",
                "redeem",
                "success",
                "activated"
            ]
            
            # Invalid indicators
            invalid_indicators = [
                "invalid",
                "expired",
                "already redeemed",
                "not found",
                "404",
                "error",
                "failed"
            ]
            
            # Check for valid indicators
            for indicator in valid_indicators:
                if indicator in page_source:
                    # Double-check by looking for specific elements
                    try:
                        # Look for nitro-related elements
                        elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Nitro') or contains(text(), 'nitro')]")
                        if elements:
                            return True
                    except:
                        pass
            
            # Check for invalid indicators
            for indicator in invalid_indicators:
                if indicator in page_source:
                    return False
            
            # If we can't determine, assume invalid
            return False
            
        except Exception as e:
            print(f"{Colors.RED}[!] Browser check error for {code}: {e}{Colors.RESET}")
            return False
    
    def check_with_api(self, code):
        """API ile nitro kodu kontrol et (alternatif yöntem)"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Content-Type': 'application/json'
            }
            
            # Try Discord API endpoint
            response = requests.get(
                f"https://discord.com/api/v9/entitlements/gift-codes/{code.split('/')[-1]}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('uses', 0) < data.get('max_uses', 1):
                    return True
            
            return False
            
        except:
            return None  # API failed
    
    def check_single_code(self, code):
        """Tek bir nitro kodu kontrol et"""
        print(f"{Colors.CYAN}[*] Checking: {code}{Colors.RESET}")
        
        # First try browser check
        if self.driver:
            is_valid = self.check_with_browser(code)
        else:
            # Fallback to API
            is_valid = self.check_with_api(code)
            if is_valid is None:
                print(f"{Colors.YELLOW}[?] Could not check {code}{Colors.RESET}")
                return
        
        if is_valid:
            print(f"{Colors.GREEN}[✓] VALID NITRO CODE: {code}{Colors.RESET}")
            self.valid_codes.append(code)
            self.valid_count += 1
            # Save valid code immediately
            self.save_valid_codes()
        else:
            print(f"{Colors.RED}[✗] INVALID: {code}{Colors.RESET}")
            self.invalid_codes.append(code)
        
        self.total_generated += 1
    
    def mass_check_codes(self, codes, threads=3):
        """Toplu kod kontrolü"""
        print(f"{Colors.CYAN}[*] Starting mass check for {len(codes)} codes...{Colors.RESET}")
        
        self.checking = True
        start_time = time.time()
        
        def check_worker(code_list):
            for code in code_list:
                if not self.checking:
                    break
                self.check_single_code(code)
                time.sleep(random.uniform(1, 3))  # Random delay to avoid detection
        
        # Split codes into threads
        chunk_size = len(codes) // threads
        if chunk_size == 0:
            chunk_size = 1
        
        thread_list = []
        for i in range(threads):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < threads - 1 else len(codes)
            thread_codes = codes[start_idx:end_idx]
            
            if thread_codes:
                thread = threading.Thread(target=check_worker, args=(thread_codes,))
                thread_list.append(thread)
                thread.start()
        
        # Wait for all threads to complete
        for thread in thread_list:
            thread.join()
        
        elapsed = time.time() - start_time
        print(f"\n{Colors.GREEN}[✓] Mass check completed in {elapsed:.1f} seconds{Colors.RESET}")
        print(f"{Colors.CYAN}[📊] Results: {self.valid_count} valid / {len(codes)} total{Colors.RESET}")
    
    def save_valid_codes(self, filename="valid_nitro_codes.txt"):
        """Geçerli kodları kaydet"""
        if not self.valid_codes:
            return
        
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                for code in self.valid_codes:
                    f.write(f"{code}\n")
            
            print(f"{Colors.GREEN}[✓] Valid codes saved to {filename}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[✗] Error saving codes: {e}{Colors.RESET}")
    
    def save_all_codes(self, filename="all_nitro_codes.txt"):
        """Tüm kodları kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=== VALID NITRO CODES ===\n")
                for code in self.valid_codes:
                    f.write(f"{code}\n")
                
                f.write("\n=== INVALID/CHECKED CODES ===\n")
                for code in self.invalid_codes:
                    f.write(f"{code}\n")
            
            print(f"{Colors.GREEN}[✓] All codes saved to {filename}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[✗] Error saving all codes: {e}{Colors.RESET}")
    
    def display_stats(self):
        """İstatistikleri göster"""
        print(f"\n{Colors.LIGHT_PURPLE}{'═'*60}{Colors.RESET}")
        print(f"{Colors.CYAN}         NITRO GENERATOR STATISTICS{Colors.RESET}")
        print(f"{Colors.LIGHT_PURPLE}{'═'*60}{Colors.RESET}")
        
        print(f"{Colors.WHITE}Total Codes Generated: {self.total_generated}{Colors.RESET}")
        print(f"{Colors.GREEN}Valid Codes Found: {self.valid_count}{Colors.RESET}")
        print(f"{Colors.RED}Invalid Codes: {len(self.invalid_codes)}{Colors.RESET}")
        
        if self.total_generated > 0:
            success_rate = (self.valid_count / self.total_generated) * 100
            print(f"{Colors.CYAN}Success Rate: {success_rate:.6f}%{Colors.RESET}")
        
        print(f"{Colors.LIGHT_PURPLE}{'═'*60}{Colors.RESET}")
    
    def cleanup(self):
        """Temizlik"""
        self.checking = False
        
        if self.driver:
            try:
                print(f"{Colors.CYAN}[*] Closing browser...{Colors.RESET}")
                self.driver.quit()
                print(f"{Colors.GREEN}[✓] Browser closed{Colors.RESET}")
            except:
                pass

def main_menu():
    """Ana menü"""
    generator = NitroGenerator()
    
    while True:
        print_banner()
        
        print(f"""
{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗
{Colors.LIGHT_PURPLE}║             MAIN MENU                   ║
{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝
{Colors.CYAN}
   [1] {Colors.WHITE}🎁 Generate Nitro Codes
   [2] {Colors.WHITE}🔍 Check Single Code
   [3] {Colors.WHITE}📊 Mass Code Checker
   [4] {Colors.WHITE}⚡ Auto Generate & Check
   [5] {Colors.WHITE}📁 Save Valid Codes
   [6] {Colors.WHITE}📈 View Statistics
   [7] {Colors.WHITE}⚙️  Setup Browser
   [0] {Colors.WHITE}🚪 Exit
{Colors.RESET}
""")
        
        choice = input(f"{Colors.LIGHT_PURPLE}[?] Select option (0-7): {Colors.WHITE}")
        
        if choice == '0':
            print(f"\n{Colors.CYAN}[*] Goodbye! {Colors.LIGHT_PURPLE}❤{Colors.RESET}\n")
            generator.cleanup()
            break
        
        elif choice == '1':
            # Generate codes
            try:
                count = int(input(f"{Colors.CYAN}[?] How many codes to generate? (1-1000): {Colors.WHITE}"))
                count = max(1, min(count, 1000))
                
                codes = generator.generate_batch(count)
                
                save = input(f"{Colors.CYAN}[?] Save generated codes? (y/n): {Colors.WHITE}").lower()
                if save == 'y':
                    filename = input(f"{Colors.CYAN}[?] Filename (default: generated_codes.txt): {Colors.WHITE}")
                    if not filename:
                        filename = "generated_codes.txt"
                    
                    with open(filename, 'w') as f:
                        for code in codes:
                            f.write(f"{code}\n")
                    
                    print(f"{Colors.GREEN}[✓] Codes saved to {filename}{Colors.RESET}")
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                
            except ValueError:
                print(f"{Colors.RED}[✗] Please enter a valid number{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '2':
            # Check single code
            code = input(f"{Colors.CYAN}[?] Enter Nitro Code (full URL): {Colors.WHITE}").strip()
            
            if not code.startswith("https://discord.gift/"):
                print(f"{Colors.RED}[✗] Invalid format! Use: https://discord.gift/XXXXXXXXXXXX{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                continue
            
            # Setup browser if not already
            if not generator.driver:
                print(f"{Colors.YELLOW}[!] Browser not set up. Setting up now...{Colors.RESET}")
                if not generator.setup_driver():
                    print(f"{Colors.RED}[✗] Browser setup failed. Using API method...{Colors.RESET}")
            
            generator.check_single_code(code)
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '3':
            # Mass checker
            filename = input(f"{Colors.CYAN}[?] Enter filename with codes (one per line): {Colors.WHITE}").strip()
            
            if not os.path.exists(filename):
                print(f"{Colors.RED}[✗] File not found: {filename}{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                continue
            
            try:
                with open(filename, 'r') as f:
                    codes = [line.strip() for line in f if line.strip()]
                
                if not codes:
                    print(f"{Colors.RED}[✗] No codes found in file{Colors.RESET}")
                    input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                    continue
                
                print(f"{Colors.CYAN}[*] Loaded {len(codes)} codes from {filename}{Colors.RESET}")
                
                # Setup browser
                if not generator.driver:
                    print(f"{Colors.YELLOW}[!] Setting up browser for checking...{Colors.RESET}")
                    generator.setup_driver()
                
                threads = input(f"{Colors.CYAN}[?] Number of threads (1-5): {Colors.WHITE}").strip()
                threads = int(threads) if threads.isdigit() else 3
                threads = max(1, min(threads, 5))
                
                generator.mass_check_codes(codes, threads)
                
                # Save results
                save = input(f"\n{Colors.CYAN}[?] Save results? (y/n): {Colors.WHITE}").lower()
                if save == 'y':
                    generator.save_all_codes()
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                
            except Exception as e:
                print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '4':
            # Auto generate & check
            try:
                generate_count = int(input(f"{Colors.CYAN}[?] How many codes to generate and check? (1-100): {Colors.WHITE}"))
                generate_count = max(1, min(generate_count, 100))
                
                threads = input(f"{Colors.CYAN}[?] Number of checking threads (1-3): {Colors.WHITE}").strip()
                threads = int(threads) if threads.isdigit() else 2
                threads = max(1, min(threads, 3))
                
                print(f"{Colors.CYAN}[*] Starting auto generate & check...{Colors.RESET}")
                
                # Generate codes
                codes = []
                for i in range(generate_count):
                    code = generator.generate_nitro_code()
                    codes.append(code)
                    print(f"{Colors.WHITE}[GEN {i+1}/{generate_count}] {code}{Colors.RESET}")
                
                # Setup browser
                if not generator.driver:
                    print(f"{Colors.YELLOW}[!] Setting up browser...{Colors.RESET}")
                    generator.setup_driver()
                
                # Check codes
                generator.mass_check_codes(codes, threads)
                
                # Save results
                generator.save_all_codes("auto_generated_results.txt")
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                
            except ValueError:
                print(f"{Colors.RED}[✗] Please enter valid numbers{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '5':
            # Save valid codes
            if generator.valid_codes:
                filename = input(f"{Colors.CYAN}[?] Filename (default: valid_nitro_codes.txt): {Colors.WHITE}")
                if not filename:
                    filename = "valid_nitro_codes.txt"
                
                generator.save_valid_codes(filename)
            else:
                print(f"{Colors.YELLOW}[!] No valid codes to save{Colors.RESET}")
            
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '6':
            # View statistics
            generator.display_stats()
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '7':
            # Setup browser
            if generator.driver:
                print(f"{Colors.YELLOW}[!] Browser already set up. Recreating...{Colors.RESET}")
                generator.cleanup()
                time.sleep(1)
            
            if generator.setup_driver():
                print(f"{Colors.GREEN}[✓] Browser setup complete{Colors.RESET}")
            else:
                print(f"{Colors.RED}[✗] Browser setup failed{Colors.RESET}")
            
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        else:
            print(f"{Colors.RED}[✗] Invalid option!{Colors.RESET}")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}[*] Program interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)