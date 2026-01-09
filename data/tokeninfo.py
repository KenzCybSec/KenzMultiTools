


import time
import requests
import os
import ctypes
from datetime import datetime
from colorama import Fore, init

init()

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

def tokeninfo():
    cls()
    ctypes.windll.kernel32.SetConsoleTitleW("Token Info Checker")
    
    print(f"\n{Fore.MAGENTA}╔{'═'*60}╗")
    print(f"{Fore.MAGENTA}║{Fore.LIGHTMAGENTA_EX}{' '*22}TOKEN INFO CHECKER{' '*21}{Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}╚{'═'*60}╝\n")
    
    token = str(input(f"{Fore.MAGENTA}[{Fore.WHITE}+{Fore.MAGENTA}] {Fore.WHITE}Enter Discord token: {Fore.LIGHTMAGENTA_EX}"))

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    languages = {
        'da': 'Danish, Denmark',
        'de': 'German, Germany',
        'en-GB': 'English, United Kingdom',
        'en-US': 'English, United States',
        'es-ES': 'Spanish, Spain',
        'fr': 'French, France',
        'hr': 'Croatian, Croatia',
        'lt': 'Lithuanian, Lithuania',
        'hu': 'Hungarian, Hungary',
        'nl': 'Dutch, Netherlands',
        'no': 'Norwegian, Norway',
        'pl': 'Polish, Poland',
        'pt-BR': 'Portuguese, Brazilian, Brazil',
        'ro': 'Romanian, Romania',
        'fi': 'Finnish, Finland',
        'sv-SE': 'Swedish, Sweden',
        'vi': 'Vietnamese, Vietnam',
        'tr': 'Turkish, Turkey',
        'cs': 'Czech, Czechia, Czech Republic',
        'el': 'Greek, Greece',
        'bg': 'Bulgarian, Bulgaria',
        'ru': 'Russian, Russia',
        'uk': 'Ukranian, Ukraine',
        'th': 'Thai, Thailand',
        'zh-CN': 'Chinese, China',
        'ja': 'Japanese',
        'zh-TW': 'Chinese, Taiwan',
        'ko': 'Korean, Korea'
    }

    cc_digits = {
        'american express': '3',
        'visa': '4',
        'mastercard': '5'
    }

    try:
        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Connection error: {e}")
        input(f"{Fore.MAGENTA}[{Fore.WHITE}↵{Fore.MAGENTA}] {Fore.WHITE}Press Enter to continue...")
        return

    if res.status_code == 200:
        res_json = res.json()
        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
        user_id = res_json['id']
        avatar_id = res_json['avatar']
        avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif' if avatar_id else "No avatar"
        phone_number = res_json.get('phone', 'None')
        email = res_json.get('email', 'None')
        mfa_enabled = res_json.get('mfa_enabled', False)
        flags = res_json.get('flags', 0)
        locale = res_json.get('locale', 'en-US')
        verified = res_json.get('verified', False)
        
        language = languages.get(locale, 'Unknown')
        creation_date = datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
        
        has_nitro = False
        nitro_days = 0
        
        try:
            res_nitro = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
            if res_nitro.status_code == 200:
                nitro_data = res_nitro.json()
                has_nitro = bool(len(nitro_data) > 0)
                
                if has_nitro and nitro_data:
                    d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                    d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                    nitro_days = abs((d1 - d2).days)
        except:
            pass

        billing_info = []
        
        try:
            billing_res = requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers)
            if billing_res.status_code == 200:
                for x in billing_res.json():
                    yy = x.get('billing_address', {})
                    name = yy.get('name', 'Unknown')
                    address_1 = yy.get('line_1', 'Unknown')
                    address_2 = yy.get('line_2', '')
                    city = yy.get('city', 'Unknown')
                    postal_code = yy.get('postal_code', 'Unknown')
                    state = yy.get('state', '')
                    country = yy.get('country', 'Unknown')

                    if x.get('type') == 1:
                        cc_brand = x.get('brand', 'Unknown')
                        cc_first = cc_digits.get(cc_brand, '*')
                        cc_last = x.get('last_4', '****')
                        cc_month = str(x.get('expires_month', 'MM'))
                        cc_year = str(x.get('expires_year', 'YYYY'))
                        
                        data = {
                            'Payment Type': 'Credit Card',
                            'Valid': not x.get('invalid', True),
                            'CC Holder Name': name,
                            'CC Brand': cc_brand.title(),
                            'CC Number': f"{cc_first}************{cc_last}",
                            'CC Exp. Date': f"{cc_month.zfill(2)}/{cc_year[2:4]}",
                            'Address 1': address_1,
                            'Address 2': address_2 if address_2 else 'None',
                            'City': city,
                            'Postal Code': postal_code,
                            'State': state if state else 'None',
                            'Country': country,
                            'Default Payment Method': x.get('default', False)
                        }

                    elif x.get('type') == 2:
                        data = {
                            'Payment Type': 'PayPal',
                            'Valid': not x.get('invalid', True),
                            'PayPal Name': name,
                            'PayPal Email': x.get('email', 'Unknown'),
                            'Address 1': address_1,
                            'Address 2': address_2 if address_2 else 'None',
                            'City': city,
                            'Postal Code': postal_code,
                            'State': state if state else 'None',
                            'Country': country,
                            'Default Payment Method': x.get('default', False)
                        }
                    else:
                        continue
                        
                    billing_info.append(data)
        except:
            pass

        print(f"\n{Fore.MAGENTA}[{Fore.WHITE}📋{Fore.MAGENTA}] {Fore.WHITE}Basic Information")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} Username: {Fore.LIGHTCYAN_EX}{user_name}")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} User ID: {Fore.LIGHTCYAN_EX}{user_id}")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} Creation Date: {Fore.LIGHTCYAN_EX}{creation_date}")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} Avatar URL: {Fore.LIGHTCYAN_EX}{avatar_url}")
        print(f"  {Fore.MAGENTA}└─{Fore.WHITE} Token: {Fore.LIGHTMAGENTA_EX}{token[:20]}...{token[-10:] if len(token) > 30 else ''}\n")

        print(f"{Fore.MAGENTA}[{Fore.WHITE}✨{Fore.MAGENTA}] {Fore.WHITE}Nitro Information")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} Nitro Status: {Fore.LIGHTCYAN_EX}{'✅ Active' if has_nitro else '❌ Not Active'}")
        if has_nitro:
            print(f"  {Fore.MAGENTA}└─{Fore.WHITE} Expires in: {Fore.LIGHTCYAN_EX}{nitro_days} day(s)\n")
        else:
            print(f"  {Fore.MAGENTA}└─{Fore.WHITE} Expires in: {Fore.LIGHTRED_EX}None\n")

        print(f"{Fore.MAGENTA}[{Fore.WHITE}📞{Fore.MAGENTA}] {Fore.WHITE}Contact Information")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} Phone Number: {Fore.LIGHTCYAN_EX}{phone_number}")
        print(f"  {Fore.MAGENTA}└─{Fore.WHITE} Email: {Fore.LIGHTCYAN_EX}{email}\n")

        if billing_info:
            print(f"{Fore.MAGENTA}[{Fore.WHITE}💳{Fore.MAGENTA}] {Fore.WHITE}Billing Information")
            for i, x in enumerate(billing_info, 1):
                print(f"  {Fore.MAGENTA}┌─[{Fore.WHITE}{i}{Fore.MAGENTA}] {x['Payment Type']}")
                for key, val in x.items():
                    if key != 'Payment Type':
                        print(f"  {Fore.MAGENTA}│  {Fore.WHITE}{key}: {Fore.LIGHTMAGENTA_EX}{val}")
                print(f"  {Fore.MAGENTA}└─\n" if i == len(billing_info) else f"  {Fore.MAGENTA}│\n")

        print(f"{Fore.MAGENTA}[{Fore.WHITE}🔒{Fore.MAGENTA}] {Fore.WHITE}Account Security")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} 2FA/MFA Enabled: {Fore.LIGHTCYAN_EX}{'✅ Yes' if mfa_enabled else '❌ No'}")
        print(f"  {Fore.MAGENTA}└─{Fore.WHITE} Flags: {Fore.LIGHTCYAN_EX}{flags}\n")

        print(f"{Fore.MAGENTA}[{Fore.WHITE}🌐{Fore.MAGENTA}] {Fore.WHITE}Other Information")
        print(f"  {Fore.MAGENTA}├─{Fore.WHITE} Locale: {Fore.LIGHTCYAN_EX}{locale} ({language})")
        print(f"  {Fore.MAGENTA}└─{Fore.WHITE} Email Verified: {Fore.LIGHTCYAN_EX}{'✅ Yes' if verified else '❌ No'}")

    elif res.status_code == 401:
        print(f"\n{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Invalid or expired token")
    else:
        print(f"\n{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Error {res.status_code}: Failed to fetch token info")

    print(f"\n{Fore.MAGENTA}{'═'*60}")
    input(f"{Fore.MAGENTA}[{Fore.WHITE}↵{Fore.MAGENTA}] {Fore.WHITE}Press Enter to exit...")

if __name__ == '__main__':
    tokeninfo()