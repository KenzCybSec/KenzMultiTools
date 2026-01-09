# Shrek was proudly coded by Shrek™ [https://github.com/SHREK-TM].
# Copyright © Shrek Multi Tools

####################################################################

import os
import sys
import requests
import json
import webbrowser
from time import sleep
from datetime import datetime
from colorama import Fore, Back, Style, init

# Renkleri başlat ve mor tema ayarla
init(autoreset=True)

# Mor renk paleti
class Colors:
    PURPLE = '\033[95m'
    LIGHT_PURPLE = '\033[95m'
    DARK_PURPLE = '\033[35m'
    CYAN = '\033[96m'
    LIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    RESET = '\033[0m'

def cls():
    """Ekranı temizle"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Mor tema banner"""
    cls()
    banner = f"""
{Colors.LIGHT_PURPLE}
  ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗  ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                                                          
                                                        

{Colors.RESET}
"""
    print(banner)

def print_menu():
    """Ana menüyü göster"""
    print(f"""
{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗
{Colors.LIGHT_PURPLE}║               MAIN MENU                  ║
{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝
{Colors.CYAN}
   [1] {Colors.WHITE}🔍 Server Lookup
   [2] {Colors.WHITE}👥 Member Statistics
   [3] {Colors.WHITE}📊 Channel Analyzer
   [4] {Colors.WHITE}🎭 Role Information
   [5] {Colors.WHITE}📁 Export Server Data
   [6] {Colors.WHITE}🔄 Token Checker
   [0] {Colors.WHITE}🚪 Exit
{Colors.RESET}
""")

def get_user_headers(token):
    """Kullanıcı bilgileri için headers oluştur"""
    return {
        'Authorization': token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

def validate_token(token):
    """Token geçerliliğini kontrol et"""
    try:
        headers = get_user_headers(token)
        response = requests.get(
            'https://discord.com/api/v9/users/@me',
            headers=headers,
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def get_user_info(token):
    """Kullanıcı bilgilerini al"""
    try:
        headers = get_user_headers(token)
        response = requests.get(
            'https://discord.com/api/v9/users/@me',
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except:
        return None
    return None

def get_guild_info(token, guild_id):
    """Sunucu bilgilerini al"""
    try:
        headers = get_user_headers(token)
        response = requests.get(
            f'https://discord.com/api/v9/guilds/{guild_id}',
            headers=headers,
            params={'with_counts': True}
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
    return None

def get_guild_members(token, guild_id, limit=100):
    """Sunucu üyelerini al"""
    try:
        headers = get_user_headers(token)
        response = requests.get(
            f'https://discord.com/api/v9/guilds/{guild_id}/members',
            headers=headers,
            params={'limit': limit}
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def get_guild_channels(token, guild_id):
    """Sunucu kanallarını al"""
    try:
        headers = get_user_headers(token)
        response = requests.get(
            f'https://discord.com/api/v9/guilds/{guild_id}/channels',
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def get_guild_roles(token, guild_id):
    """Sunucu rollerini al"""
    try:
        headers = get_user_headers(token)
        response = requests.get(
            f'https://discord.com/api/v9/guilds/{guild_id}/roles',
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return []

def display_guild_info(guild_data, token):
    """Sunucu bilgilerini göster"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║          SERVER INFORMATION               ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    if not guild_data:
        print(f"\n{Colors.RED}[✗] Failed to fetch server information{Colors.RESET}")
        return
    
    # Get owner info
    owner_info = None
    try:
        headers = get_user_headers(token)
        response = requests.get(
            f"https://discord.com/api/v9/guilds/{guild_data['id']}/members/{guild_data['owner_id']}",
            headers=headers
        )
        if response.status_code == 200:
            owner_info = response.json()
    except:
        pass
    
    print(f"\n{Colors.CYAN}[📛] Server Name: {Colors.WHITE}{guild_data.get('name', 'Unknown')}")
    print(f"{Colors.CYAN}[🆔] Server ID: {Colors.WHITE}{guild_data.get('id', 'Unknown')}")
    
    if owner_info:
        owner_user = owner_info.get('user', {})
        print(f"{Colors.CYAN}[👑] Owner: {Colors.WHITE}{owner_user.get('username', 'Unknown')}#{owner_user.get('discriminator', '0000')}")
    
    print(f"{Colors.CYAN}[👑] Owner ID: {Colors.WHITE}{guild_data.get('owner_id', 'Unknown')}")
    print(f"{Colors.CYAN}[👥] Members: {Colors.WHITE}{guild_data.get('approximate_member_count', 'Unknown')}")
    print(f"{Colors.CYAN}[🟢] Online: {Colors.WHITE}{guild_data.get('approximate_presence_count', 'Unknown')}")
    
    # Premium tier
    premium_tier = guild_data.get('premium_tier', 0)
    premium_text = {
        0: "None",
        1: "Level 1",
        2: "Level 2", 
        3: "Level 3"
    }.get(premium_tier, f"Tier {premium_tier}")
    print(f"{Colors.CYAN}[💎] Boost Level: {Colors.WHITE}{premium_text}")
    print(f"{Colors.CYAN}[🚀] Boosts: {Colors.WHITE}{guild_data.get('premium_subscription_count', 0)}")
    
    # Server icon
    if guild_data.get('icon'):
        icon_url = f"https://cdn.discordapp.com/icons/{guild_data['id']}/{guild_data['icon']}.webp?size=256"
        print(f"{Colors.CYAN}[🖼️] Icon URL: {Colors.WHITE}{icon_url}")
    
    # Creation date
    if guild_data.get('id'):
        try:
            snowflake = int(guild_data['id'])
            timestamp = ((snowflake >> 22) + 1420070400000) / 1000
            created_at = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{Colors.CYAN}[📅] Created: {Colors.WHITE}{created_at}")
        except:
            pass
    
    print(f"{Colors.CYAN}[🌍] Region: {Colors.WHITE}{guild_data.get('region', 'Unknown')}")
    print(f"{Colors.CYAN}[🔒] Verification: {Colors.WHITE}{guild_data.get('verification_level', 'Unknown')}")
    
    # Features
    features = guild_data.get('features', [])
    if features:
        print(f"{Colors.CYAN}[✨] Features: {Colors.WHITE}{', '.join(features[:5])}")
        if len(features) > 5:
            print(f"{Colors.CYAN}    + {len(features)-5} more features{Colors.RESET}")

def display_member_stats(token, guild_id):
    """Üye istatistiklerini göster"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║          MEMBER STATISTICS               ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    try:
        members = get_guild_members(token, guild_id, 100)
        if not members:
            print(f"\n{Colors.YELLOW}[!] Could not fetch member data{Colors.RESET}")
            return
        
        total_members = len(members)
        bots = sum(1 for m in members if m.get('user', {}).get('bot', False))
        humans = total_members - bots
        
        print(f"\n{Colors.CYAN}[📊] Sample Size: {Colors.WHITE}{total_members} members")
        print(f"{Colors.CYAN}[🤖] Bots: {Colors.WHITE}{bots} ({bots/total_members*100:.1f}%)")
        print(f"{Colors.CYAN}[👤] Humans: {Colors.WHITE}{humans} ({humans/total_members*100:.1f}%)")
        
        # Top roles
        role_counts = {}
        for member in members:
            for role_id in member.get('roles', []):
                role_counts[role_id] = role_counts.get(role_id, 0) + 1
        
        if role_counts:
            top_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"\n{Colors.CYAN}[🎭] Top 5 Roles by Members:{Colors.RESET}")
            for role_id, count in top_roles:
                print(f"   {Colors.WHITE}Role {role_id[:8]}...: {count} members")
        
    except Exception as e:
        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")

def display_channel_info(token, guild_id):
    """Kanal bilgilerini göster"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║          CHANNEL ANALYSIS                ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    try:
        channels = get_guild_channels(token, guild_id)
        if not channels:
            print(f"\n{Colors.YELLOW}[!] Could not fetch channel data{Colors.RESET}")
            return
        
        text_channels = []
        voice_channels = []
        category_channels = []
        
        for channel in channels:
            channel_type = channel.get('type', 0)
            if channel_type == 0:  # Text channel
                text_channels.append(channel)
            elif channel_type == 2:  # Voice channel
                voice_channels.append(channel)
            elif channel_type == 4:  # Category
                category_channels.append(channel)
        
        print(f"\n{Colors.CYAN}[📝] Text Channels: {Colors.WHITE}{len(text_channels)}")
        print(f"{Colors.CYAN}[🎤] Voice Channels: {Colors.WHITE}{len(voice_channels)}")
        print(f"{Colors.CYAN}[📁] Categories: {Colors.WHITE}{len(category_channels)}")
        print(f"{Colors.CYAN}[📊] Total Channels: {Colors.WHITE}{len(channels)}")
        
        # Show some channel names
        if text_channels:
            print(f"\n{Colors.CYAN}[💬] Sample Text Channels:{Colors.RESET}")
            for channel in text_channels[:5]:
                name = channel.get('name', 'Unknown')
                print(f"   {Colors.WHITE}#{name}")
        
    except Exception as e:
        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")

def display_role_info(token, guild_id):
    """Rol bilgilerini göster"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║          ROLE INFORMATION                ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    try:
        roles = get_guild_roles(token, guild_id)
        if not roles:
            print(f"\n{Colors.YELLOW}[!] Could not fetch role data{Colors.RESET}")
            return
        
        # Sort roles by position (highest first)
        roles.sort(key=lambda x: x.get('position', 0), reverse=True)
        
        print(f"\n{Colors.CYAN}[🎭] Total Roles: {Colors.WHITE}{len(roles)}")
        
        print(f"\n{Colors.CYAN}[🏆] Top Roles:{Colors.RESET}")
        for role in roles[:10]:  # Show top 10 roles
            name = role.get('name', 'Unknown')
            color = role.get('color', 0)
            position = role.get('position', 0)
            perms = role.get('permissions', '0')
            
            # Format color
            if color == 0:
                color_str = "Default"
            else:
                color_str = f"#{color:06x}"
            
            # Basic permissions
            perms_int = int(perms)
            is_admin = (perms_int & 0x8) != 0  # ADMINISTRATOR permission
            
            admin_mark = " 👑" if is_admin else ""
            
            print(f"   {Colors.WHITE}{name}{admin_mark}")
            print(f"     Position: {position} | Color: {color_str}")
        
    except Exception as e:
        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")

def export_server_data(token, guild_id):
    """Sunucu verilerini dışa aktar"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║          EXPORT SERVER DATA              ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    try:
        # Get all data
        guild_info = get_guild_info(token, guild_id)
        members = get_guild_members(token, guild_id, 50)
        channels = get_guild_channels(token, guild_id)
        roles = get_guild_roles(token, guild_id)
        
        if not guild_info:
            print(f"\n{Colors.RED}[✗] Could not fetch server data{Colors.RESET}")
            return
        
        # Create export data
        export_data = {
            'export_date': datetime.now().isoformat(),
            'server_id': guild_id,
            'server_info': guild_info,
            'members_sample': members,
            'channels': channels,
            'roles': roles,
            'exported_by': get_user_info(token)
        }
        
        # Save to JSON file
        filename = f"discord_server_{guild_id}_{int(datetime.now().timestamp())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n{Colors.GREEN}[✓] Data exported to: {Colors.WHITE}{filename}")
        print(f"{Colors.CYAN}[📁] File size: {Colors.WHITE}{os.path.getsize(filename) / 1024:.1f} KB")
        
    except Exception as e:
        print(f"{Colors.RED}[✗] Export failed: {e}{Colors.RESET}")

def token_checker():
    """Token kontrol aracı"""
    print(f"\n{Colors.LIGHT_PURPLE}╔══════════════════════════════════════════╗")
    print(f"{Colors.LIGHT_PURPLE}║          TOKEN CHECKER                   ║")
    print(f"{Colors.LIGHT_PURPLE}╚══════════════════════════════════════════╝{Colors.RESET}")
    
    token = input(f"\n{Colors.CYAN}[?] Enter Discord Token: {Colors.WHITE}")
    
    if not token:
        print(f"{Colors.RED}[✗] No token provided{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[*] Validating token...{Colors.RESET}")
    
    if validate_token(token):
        user_info = get_user_info(token)
        if user_info:
            print(f"\n{Colors.GREEN}[✓] TOKEN IS VALID{Colors.RESET}")
            print(f"{Colors.CYAN}[👤] Username: {Colors.WHITE}{user_info.get('username')}#{user_info.get('discriminator')}")
            print(f"{Colors.CYAN}[🆔] User ID: {Colors.WHITE}{user_info.get('id')}")
            print(f"{Colors.CYAN}[📧] Email: {Colors.WHITE}{user_info.get('email', 'N/A')}")
            
            # Check nitro status
            premium_type = user_info.get('premium_type', 0)
            nitro_status = {
                0: "None",
                1: "Nitro Classic",
                2: "Nitro Booster",
                3: "Nitro Full"
            }.get(premium_type, "Unknown")
            
            print(f"{Colors.CYAN}[💎] Nitro: {Colors.WHITE}{nitro_status}")
            print(f"{Colors.CYAN}[🔒] 2FA: {Colors.WHITE}{'Enabled' if user_info.get('mfa_enabled') else 'Disabled'}")
            print(f"{Colors.CYAN}[✅] Verified: {Colors.WHITE}{'Yes' if user_info.get('verified') else 'No'}")
        else:
            print(f"{Colors.YELLOW}[!] Valid token but could not fetch user info{Colors.RESET}")
    else:
        print(f"{Colors.RED}[✗] INVALID OR EXPIRED TOKEN{Colors.RESET}")
    
    input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")

def main():
    """Ana program"""
    while True:
        print_banner()
        print_menu()
        
        choice = input(f"{Colors.LIGHT_PURPLE}[?] Select option (0-6): {Colors.WHITE}")
        
        if choice == '0':
            print(f"\n{Colors.CYAN}[*] Goodbye! {Colors.LIGHT_PURPLE}❤{Colors.RESET}\n")
            sys.exit(0)
        
        elif choice == '1':
            # Server Lookup
            print_banner()
            print(f"{Colors.LIGHT_PURPLE}[🔍] SERVER LOOKUP{Colors.RESET}\n")
            
            token = input(f"{Colors.CYAN}[?] Enter Discord Token: {Colors.WHITE}")
            if not validate_token(token):
                print(f"\n{Colors.RED}[✗] Invalid token!{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                continue
            
            guild_id = input(f"{Colors.CYAN}[?] Enter Server ID: {Colors.WHITE}")
            
            print(f"\n{Colors.CYAN}[*] Fetching server information...{Colors.RESET}")
            
            guild_data = get_guild_info(token, guild_id)
            display_guild_info(guild_data, token)
            
            # Ask for additional info
            if guild_data:
                print(f"\n{Colors.CYAN}[?] Show additional information?{Colors.RESET}")
                print(f"   {Colors.WHITE}1. Member Statistics")
                print(f"   {Colors.WHITE}2. Channel Analysis")
                print(f"   {Colors.WHITE}3. Role Information")
                print(f"   {Colors.WHITE}4. No, back to menu")
                
                sub_choice = input(f"\n{Colors.CYAN}[?] Select: {Colors.WHITE}")
                
                if sub_choice == '1':
                    display_member_stats(token, guild_id)
                elif sub_choice == '2':
                    display_channel_info(token, guild_id)
                elif sub_choice == '3':
                    display_role_info(token, guild_id)
            
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '2':
            # Member Statistics
            print_banner()
            print(f"{Colors.LIGHT_PURPLE}[👥] MEMBER STATISTICS{Colors.RESET}\n")
            
            token = input(f"{Colors.CYAN}[?] Enter Discord Token: {Colors.WHITE}")
            if not validate_token(token):
                print(f"\n{Colors.RED}[✗] Invalid token!{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                continue
            
            guild_id = input(f"{Colors.CYAN}[?] Enter Server ID: {Colors.WHITE}")
            
            display_member_stats(token, guild_id)
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '3':
            # Channel Analyzer
            print_banner()
            print(f"{Colors.LIGHT_PURPLE}[📊] CHANNEL ANALYZER{Colors.RESET}\n")
            
            token = input(f"{Colors.CYAN}[?] Enter Discord Token: {Colors.WHITE}")
            if not validate_token(token):
                print(f"\n{Colors.RED}[✗] Invalid token!{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                continue
            
            guild_id = input(f"{Colors.CYAN}[?] Enter Server ID: {Colors.WHITE}")
            
            display_channel_info(token, guild_id)
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '4':
            # Role Information
            print_banner()
            print(f"{Colors.LIGHT_PURPLE}[🎭] ROLE INFORMATION{Colors.RESET}\n")
            
            token = input(f"{Colors.CYAN}[?] Enter Discord Token: {Colors.WHITE}")
            if not validate_token(token):
                print(f"\n{Colors.RED}[✗] Invalid token!{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                continue
            
            guild_id = input(f"{Colors.CYAN}[?] Enter Server ID: {Colors.WHITE}")
            
            display_role_info(token, guild_id)
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '5':
            # Export Server Data
            print_banner()
            print(f"{Colors.LIGHT_PURPLE}[📁] EXPORT SERVER DATA{Colors.RESET}\n")
            
            token = input(f"{Colors.CYAN}[?] Enter Discord Token: {Colors.WHITE}")
            if not validate_token(token):
                print(f"\n{Colors.RED}[✗] Invalid token!{Colors.RESET}")
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
                continue
            
            guild_id = input(f"{Colors.CYAN}[?] Enter Server ID: {Colors.WHITE}")
            
            export_server_data(token, guild_id)
            input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")
        
        elif choice == '6':
            # Token Checker
            print_banner()
            token_checker()
        
        else:
            print(f"\n{Colors.RED}[✗] Invalid option!{Colors.RESET}")
            sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}[*] Program interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[✗] Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)