import requests
import time
import json
import os
from colorama import Fore, Back, Style, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Initialize colorama with custom colors
init(autoreset=True)

# Custom color definitions for light purple theme
class Colors:
    PRIMARY = '\033[95m'  # Light Purple
    SECONDARY = '\033[96m'  # Light Cyan
    SUCCESS = '\033[92m'  # Light Green
    WARNING = '\033[93m'  # Light Yellow
    ERROR = '\033[91m'  # Light Red
    INFO = '\033[94m'  # Light Blue
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    """Display the ASCII art banner"""
    banner = f"""{Colors.PRIMARY}
 _________  ________  ___  __    _______   ________   ___       ________  ________  ___  ________      
|\___   ___\\   __  \|\  \|\  \ |\  ___ \ |\   ___  \|\  \     |\   __  \|\   ____\|\  \|\   ___  \    
\|___ \  \_\ \  \|\  \ \  \/  /|\ \   __/|\ \  \\ \  \ \  \    \ \  \|\  \ \  \___|\ \  \ \  \\ \  \   
     \ \  \ \ \  \\\  \ \   ___  \ \  \_|/_\ \  \\ \  \ \  \    \ \  \\\  \ \  \  __\ \  \ \  \\ \  \  
      \ \  \ \ \  \\\  \ \  \\ \  \ \  \_|\ \ \  \\ \  \ \  \____\ \  \\\  \ \  \|\  \ \  \ \  \\ \  \ 
       \ \__\ \ \_______\ \__\\ \__\ \_______\ \__\\ \__\ \_______\ \_______\ \_______\ \__\ \__\\ \__\
        \|__|  \|_______|\|__| \|__|\|_______|\|__| \|__|\|_______|\|_______|\|_______|\|__|\|__| \|__|
    {Colors.END}"""
    
    info = f"""{Colors.SECONDARY}
    ╔══════════════════════════════════════════════════════════╗
    ║                   DISCORD TOKEN LOGIN             ║
    ║                     Created By Kenz               ║
    ╚══════════════════════════════════════════════════════════╝{Colors.END}"""
    
    print(banner)
    print(info)
    print(f"{Colors.PRIMARY}{'═'*70}{Colors.END}\n")

class DiscordTokenLogin:
    def __init__(self):
        self.driver = None
        self.token = None
        self.user_info = None
        self.browser_type = "chrome"
        
    def get_headers(self, token):
        """Generate headers with token"""
        return {
            'Authorization': str(token),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    
    def validate_token(self, token):
        """Validate Discord token and get user information"""
        try:
            headers = self.get_headers(token)
            response = requests.get(
                'https://discord.com/api/v9/users/@me',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                self.user_info = {
                    'username': f"{user_data.get('username', 'Unknown')}#{user_data.get('discriminator', '0000')}",
                    'id': user_data.get('id'),
                    'email': user_data.get('email'),
                    'phone': user_data.get('phone'),
                    'verified': user_data.get('verified', False),
                    'mfa_enabled': user_data.get('mfa_enabled', False),
                    'premium_type': user_data.get('premium_type', 0),
                    'avatar': user_data.get('avatar'),
                    'banner': user_data.get('banner'),
                    'accent_color': user_data.get('accent_color')
                }
                return True
            else:
                print(f"{Colors.ERROR}[✗] Token validation failed: HTTP {response.status_code}{Colors.END}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"{Colors.ERROR}[✗] Network error: {e}{Colors.END}")
            return False
        except json.JSONDecodeError:
            print(f"{Colors.ERROR}[✗] Invalid response from Discord API{Colors.END}")
            return False
    
    def display_user_info(self):
        """Display user information in a formatted way"""
        if not self.user_info:
            return
        
        print(f"\n{Colors.SUCCESS}{'═'*50}")
        print(f"{Colors.SUCCESS}         ACCOUNT INFORMATION")
        print(f"{Colors.SUCCESS}{'═'*50}{Colors.END}")
        
        info = self.user_info
        nitro_status = {
            0: "None",
            1: "Nitro Classic",
            2: "Nitro Booster", 
            3: "Nitro Full"
        }.get(info['premium_type'], "Unknown")
        
        print(f"{Colors.INFO}👤 Username: {Colors.PRIMARY}{info['username']}{Colors.END}")
        print(f"{Colors.INFO}🆔 User ID: {Colors.SECONDARY}{info['id']}{Colors.END}")
        print(f"{Colors.INFO}📧 Email: {Colors.SECONDARY}{info.get('email', 'Not available')}{Colors.END}")
        print(f"{Colors.INFO}📱 Phone: {Colors.SECONDARY}{info.get('phone', 'Not available')}{Colors.END}")
        print(f"{Colors.INFO}💎 Nitro: {Colors.PRIMARY}{nitro_status}{Colors.END}")
        print(f"{Colors.INFO}✅ Verified: {Colors.SUCCESS if info['verified'] else Colors.ERROR}{'Yes' if info['verified'] else 'No'}{Colors.END}")
        print(f"{Colors.INFO}🔒 2FA: {Colors.SUCCESS if info['mfa_enabled'] else Colors.WARNING}{'Enabled' if info['mfa_enabled'] else 'Disabled'}{Colors.END}")
        
        if info.get('avatar'):
            avatar_url = f"https://cdn.discordapp.com/avatars/{info['id']}/{info['avatar']}.png"
            print(f"{Colors.INFO}🖼️ Avatar: {Colors.SECONDARY}{avatar_url}{Colors.END}")
        
        print(f"{Colors.SUCCESS}{'═'*50}{Colors.END}\n")
    
    def setup_chrome_driver(self):
        """Setup Chrome WebDriver"""
        try:
            print(f"{Colors.INFO}[*] Setting up Chrome driver...{Colors.END}")
            
            options = webdriver.ChromeOptions()
            
            # Chrome configuration
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Optional: Run in headless mode (remove for debugging)
            # options.add_argument('--headless')
            # options.add_argument('--no-sandbox')
            # options.add_argument('--disable-dev-shm-usage')
            
            # Disable notifications
            options.add_argument('--disable-notifications')
            
            # Use WebDriver Manager to handle driver automatically
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Execute CDP commands to prevent detection
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.browser_type = "chrome"
            print(f"{Colors.SUCCESS}[✓] Chrome driver initialized successfully{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.ERROR}[✗] Chrome setup failed: {e}{Colors.END}")
            return False
    
    def setup_edge_driver(self):
        """Setup Microsoft Edge WebDriver"""
        try:
            print(f"{Colors.INFO}[*] Setting up Edge driver...{Colors.END}")
            
            options = webdriver.EdgeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-notifications')
            
            service = EdgeService(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=options)
            
            self.browser_type = "edge"
            print(f"{Colors.SUCCESS}[✓] Edge driver initialized successfully{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.ERROR}[✗] Edge setup failed: {e}{Colors.END}")
            return False
    
    def setup_firefox_driver(self):
        """Setup Firefox WebDriver"""
        try:
            print(f"{Colors.INFO}[*] Setting up Firefox driver...{Colors.END}")
            
            options = webdriver.FirefoxOptions()
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference('useAutomationExtension', False)
            options.set_preference("dom.push.enabled", False)
            
            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)
            
            self.browser_type = "firefox"
            print(f"{Colors.SUCCESS}[✓] Firefox driver initialized successfully{Colors.END}")
            return True
            
        except Exception as e:
            print(f"{Colors.ERROR}[✗] Firefox setup failed: {e}{Colors.END}")
            return False
    
    def inject_token_via_js(self):
        """Inject token into Discord using JavaScript"""
        if not self.driver or not self.token:
            return False
        
        try:
            # Navigate to Discord login page
            print(f"{Colors.INFO}[*] Opening Discord login page...{Colors.END}")
            self.driver.get("https://discord.com/login")
            time.sleep(2)
            
            # JavaScript to inject token
            script = f"""
            function login(token) {{
                setInterval(() => {{
                    document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
                }}, 50);
                setTimeout(() => {{
                    location.reload();
                }}, 2500);
            }}
            login("{self.token}");
            """
            
            # Execute the script
            print(f"{Colors.INFO}[*] Injecting token...{Colors.END}")
            self.driver.execute_script(script)
            time.sleep(3)
            
            # Wait for page to reload and check if login was successful
            print(f"{Colors.INFO}[*] Waiting for login to complete...{Colors.END}")
            
            # Try multiple ways to detect successful login
            try:
                # Wait for either the main app to load or stay on login page
                wait = WebDriverWait(self.driver, 10)
                
                # Check if we're on channels page (successful login)
                if "channels" in self.driver.current_url or "@me" in self.driver.current_url:
                    print(f"{Colors.SUCCESS}[✓] Successfully logged in as {self.user_info['username']}{Colors.END}")
                    return True
                
                # Check for user avatar (another indicator of login)
                elements = self.driver.find_elements(By.CSS_SELECTOR, '[class*="avatar"], [data-testid*="user"], img[src*="avatars"]')
                if elements:
                    print(f"{Colors.SUCCESS}[✓] Successfully logged in as {self.user_info['username']}{Colors.END}")
                    return True
                
                # Check page title
                if "Discord" in self.driver.title and "Login" not in self.driver.title:
                    print(f"{Colors.SUCCESS}[✓] Successfully logged in as {self.user_info['username']}{Colors.END}")
                    return True
                    
            except:
                pass
            
            # If we're still here, login might have failed
            current_url = self.driver.current_url
            if "login" in current_url:
                print(f"{Colors.WARNING}[!] Still on login page. Trying alternative method...{Colors.END}")
                return self.try_alternative_login()
            
            return True
            
        except Exception as e:
            print(f"{Colors.ERROR}[✗] Error during token injection: {e}{Colors.END}")
            return False
    
    def try_alternative_login(self):
        """Try alternative login methods"""
        try:
            # Alternative method 1: Direct local storage injection
            print(f"{Colors.INFO}[*] Trying alternative method 1...{Colors.END}")
            script2 = f"""
            localStorage.token = "{self.token}";
            localStorage.token = `"{self.token}"`;
            """
            self.driver.execute_script(script2)
            self.driver.refresh()
            time.sleep(3)
            
            # Alternative method 2: Using document.domain
            if "login" in self.driver.current_url:
                print(f"{Colors.INFO}[*] Trying alternative method 2...{Colors.END}")
                script3 = f"""
                window.localStorage.token = `"{self.token}"`;
                window.location.href = "https://discord.com/app";
                """
                self.driver.execute_script(script3)
                time.sleep(3)
            
            # Check if successful
            if "channels" in self.driver.current_url or "@me" in self.driver.current_url:
                print(f"{Colors.SUCCESS}[✓] Login successful with alternative method{Colors.END}")
                return True
            
            return False
            
        except Exception as e:
            print(f"{Colors.ERROR}[✗] Alternative method failed: {e}{Colors.END}")
            return False
    
    def manual_login_instructions(self):
        """Show manual login instructions"""
        print(f"\n{Colors.WARNING}{'═'*60}")
        print(f"{Colors.WARNING}          MANUAL LOGIN INSTRUCTIONS")
        print(f"{Colors.WARNING}{'═'*60}{Colors.END}")
        
        print(f"\n{Colors.INFO}If automatic login failed, follow these steps:{Colors.END}")
        print(f"{Colors.SECONDARY}1. Open {Colors.PRIMARY}https://discord.com/login{Colors.SECONDARY} in your browser{Colors.END}")
        print(f"{Colors.SECONDARY}2. Open Developer Console (F12){Colors.END}")
        print(f"{Colors.SECONDARY}3. Go to Console tab{Colors.END}")
        print(f"{Colors.SECONDARY}4. Paste this code and press Enter:{Colors.END}")
        
        manual_script = f"""
{Colors.PRIMARY}function login(token) {{
    setInterval(() => {{
        document.body.appendChild(document.createElement('iframe')).contentWindow.localStorage.token = `"${{token}}"`;
    }}, 50);
    setTimeout(() => {{
        location.reload();
    }}, 2500);
}}
login("{self.token}");{Colors.END}
        """
        
        print(f"\n{Colors.PRIMARY}{manual_script}{Colors.END}")
        print(f"\n{Colors.SUCCESS}5. Wait for page to reload automatically{Colors.END}")
        print(f"{Colors.WARNING}{'═'*60}{Colors.END}\n")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            try:
                print(f"{Colors.INFO}[*] Closing browser...{Colors.END}")
                self.driver.quit()
                print(f"{Colors.SUCCESS}[✓] Browser closed{Colors.END}")
            except:
                pass
    
    def run(self):
        """Main execution function"""
        print_banner()
        
        # Get token from user
        print(f"{Colors.PRIMARY}[?] Enter Discord Token: {Colors.END}", end="")
        self.token = input().strip()
        
        if not self.token:
            print(f"{Colors.ERROR}[✗] No token provided{Colors.END}")
            return
        
        # Validate token
        print(f"{Colors.INFO}[*] Validating token...{Colors.END}")
        if not self.validate_token(self.token):
            print(f"{Colors.ERROR}[✗] Invalid or expired token{Colors.END}")
            return
        
        # Display user info
        self.display_user_info()
        
        # Ask for browser selection
        print(f"{Colors.PRIMARY}[?] Select browser:")
        print(f"{Colors.SECONDARY}1. Chrome (Recommended)")
        print(f"{Colors.SECONDARY}2. Microsoft Edge")
        print(f"{Colors.SECONDARY}3. Firefox")
        print(f"{Colors.ERROR}4. Manual Login Instructions Only{Colors.END}")
        
        choice = input(f"\n{Colors.PRIMARY}Select option (1-4): {Colors.END}").strip()
        
        success = False
        
        if choice == '1':
            if self.setup_chrome_driver():
                success = self.inject_token_via_js()
        elif choice == '2':
            if self.setup_edge_driver():
                success = self.inject_token_via_js()
        elif choice == '3':
            if self.setup_firefox_driver():
                success = self.inject_token_via_js()
        elif choice == '4':
            self.manual_login_instructions()
            success = True
        else:
            print(f"{Colors.ERROR}[✗] Invalid selection{Colors.END}")
        
        # If automatic login failed, show manual instructions
        if not success and choice in ['1', '2', '3']:
            print(f"{Colors.WARNING}[!] Automatic login failed. Showing manual instructions...{Colors.END}")
            self.manual_login_instructions()
        
        # Keep browser open if login was successful
        if success and self.driver and choice in ['1', '2', '3']:
            print(f"\n{Colors.SUCCESS}[✓] Browser is now open with logged in session")
            print(f"{Colors.INFO}[*] Press Ctrl+C in this terminal to close the browser{Colors.END}")
            try:
                # Keep the script running
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{Colors.INFO}[*] Closing...{Colors.END}")
        
        # Cleanup
        self.cleanup()
        
        print(f"\n{Colors.SUCCESS}{'═'*60}")
        print(f"{Colors.SUCCESS}           PROCESS COMPLETED")
        print(f"{Colors.SUCCESS}{'═'*60}{Colors.END}")

# Main execution
if __name__ == "__main__":
    try:
        login_tool = DiscordTokenLogin()
        login_tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Program interrupted by user{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.ERROR}[✗] Unexpected error: {e}{Colors.END}")