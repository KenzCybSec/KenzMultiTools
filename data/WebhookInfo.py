import os
import sys
import json
import requests
import time
from datetime import datetime
from colorama import Fore, Back, Style, init

# Renkleri başlat
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
    BOLD = '\033[1m'

def cls():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Webhook Information Banner"""
    cls()
    banner = f"""
{Colors.LIGHT_PURPLE}
 █     █░▓█████  ▄▄▄▄    ██░ ██  ▒█████   ▒█████   ██ ▄█▀ ██▓ ███▄    █   █████▒▒█████  
▓█░ █ ░█░▓█   ▀ ▓█████▄ ▓██░ ██▒▒██▒  ██▒▒██▒  ██▒ ██▄█▒ ▓██▒ ██ ▀█   █ ▓██   ▒▒██▒  ██▒
▒█░ █ ░█ ▒███   ▒██▒ ▄██▒██▀▀██░▒██░  ██▒▒██░  ██▒▓███▄░ ▒██▒▓██  ▀█ ██▒▒████ ░▒██░  ██▒
░█░ █ ░█ ▒▓█  ▄ ▒██░█▀  ░▓█ ░██ ▒██   ██░▒██   ██░▓██ █▄ ░██░▓██▒  ▐▌██▒░▓█▒  ░▒██   ██░
░░██▒██▓ ░▒████▒░▓█  ▀█▓░▓█▒░██▓░ ████▓▒░░ ████▓▒░▒██▒ █▄░██░▒██░   ▓██░░▒█░   ░ ████▓▒░
░ ▓░▒ ▒  ░░ ▒░ ░░▒▓███▀▒ ▒ ░░▒░▒░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░▓  ░ ▒░   ▒ ▒  ▒ ░   ░ ▒░▒░▒░ 
  ▒ ░ ░   ░ ░  ░▒░▒   ░  ▒ ░▒░ ░  ░ ▒ ▒░   ░ ▒ ▒░ ░ ░▒ ▒░ ▒ ░░ ░░   ░ ▒░ ░       ░ ▒ ▒░ 
  ░   ░     ░    ░    ░  ░  ░░ ░░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░░ ░  ▒ ░   ░   ░ ░  ░ ░   ░ ░ ░ ▒  
    ░       ░  ░ ░       ░  ░  ░    ░ ░      ░ ░  ░  ░    ░           ░            ░ ░  
                      ░                                                                 
                                                                
    ╔══════════════════════════════════════════════════════════╗
    ║         WEBHOOK INFORMATION SCANNER                ║
    ║               Made By Kenz                         ║
    ╚══════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

def check_webhook_url(url):
    """Webhook URL formatını kontrol et"""
    if not url.startswith("https://discord.com/api/webhooks/"):
        return False
    
    parts = url.split('/')
    if len(parts) < 7:
        return False
    
    webhook_id = parts[5]
    webhook_token = parts[6]
    
    # ID ve token format kontrolü
    if len(webhook_id) != 19 or not webhook_id.isdigit():
        return False
    
    if len(webhook_token) < 60:  # Discord tokenları genelde 68 karakter
        return False
    
    return True

def calculate_time_ago(timestamp):
    """Zaman farkını hesapla"""
    now = datetime.now().timestamp()
    diff = now - timestamp
    
    if diff < 60:
        return f"({int(diff)} seconds ago)"
    elif diff < 3600:
        return f"({int(diff/60)} minutes ago)"
    elif diff < 86400:
        return f"({int(diff/3600)} hours ago)"
    elif diff < 2592000:
        return f"({int(diff/86400)} days ago)"
    else:
        return f"({int(diff/2592000)} months ago)"

def info_webhook(webhook_url):
    """Webhook bilgilerini al ve göster"""
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        print(f"{Colors.CYAN}[*] Fetching webhook information...{Colors.RESET}")
        response = requests.get(webhook_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"{Colors.RED}[✗] Webhook not found or invalid (HTTP {response.status_code}){Colors.RESET}")
            
            if response.status_code == 404:
                print(f"{Colors.YELLOW}[!] The webhook might have been deleted{Colors.RESET}")
            elif response.status_code == 429:
                print(f"{Colors.YELLOW}[!] Rate limited - Try again later{Colors.RESET}")
            elif response.status_code == 403:
                print(f"{Colors.YELLOW}[!] Access forbidden - Invalid permissions{Colors.RESET}")
            
            return
        
        webhook_info = response.json()

        # Webhook basic information
        webhook_id = webhook_info.get('id', "❌ None")
        webhook_token = webhook_info.get('token', "❌ None")
        webhook_name = webhook_info.get('name', "❌ None")
        webhook_avatar = webhook_info.get('avatar', "❌ None")
        
        # Webhook type
        webhook_type_code = webhook_info.get('type', 1)
        if webhook_type_code == 1:
            webhook_type = f"{Colors.GREEN}🤖 Bot Webhook{Colors.RESET}"
        elif webhook_type_code == 2:
            webhook_type = f"{Colors.CYAN}👤 User Webhook{Colors.RESET}"
        else:
            webhook_type = f"{Colors.YELLOW}❓ Unknown ({webhook_type_code}){Colors.RESET}"
        
        channel_id = webhook_info.get('channel_id', "❌ None")
        guild_id = webhook_info.get('guild_id', "❌ None")
        
        # Webhook creation time
        created_ago = ""
        if webhook_id != "❌ None" and webhook_id.isdigit():
            snowflake = int(webhook_id)
            timestamp = ((snowflake >> 22) + 1420070400000) / 1000
            created_at = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            created_ago = calculate_time_ago(timestamp)
        else:
            created_at = "❌ Unknown"

        print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
        print(f"{Colors.LIGHT_PURPLE}║         WEBHOOK BASIC INFORMATION        ║")
        print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}[🆔] Webhook ID: {Colors.WHITE}{webhook_id}")
        print(f"{Colors.CYAN}[🔑] Token: {Colors.WHITE}{webhook_token}")
        print(f"{Colors.CYAN}[📛] Name: {Colors.WHITE}{webhook_name}")
        print(f"{Colors.CYAN}[🎭] Type: {webhook_type}")
        print(f"{Colors.CYAN}[📅] Created: {Colors.WHITE}{created_at} {created_ago}")
        print(f"{Colors.CYAN}[💬] Channel ID: {Colors.WHITE}{channel_id}")
        print(f"{Colors.CYAN}[🏰] Server ID: {Colors.WHITE}{guild_id}")
        
        # Avatar URL
        if webhook_avatar and webhook_avatar != "❌ None":
            avatar_url = f"https://cdn.discordapp.com/avatars/{webhook_id}/{webhook_avatar}.png?size=256"
            print(f"{Colors.CYAN}[🖼️] Avatar URL: {Colors.WHITE}{avatar_url}")
        
        print(f"\n{Colors.CYAN}[🔗] Webhook URL: {Colors.WHITE}{webhook_url}")
        
        # Test webhook
        print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
        print(f"{Colors.LIGHT_PURPLE}║              TEST WEBHOOK                ║")
        print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
        
        test_choice = input(f"\n{Colors.CYAN}[?] Test webhook with a message? (y/n): {Colors.WHITE}").lower()
        
        if test_choice == 'y':
            test_message = input(f"{Colors.CYAN}[?] Test message: {Colors.WHITE}")
            
            test_payload = {
                'content': test_message,
                'username': 'Webhook Tester',
                'avatar_url': 'https://cdn.discordapp.com/attachments/1049854308549726289/1050922249776984115/4b19e2d99e9085b56cdc.png'
            }
            
            try:
                test_response = requests.post(webhook_url, json=test_payload, timeout=10)
                
                if test_response.status_code in [200, 204]:
                    print(f"{Colors.GREEN}[✓] Test message sent successfully!{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[✗] Failed to send test message (HTTP {test_response.status_code}){Colors.RESET}")
                    
            except requests.exceptions.Timeout:
                print(f"{Colors.RED}[✗] Request timeout{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
        
        # Creator information
        if 'user' in webhook_info:
            user_info = webhook_info['user']
            
            print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
            print(f"{Colors.LIGHT_PURPLE}║          CREATOR INFORMATION              ║")
            print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
            
            user_id = user_info.get('id', "❌ None")
            username = user_info.get('username', "❌ None")
            display_name = user_info.get('global_name', "❌ None")
            discriminator = user_info.get('discriminator', "❌ None")
            
            # Format username
            if discriminator != "❌ None" and discriminator != "0":
                full_username = f"{username}#{discriminator}"
            else:
                full_username = username
            
            user_avatar = user_info.get('avatar', "❌ None")
            user_flags = user_info.get('flags', 0)
            accent_color = user_info.get('accent_color')
            banner_color = user_info.get('banner_color')
            
            print(f"\n{Colors.CYAN}[👤] User ID: {Colors.WHITE}{user_id}")
            print(f"{Colors.CYAN}[📛] Username: {Colors.WHITE}{full_username}")
            
            if display_name != "❌ None":
                print(f"{Colors.CYAN}[🏷️] Display Name: {Colors.WHITE}{display_name}")
            
            # User badges
            badges = []
            if user_flags != 0:
                badge_dict = {
                    1 << 0: "🏆 Staff",
                    1 << 1: "🤝 Partner",
                    1 << 2: "🎖️ Hypesquad",
                    1 << 3: "🐛 Bug Hunter",
                    1 << 6: "🏅 Hypesquad Bravery",
                    1 << 7: "💚 Hypesquad Brilliance", 
                    1 << 8: "❤️ Hypesquad Balance",
                    1 << 9: "💎 Early Supporter",
                    1 << 14: "✅ Bug Hunter Gold",
                    1 << 16: "⚡ Verified Bot",
                    1 << 17: "🔷 Early Verified Bot",
                    1 << 18: "❌ Deleted",
                    1 << 19: "👑 Certified Mod"
                }
                
                for flag, badge in badge_dict.items():
                    if user_flags & flag:
                        badges.append(badge)
            
            if badges:
                print(f"{Colors.CYAN}[🎖️] Badges: {Colors.WHITE}{', '.join(badges)}")
            
            if accent_color:
                print(f"{Colors.CYAN}[🎨] Accent Color: {Colors.WHITE}#{accent_color:06x}")
            
            if banner_color:
                print(f"{Colors.CYAN}[🚩] Banner Color: {Colors.WHITE}#{banner_color:06x}")
            
            # Avatar URL
            if user_avatar != "❌ None":
                user_avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_avatar}.png?size=256"
                print(f"{Colors.CYAN}[🖼️] Avatar URL: {Colors.WHITE}{user_avatar_url}")
            
            # Banner URL
            if banner := user_info.get('banner'):
                banner_url = f"https://cdn.discordapp.com/banners/{user_id}/{banner}.png?size=600"
                print(f"{Colors.CYAN}[🚩] Banner URL: {Colors.WHITE}{banner_url}")
        
        # Additional actions
        while True:
            print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
            print(f"{Colors.LIGHT_PURPLE}║           ADDITIONAL ACTIONS              ║")
            print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
            
            print(f"\n{Colors.CYAN}1. {Colors.WHITE}Delete this webhook")
            print(f"{Colors.CYAN}2. {Colors.WHITE}Rename this webhook")
            print(f"{Colors.CYAN}3. {Colors.WHITE}Change webhook avatar")
            print(f"{Colors.CYAN}4. {Colors.WHITE}Send embed message")
            print(f"{Colors.CYAN}5. {Colors.WHITE}Spam webhook (careful!)")
            print(f"{Colors.CYAN}6. {Colors.WHITE}Get webhook info again")
            print(f"{Colors.CYAN}7. {Colors.WHITE}Back to main menu")
            
            action = input(f"\n{Colors.CYAN}[?] Select action (1-7): {Colors.WHITE}")
            
            if action == '1':
                confirm = input(f"{Colors.RED}[!] Are you sure you want to delete this webhook? (y/n): {Colors.WHITE}").lower()
                if confirm == 'y':
                    try:
                        delete_response = requests.delete(webhook_url, timeout=10)
                        if delete_response.status_code in [200, 204]:
                            print(f"{Colors.GREEN}[✓] Webhook deleted successfully!{Colors.RESET}")
                            break
                        else:
                            print(f"{Colors.RED}[✗] Failed to delete webhook (HTTP {delete_response.status_code}){Colors.RESET}")
                    except Exception as e:
                        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
            
            elif action == '2':
                new_name = input(f"{Colors.CYAN}[?] New webhook name: {Colors.WHITE}")
                rename_payload = {'name': new_name}
                
                try:
                    rename_response = requests.patch(webhook_url, json=rename_payload, timeout=10)
                    
                    if rename_response.status_code == 200:
                        print(f"{Colors.GREEN}[✓] Webhook renamed to '{new_name}'{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}[✗] Failed to rename webhook{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
            
            elif action == '3':
                avatar_url = input(f"{Colors.CYAN}[?] New avatar URL: {Colors.WHITE}")
                avatar_payload = {'avatar': avatar_url}
                
                try:
                    avatar_response = requests.patch(webhook_url, json=avatar_payload, timeout=10)
                    
                    if avatar_response.status_code == 200:
                        print(f"{Colors.GREEN}[✓] Webhook avatar updated{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}[✗] Failed to update avatar{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
            
            elif action == '4':
                embed_title = input(f"{Colors.CYAN}[?] Embed title: {Colors.WHITE}")
                embed_desc = input(f"{Colors.CYAN}[?] Embed description: {Colors.WHITE}")
                
                embed = {
                    "title": embed_title,
                    "description": embed_desc,
                    "color": 0x9b59b6,  # Purple color
                    "timestamp": datetime.now().isoformat(),
                    "footer": {
                        "text": "Webhook Information Tool"
                    }
                }
                
                embed_payload = {
                    "embeds": [embed],
                    "username": "Embed Sender"
                }
                
                try:
                    embed_response = requests.post(webhook_url, json=embed_payload, timeout=10)
                    
                    if embed_response.status_code in [200, 204]:
                        print(f"{Colors.GREEN}[✓] Embed sent successfully!{Colors.RESET}")
                    else:
                        print(f"{Colors.RED}[✗] Failed to send embed{Colors.RESET}")
                except Exception as e:
                    print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
            
            elif action == '5':
                spam_msg = input(f"{Colors.CYAN}[?] Spam message: {Colors.WHITE}")
                spam_count = input(f"{Colors.CYAN}[?] Number of messages (1-50): {Colors.WHITE}")
                
                try:
                    spam_count = int(spam_count)
                    spam_count = max(1, min(spam_count, 50))
                    
                    print(f"{Colors.YELLOW}[!] WARNING: This may get the webhook rate-limited or banned!{Colors.RESET}")
                    confirm = input(f"{Colors.RED}[!] Continue? (y/n): {Colors.WHITE}").lower()
                    
                    if confirm == 'y':
                        print(f"{Colors.YELLOW}[!] Starting spam... (CTRL+C to stop){Colors.RESET}")
                        
                        sent = 0
                        for i in range(spam_count):
                            try:
                                spam_response = requests.post(webhook_url, json={'content': spam_msg}, timeout=5)
                                if spam_response.status_code in [200, 204]:
                                    sent += 1
                                    print(f"{Colors.GREEN}[{i+1}/{spam_count}] Message sent{Colors.RESET}")
                                else:
                                    print(f"{Colors.RED}[{i+1}/{spam_count}] Failed (HTTP {spam_response.status_code}){Colors.RESET}")
                                time.sleep(0.5)
                            except KeyboardInterrupt:
                                print(f"{Colors.YELLOW}[!] Spam stopped by user{Colors.RESET}")
                                break
                            except:
                                print(f"{Colors.RED}[{i+1}/{spam_count}] Error{Colors.RESET}")
                        
                        print(f"{Colors.CYAN}[📊] Sent {sent}/{spam_count} messages{Colors.RESET}")
                    else:
                        print(f"{Colors.CYAN}[*] Spam cancelled{Colors.RESET}")
                        
                except ValueError:
                    print(f"{Colors.RED}[✗] Please enter a valid number{Colors.RESET}")
            
            elif action == '6':
                # Get info again
                print(f"{Colors.CYAN}[*] Refreshing webhook information...{Colors.RESET}")
                info_webhook(webhook_url)
                return
            
            elif action == '7':
                print(f"{Colors.CYAN}[*] Returning to main menu...{Colors.RESET}")
                return
            
            else:
                print(f"{Colors.RED}[✗] Invalid selection{Colors.RESET}")
        
    except requests.exceptions.Timeout:
        print(f"{Colors.RED}[✗] Request timeout - Webhook might be invalid or rate-limited{Colors.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}[✗] Network error: {e}{Colors.RESET}")
    except json.JSONDecodeError:
        print(f"{Colors.RED}[✗] Invalid response from webhook{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")

def main():
    """Ana program"""
    while True:
        try:
            print_banner()
            
            print(f"{Colors.CYAN}[*] Enter Discord Webhook URL{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Format: https://discord.com/api/webhooks/ID/TOKEN{Colors.RESET}")
            
            webhook_url = input(f"\n{Colors.LIGHT_PURPLE}[?] Webhook URL -> {Colors.WHITE}").strip()
            
            if not webhook_url:
                print(f"{Colors.RED}[✗] No URL entered{Colors.RESET}")
                time.sleep(1)
                continue
            
            # Validate URL
            if not check_webhook_url(webhook_url):
                print(f"{Colors.RED}[✗] Invalid Discord webhook URL format!{Colors.RESET}")
                print(f"{Colors.YELLOW}[!] Please check the URL and try again{Colors.RESET}")
                time.sleep(2)
                continue
            
            # Get webhook info
            info_webhook(webhook_url)
            
            # Ask if user wants to check another webhook
            print(f"\n{Colors.LIGHT_PURPLE}{'═'*60}{Colors.RESET}")
            another = input(f"{Colors.CYAN}[?] Check another webhook? (y/n): {Colors.WHITE}").lower()
            
            if another != 'y':
                print(f"\n{Colors.GREEN}[✓] Thank you for using Webhook Information Tool!{Colors.RESET}")
                print(f"{Colors.LIGHT_PURPLE}[❤] Goodbye!{Colors.RESET}\n")
                break
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[!] Program interrupted by user{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}[✗] Unexpected error: {e}{Colors.RESET}")
            time.sleep(2)

if __name__ == "__main__":
    # Gerekli modül kontrolü
    try:
        import requests
    except ImportError:
        print(f"{Colors.RED}[✗] 'requests' module not installed!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Please install it with: pip install requests{Colors.RESET}")
        sys.exit(1)
    
    try:
        import colorama
    except ImportError:
        print(f"{Colors.RED}[✗] 'colorama' module not installed!{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Please install it with: pip install colorama{Colors.RESET}")
        sys.exit(1)
    
    # Programı başlat
    main()