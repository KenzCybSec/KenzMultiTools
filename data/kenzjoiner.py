import tls_client, base64, json, os, sys, time, threading, uuid, urllib.parse, websocket, re, subprocess
from typing import Optional
from datetime import datetime
from colorama import Fore, Style, init

# Colorama'yı başlat
init(autoreset=True)

# Renk tanımlamaları - Kenz stili
class KenzColors:
    PRIMARY = Fore.LIGHTCYAN_EX
    SECONDARY = Fore.LIGHTMAGENTA_EX
    SUCCESS = Fore.LIGHTGREEN_EX
    ERROR = Fore.LIGHTRED_EX
    WARNING = Fore.LIGHTYELLOW_EX
    INFO = Fore.LIGHTBLUE_EX
    BANNER = Fore.LIGHTCYAN_EX
    MENU = Fore.LIGHTMAGENTA_EX
    INPUT = Fore.LIGHTCYAN_EX
    BORDER = Fore.LIGHTBLACK_EX
    COUNTER = Fore.LIGHTYELLOW_EX
    RESET = Fore.RESET
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    WHITE = Fore.WHITE 
# Stil tanımlamaları
KC = KenzColors
SUCCESS = f"{KC.BRIGHT}[{KC.SUCCESS}✓{KC.BRIGHT}]{KC.RESET}"
FAIL = f"{KC.BRIGHT}[{KC.ERROR}✗{KC.BRIGHT}]{KC.RESET}"
INPUT = f"{KC.BRIGHT}[{KC.INPUT}→{KC.BRIGHT}]{KC.RESET}"
INFO = f"{KC.BRIGHT}[{KC.INFO}i{KC.BRIGHT}]{KC.RESET}"
WARNING = f"{KC.BRIGHT}[{KC.WARNING}!{KC.BRIGHT}]{KC.RESET}"
PROCESS = f"{KC.BRIGHT}[{KC.PRIMARY}●{KC.BRIGHT}]{KC.RESET}"

chrome_version = "141"

def print_banner():
    """Kenz stili banner"""
    banner = f"""
    {KC.BANNER}{KC.BRIGHT}
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║    ██╗  ██╗███████╗███╗   ██╗███████╗               ║
    ║    ██║ ██╔╝██╔════╝████╗  ██║╚══███╔╝               ║
    ║    █████╔╝ █████╗  ██╔██╗ ██║  ███╔╝                ║
    ║    ██╔═██╗ ██╔══╝  ██║╚██╗██║ ███╔╝                 ║
    ║    ██║  ██╗███████╗██║ ╚████║███████╗               ║
    ║    ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝               ║
    ║                                                      ║
    ║         {KC.SECONDARY}ᴅɪꜱᴄᴏʀᴅ ᴍᴜʟᴛɪ-ᴛᴏᴏʟꜱ ᴠ2.0{KC.BANNER}         ║
    ║              {KC.WARNING}ᴍᴀᴅᴇ ʙʏ ᴋᴇɴᴢ{KC.BANNER}                ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    {KC.RESET}
    """
    return banner

def print_stats_box(tokens, proxies):
    """İstatistik kutusu"""
    box = f"""
    {KC.BORDER}{KC.BRIGHT}╔═══════════════════════════════════════════════════════════════╗{KC.RESET}
    {KC.BORDER}{KC.BRIGHT}║{KC.INFO}                    ᴄᴜʀʀᴇɴᴛ ꜱᴛᴀᴛꜱ                    {KC.BORDER}{KC.BRIGHT}║{KC.RESET}
    {KC.BORDER}{KC.BRIGHT}║                                                               ║{KC.RESET}
    {KC.BORDER}{KC.BRIGHT}║  {KC.PRIMARY}•{KC.RESET} ᴛᴏᴋᴇɴꜱ ʟᴏᴀᴅᴇᴅ: {KC.COUNTER}{tokens:<10}{KC.RESET}                     {KC.BORDER}{KC.BRIGHT}║{KC.RESET}
    {KC.BORDER}{KC.BRIGHT}║  {KC.PRIMARY}•{KC.RESET} ᴘʀᴏxɪᴇꜱ ʟᴏᴀᴅᴇᴅ: {KC.COUNTER}{proxies:<10}{KC.RESET}                     {KC.BORDER}{KC.BRIGHT}║{KC.RESET}
    {KC.BORDER}{KC.BRIGHT}║  {KC.PRIMARY}•{KC.RESET} ᴠᴇʀꜱɪᴏɴ: {KC.COUNTER}ᴄʜʀᴏᴍᴇ {chrome_version}{KC.RESET}                           {KC.BORDER}{KC.BRIGHT}║{KC.RESET}
    {KC.BORDER}{KC.BRIGHT}║  {KC.PRIMARY}•{KC.RESET} ꜱᴛᴀᴛᴜꜱ: {KC.SUCCESS}ʀᴇᴀᴅʏ{KC.RESET}                                 {KC.BORDER}{KC.BRIGHT}║{KC.RESET}
    {KC.BORDER}{KC.BRIGHT}╚═══════════════════════════════════════════════════════════════╝{KC.RESET}
    """
    return box

def print_menu():
    """Ana menü"""
    menu = f"""
    {KC.MENU}{KC.BRIGHT}
    ╔═══════════════════════════════════════════════════════════════╗
    ║                     ᴍᴀɪɴ ᴍᴇɴᴜ - ᴄʜᴏᴏꜱᴇ                      ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  {KC.BRIGHT}[{KC.PRIMARY}1{KC.BRIGHT}]{KC.RESET} {KC.INFO}ꜱᴇʀᴠᴇʀ ᴊᴏɪɴᴇʀ{KC.MENU}          {KC.BRIGHT}[{KC.PRIMARY}5{KC.BRIGHT}]{KC.RESET} {KC.INFO}ʀᴇᴀᴄᴛɪᴏɴ ᴄʟɪᴄᴋᴇʀ{KC.MENU}       ║
    ║  {KC.BRIGHT}[{KC.PRIMARY}2{KC.BRIGHT}]{KC.RESET} {KC.INFO}ꜱᴇʀᴠᴇʀ ʟᴇᴀᴠᴇʀ{KC.MENU}          {KC.BRIGHT}[{KC.PRIMARY}6{KC.BRIGHT}]{KC.RESET} {KC.INFO}ʀᴜʟᴇ ʙʏᴘᴀꜱꜱ{KC.MENU}           ║
    ║  {KC.BRIGHT}[{KC.PRIMARY}3{KC.BRIGHT}]{KC.RESET} {KC.INFO}ᴛᴏᴋᴇɴ ᴄʜᴇᴄᴋᴇʀ{KC.MENU}          {KC.BRIGHT}[{KC.PRIMARY}7{KC.BRIGHT}]{KC.RESET} {KC.INFO}ᴏɴʙᴏᴀʀᴅ ʙʏᴘᴀꜱꜱ{KC.MENU}        ║
    ║  {KC.BRIGHT}[{KC.PRIMARY}4{KC.BRIGHT}]{KC.RESET} {KC.INFO}ʙᴜᴛᴛᴏɴ ᴄʟɪᴄᴋᴇʀ{KC.MENU}         {KC.BRIGHT}[{KC.PRIMARY}8{KC.BRIGHT}]{KC.RESET} {KC.INFO}ᴇxɪᴛ{KC.MENU}                 ║
    ║                                                               ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║          {KC.WARNING}ᴘʀᴇꜱꜱ [{KC.PRIMARY}0{KC.WARNING}] ᴛᴏ ʀᴇꜰʀᴇꜱʜ ᴅᴀᴛᴀ          ║
    ╚═══════════════════════════════════════════════════════════════╝
    {KC.RESET}
    """
    return menu

class DiscordJoinerPY:
    def __init__(self):
        self.client = tls_client.Session(client_identifier=f"chrome_{chrome_version}", random_tls_extension_order=True)
        self.threads = []
        self.tokens = []
        self.proxies = []
        self.fingerprints = {}
        self.check()
        # İstatistikler
        self.joined_count = 0
        self.invalid_count = 0
        self.hcaptcha_count = 0
        self.clicked_count = 0
        self.button_fail_count = 0
        self.reacted_count = 0
        self.reaction_fail_count = 0
        self.total_tokens_to_process = 0
        self.rules_accepted_count = 0
        self.rules_fail_count = 0
        self.reactor_lock = threading.Lock()
        self.reactor_selected_emoji = None
        self.reactor_setup_done = False
        self.onboarding_fail_count = 0
        self.onboarding_success_count = 0
        self.left_count = 0
        self.leave_fail_count = 0
        self.valid_count = 0
        self.locked_count = 0
        self.invalid_checker_count = 0
        self.valid_tokens_list = []
        self.checker_lock = threading.Lock()
        # Build numaraları
        self.build_number, self.native_version = self.build_numbers()
        self.properties = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "has_client_mods": False,
            "browser_user_agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version}.0.0.0 Safari/537.36",
            "browser_version": f"{chrome_version}.0.0.0",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "https://discord.com/",
            "referring_domain_current": "discord.com",
            "release_channel": "stable",
            "client_build_number": self.build_number,
            "native_build_number": self.native_version,
            "client_event_source": None,
            "client_launch_id": str(uuid.uuid4()),
            "launch_signature": str(uuid.uuid4()),
            "client_heartbeat_session_id": str(uuid.uuid4()),
            "client_app_state": "focused"
        }

    def _native(self):
        try:
            response = self.client.get(
                "https://updates.discord.com/distributions/app/manifests/latest",
                params={"install_id": "0", "channel": "stable", "platform": "win", "arch": "x86"},
                headers={"user-agent": "Discord-Updater/1", "accept-encoding": "gzip"}
            ).json()
            return int(response["metadata_version"])
        except Exception:
            return 51902

    def _build(self):
        try:
            page = self.client.get("https://discord.com/app").text
            assets = re.findall(r'(?:https://discord\.com)?/assets/([a-f0-9]+)\.js', page)
            for asset in reversed(assets):
                js = self.client.get(f"https://discord.com/assets/{asset}", timeout=10).text
                if "buildNumber:" in js:
                    return int(js.split('buildNumber:"')[1].split('"')[0])
            return 426030
        except Exception:
            return 426030

    def build_numbers(self):
        return self._build(), self._native()

    def get_fingerprint(self, token):
        if token in self.fingerprints:
            return self.fingerprints[token]
        try:
            res = self.client.get(
                "https://discord.com/api/v9/experiments",
                headers={
                    "user-agent": self.properties["browser_user_agent"],
                    "authorization": token,
                    "accept": "*/*",
                    "referer": "https://discord.com/channels/@me",
                    "x-discord-locale": "en-GB",
                    "x-super-properties": base64.b64encode(json.dumps(self.properties, separators=(',', ':')).encode()).decode()}
            )

            fingerprint = res.json().get("fingerprint", "")
            self.fingerprints[token] = fingerprint
            return fingerprint
        except Exception:
            return ""

    def discord_cookies(self) -> Optional[str]:
        try:
            response = self.client.get('https://discord.com')
            if response.status_code == 200:
                cookies = "; ".join([f"{cookie.name}={cookie.value}" for cookie in response.cookies])
                result = cookies + "; locale=en-US"
                return result
            else:
                return "__dcfduid=62f9e16000a211ef8089eda5bffbf7f9; __sdcfduid=62f9e16100a211ef8089eda5bffbf7f98e904ba04346eacdf57ee4af97bdd94e4c16f7df1db5132bea9132dd26b21a2a; locale=en-US"
        except Exception:
            return None

    def headers(self, token):
        fingerprint = self.get_fingerprint(token)
        cookie = self.discord_cookies()
        full_version = self.properties["browser_user_agent"].rsplit("Chrome/", 1)[-1].split(" ")[0].split(".")[0]
        full_versionn = self.properties["browser_user_agent"].rsplit("Chrome/", 1)[-1].split(" ")[0]

        headers = {
            "Authority": "discord.com",
            "Accept": "*/*",
            "Accept-encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.9",
            "Authorization": token,
            "Content-Type": "application/json",
            "Cookie": cookie if cookie else "",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/channels/@me",
            "Sec-Ch-Ua": f'"Google Chrome";v="{chrome_version}", "Not?A_Brand";v="8", "Chromium";v="{chrome_version}"',
            "Sec-ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Full-Version": f'"{full_versionn}"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.properties["browser_user_agent"],
            "X-Debug-Options": "bugReporterEnabled",
            "X-Discord-Locale": "en-US",
            "X-Discord-Timezone": "Etc/GMT-7",
            "X-Super-Properties": base64.b64encode(json.dumps(self.properties, separators=(',', ':')).encode()).decode(),
            "X-Fingerprint": fingerprint,
            "Connection": "keep-alive"
        }
        return headers

    def print_loading(self, text):
        """Yükleme animasyonu"""
        print(f"\n{PROCESS} {KC.PRIMARY}{text}{KC.RESET}", end="", flush=True)
    
    def print_progress(self, current, total, prefix=""):
        """İlerleme çubuğu"""
        percent = int((current / total) * 100)
        bar_length = 30
        filled_length = int(bar_length * current // total)
        bar = f"{KC.SUCCESS}█" * filled_length + f"{KC.BORDER}░" * (bar_length - filled_length)
        print(f"\r{prefix}{KC.PRIMARY}[{bar}{KC.PRIMARY}] {percent}% ({current}/{total})", end="", flush=True)

    def accept_invite(self, token: str, invite: str, proxy_: str = None):
        token_display = f"{KC.WHITE}{token[:35]}...{KC.RESET}"
        try:
            ws = websocket.WebSocket()
            ws.connect("wss://gateway.discord.gg/?encoding=json&v=9")
            hello = json.loads(ws.recv())
            heartbeat_interval = int(hello["d"]["heartbeat_interval"]) / 1000
            ws.send(json.dumps({"op": 2, "d": {"token": token, "properties": {"$os": "Android", "$browser": "Discord Android", "$device": "Android"}, "presence": {"status": "online", "since": 0, "afk": False}}}))
            ws.send(json.dumps({"op": 1, "d": None}))
        except Exception as e:
            pass
        
        try:
            response = self.client.post(
                url=f'https://discord.com/api/v10/invites/{invite}',
                headers=self.headers(token=token),
                json={"session_id": str(uuid.uuid4())},
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
            )
            response_json = response.json()
            status = f"{KC.BORDER}({response.status_code}){KC.RESET}"
            timestamp = time.strftime("%H:%M:%S")
            
            if response.status_code == 200:
                server_name = response_json.get('guild', {}).get('name', 'Unknown Server')
                print(f"\n{SUCCESS} {timestamp} | {KC.SUCCESS}ᴊᴏɪɴᴇᴅ{KC.RESET}   | {token_display} | {KC.INFO}{server_name}{KC.RESET}")
                self.joined_count += 1
            elif response.status_code == 401:
                print(f"\n{FAIL} {timestamp} | {KC.ERROR}ɪɴᴠᴀʟɪᴅ{KC.RESET}  | {token_display} | {status}")
                self.invalid_count += 1
            elif response.status_code == 400 and response_json.get('captcha_key'):
                print(f"\n{FAIL} {timestamp} | {KC.WARNING}ᴄᴀᴘᴛᴄʜᴀ{KC.RESET} | {token_display} | {status}")
                self.hcaptcha_count += 1
            elif response.status_code == 404:
                print(f"\n{FAIL} {KC.ERROR}Invalid Invite Code: {KC.WHITE}{invite}{KC.RESET}")
                self.invalid_count += 1
            else:
                print(f"\n{FAIL} {timestamp} | {KC.ERROR}ᴇʀʀᴏʀ{KC.RESET}    | {token_display} {status} {KC.BORDER}{response_json.get('message', 'Unknown error')}{KC.RESET}")
                self.invalid_count += 1
        except Exception as e:
            print(f"\n{FAIL} {KC.ERROR}Error for token {token_display}: {KC.BORDER}{e}{KC.RESET}")
            self.invalid_count += 1

    def button_bypass(self, token: str, message_id: str, channel_id: str, guild_id: str, proxy_: str = None):
        token_display = f"{KC.WHITE}{token[:35]}...{KC.RESET}"
        try:
            response = self.client.get(
                f"https://discord.com/api/v10/channels/{channel_id}/messages",
                params={"limit": "50", "around": message_id},
                headers=self.headers(token), 
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None)
            
            if response.status_code != 200 or not response.json():
                print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ɴᴏ ᴍꜱɢ{KC.RESET}   | {token_display} | {KC.BORDER}Could not fetch messages{KC.RESET}")
                self.button_fail_count += 1
                return
            
            data = response.json()
            message_to_click = next((msg for msg in data if msg["id"] == message_id), None)
            if not message_to_click:
                print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ɴᴏ ᴍꜱɢ{KC.RESET}  | {token_display} | {KC.BORDER}Message not found{KC.RESET}")
                self.button_fail_count += 1
                return

            components = message_to_click.get("components", [])
            if not any(comp.get("components") for comp in components):
                print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ɴᴏ ʙᴛɴ{KC.RESET}  | {token_display} | {KC.BORDER}No buttons found{KC.RESET}")
                self.button_fail_count += 1
                return

            buttons = []
            for comp in components:
                if comp.get("components"):
                    buttons.extend([c for c in comp["components"] if c["type"] == 2])

            for button in buttons:
                data = {"application_id": message_to_click.get("application_id") or message_to_click["author"]["id"], "channel_id": channel_id, "data": {"component_type": 2, "custom_id": button["custom_id"]},"guild_id": guild_id, "message_flags": 0, "message_id": message_id, "nonce": str((int(time.mktime(datetime.now().timetuple())) * 1000 - 1704067200000) * 4194304), "session_id": uuid.uuid4().hex, "type": 3}
                click_response = self.client.post("https://discord.com/api/v10/interactions", headers=self.headers(token), json=data)
                if click_response.status_code == 204:
                    btn_label = button.get('label', button['custom_id'][:20])
                    print(f"\n{SUCCESS} {time.strftime('%H:%M:%S')} | {KC.SUCCESS}ᴄʟɪᴄᴋᴇᴅ{KC.RESET}  | {token_display} | {KC.INFO}{btn_label}{KC.RESET}")
                    self.clicked_count += 1
                else:
                    err_msg = click_response.json().get('message', 'Failed to click')
                    print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ꜰᴀɪʟᴇᴅ{KC.RESET}   | {token_display} | {KC.BORDER}({click_response.status_code}) {err_msg}{KC.RESET}")
                    self.button_fail_count += 1
        except Exception as e:
            print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ᴇʀʀᴏʀ{KC.RESET}    | {token_display} | {KC.BORDER}{e}{KC.RESET}")
            self.button_fail_count += 1
            
    def add_reaction(self, token: str, channel_id: str, message_id: str, emoji: str, proxy_: str = None):
        token_display = f"{KC.WHITE}{token[:35]}...{KC.RESET}"
        if ":" in emoji: 
            encoded_emoji = emoji
        else: 
            encoded_emoji = urllib.parse.quote(emoji)
        
        try:
            response = self.client.put(
                f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}/reactions/{encoded_emoji}/@me?location=Message&type=0", 
                headers=self.headers(token), 
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
            )
            status = f"{KC.BORDER}({response.status_code}){KC.RESET}"
            timestamp = time.strftime("%H:%M:%S")
            
            if response.status_code == 204:
                display_emoji = f":{emoji.split(':')[0]}:" if ':' in emoji else emoji
                print(f"\n{SUCCESS} {timestamp} | {KC.SUCCESS}ʀᴇᴀᴄᴛᴇᴅ{KC.RESET}  | {token_display} | {KC.INFO}{display_emoji}{KC.RESET}")
                self.reacted_count += 1
            elif response.status_code == 401:
                print(f"\n{FAIL} {timestamp} | {KC.ERROR}ɪɴᴠᴀʟɪᴅ{KC.RESET}  | {token_display} {status}")
                self.reaction_fail_count += 1
            else:
                message = response.json().get('message', 'Unknown error')
                print(f"\n{FAIL} {timestamp} | {KC.ERROR}ᴇʀʀᴏʀ{KC.RESET}    | {token_display} {status} {KC.BORDER}{message}{KC.RESET}")
                self.reaction_fail_count += 1
        except Exception as e:
            print(f"\n{FAIL} {timestamp} | {KC.ERROR}ᴇʀʀᴏʀ{KC.RESET}    | {token_display} | {KC.BORDER}{e}{KC.RESET}")
            self.reaction_fail_count += 1
            
    def accept_rules(self, token: str, guild_id: str, proxy_: str = None):
        token_display = f"{KC.WHITE}{token[:35]}...{KC.RESET}"
        try:
            get_response = self.client.get(
                f"https://discord.com/api/v10/guilds/{guild_id}/member-verification?with_guild=false",
                headers=self.headers(token), 
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
            )
            
            if get_response.status_code != 200:
                print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ɴᴏ ʀᴜʟᴇꜱ{KC.RESET} | {token_display} | {KC.BORDER}Can't fetch rules ({get_response.status_code}){KC.RESET}")
                self.rules_fail_count += 1
                return
            
            payload = get_response.json()
            put_response = self.client.put(
                f"https://discord.com/api/v10/guilds/{guild_id}/requests/@me", 
                headers=self.headers(token), 
                json=payload, 
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
            )
            
            response_json = put_response.json()
            if put_response.status_code in [201, 204]:
                server_name = response_json.get('guild', {}).get('name', 'Unknown Server')
                print(f"\n{SUCCESS} {time.strftime('%H:%M:%S')} | {KC.SUCCESS}ᴀᴄᴄᴇᴘᴛᴇᴅ{KC.RESET} | {token_display} | {KC.INFO}{server_name}{KC.RESET}")
                self.rules_accepted_count += 1
            else:
                print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ꜰᴀɪʟᴇᴅ{KC.RESET}   | {token_display} | {KC.BORDER}Can't accept rules ({put_response.status_code}){KC.RESET}")
                self.rules_fail_count += 1
        except Exception as e:
            print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ᴇʀʀᴏʀ{KC.RESET}    | {token_display} | {KC.BORDER}{e}{KC.RESET}")
            self.rules_fail_count += 1

    def onboarding_bypass(self, token: str, guild_id: str, proxy_: str = None):
        token_display = f"{KC.WHITE}{token[:35]}...{KC.RESET}"
        try:
            get_response = self.client.get(
                f"https://discord.com/api/v10/guilds/{guild_id}/onboarding", 
                headers=self.headers(token), 
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
            )
            
            if get_response.status_code != 200:
                self.onboarding_fail_count += 1
                return
            
            data = get_response.json()
            if not data.get("prompts") or data.get("enabled") is False:
                print(f"\n{INFO} {time.strftime('%H:%M:%S')} | {KC.WARNING}ɴᴏ ᴏɴʙᴏᴀʀᴅ{KC.RESET}| {token_display} | {KC.BORDER}Nothing to do{KC.RESET}")
                self.onboarding_success_count += 1
                return
            
            now = int(datetime.now().timestamp())
            onboarding_responses = [p["options"][-1]["id"] for p in data["prompts"]]
            onboarding_prompts_seen = {p["id"]: now for p in data["prompts"]}
            onboarding_responses_seen = {opt["id"]: now for p in data["prompts"] for opt in p["options"]}
            onboarding_payload = {
                "onboarding_responses": onboarding_responses,
                "onboarding_prompts_seen": onboarding_prompts_seen,
                "onboarding_responses_seen": onboarding_responses_seen,
            }
        except Exception as e:
            print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ꜰᴇᴛᴄʜ ꜰᴀɪʟ{KC.RESET}| {token_display} | {KC.BORDER}{e}{KC.RESET}")
            self.onboarding_fail_count += 1
            return
        
        try:
            post_response = self.client.post(
                f"https://discord.com/api/v10/guilds/{guild_id}/onboarding-responses",
                headers=self.headers(token), 
                json=onboarding_payload, 
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
            )
            
            response_json = post_response.json()
            if post_response.status_code == 200:
                server_name = response_json.get('guild', {}).get('name', 'Unknown Server')
                print(f"\n{SUCCESS} {time.strftime('%H:%M:%S')} | {KC.SUCCESS}ᴏɴʙᴏᴀʀᴅᴇᴅ{KC.RESET} | {token_display} | {KC.INFO}{server_name}{KC.RESET}")
                self.onboarding_success_count += 1
            else:
                message = post_response.json().get('message', 'Unknown Error')
                print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ꜰᴀɪʟᴇᴅ{KC.RESET}    | {token_display} | {KC.BORDER}{message} ({post_response.status_code}){KC.RESET}")
                self.onboarding_fail_count += 1
        except Exception as e:
            print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ᴘᴏꜱᴛ ᴇʀʀᴏʀ{KC.RESET} | {token_display} | {KC.BORDER}{e}{KC.RESET}")
            self.onboarding_fail_count += 1

    def guild_leaver(self, token: str, guild_id: str, proxy_: str = None):
        token_display = f"{KC.WHITE}{token[:35]}...{KC.RESET}"
        guild_name = guild_id
        
        try:
            res = self.client.get(
                f"https://discord.com/api/v10/guilds/{guild_id}", 
                headers=self.headers(token), 
                proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
            )
            if res.status_code == 200:
                guild_name = res.json().get('name', guild_id)
        except: 
            pass
        
        while True:
            try:
                response = self.client.delete(
                    f"https://discord.com/api/v10/users/@me/guilds/{guild_id}", 
                    json={"lurking": False}, 
                    headers=self.headers(token), 
                    proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
                )
                
                if response.status_code in [204, 200]:
                    print(f"\n{SUCCESS} {time.strftime('%H:%M:%S')} | {KC.SUCCESS}ʟᴇꜰᴛ{KC.RESET}     | {token_display} | {KC.INFO}{guild_name}{KC.RESET}")
                    self.left_count += 1
                    break 
                elif response.status_code == 429:
                    retry_after = response.json().get("retry_after", 1)
                    print(f"\n{INFO} {time.strftime('%H:%M:%S')} | {KC.WARNING}ʀᴀᴛᴇʟɪᴍɪᴛ{KC.RESET}| {token_display} | {KC.BORDER}{retry_after}s{KC.RESET}")
                    time.sleep(retry_after)
                else:
                    message = response.json().get('message', 'Unknown Error')
                    print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ꜰᴀɪʟᴇᴅ{KC.RESET}   | {token_display} | {KC.BORDER}{message} ({response.status_code}){KC.RESET}")
                    self.leave_fail_count += 1
                    break
            except Exception as e:
                print(f"\n{FAIL} {time.strftime('%H:%M:%S')} | {KC.ERROR}ᴇʀʀᴏʀ{KC.RESET}    | {token_display} | {KC.BORDER}{e}{KC.RESET}")
                self.leave_fail_count += 1
                break

    def token_checker(self, token: str, proxy_: str = None):
        token_display = f"{KC.WHITE}{token[:35]}...{KC.RESET}"
        
        while True:
            try:
                response = self.client.get(
                    "https://discord.com/api/v10/users/@me/library",
                    headers=self.headers(token),
                    proxy={"http": f"http://{proxy_}", "https": f"https://{proxy_}"} if proxy_ else None
                )
                
                status = f"{KC.BORDER}({response.status_code}){KC.RESET}"
                timestamp = time.strftime("%H:%M:%S")
                
                if response.status_code == 200:
                    print(f"\n{SUCCESS} {timestamp} | {KC.SUCCESS}ᴠᴀʟɪᴅ{KC.RESET}     | {token_display}")
                    with self.checker_lock:
                        self.valid_tokens_list.append(token)
                        self.valid_count += 1
                    break
                elif response.status_code == 403:
                    print(f"\n{FAIL} {timestamp} | {KC.WARNING}ʟᴏᴄᴋᴇᴅ{KC.RESET}   | {token_display} {status}")
                    self.locked_count += 1
                    break
                elif response.status_code == 401:
                    print(f"\n{FAIL} {timestamp} | {KC.ERROR}ɪɴᴠᴀʟɪᴅ{KC.RESET}  | {token_display} {status}")
                    self.invalid_checker_count += 1
                    break
                elif response.status_code == 429:
                    retry_after = response.json().get("retry_after", 1)
                    print(f"\n{INFO} {timestamp} | {KC.WARNING}ʀᴀᴛᴇʟɪᴍɪᴛ{KC.RESET}| {token_display} | {KC.BORDER}{retry_after}s{KC.RESET}")
                    time.sleep(retry_after)
                else:
                    message = response.json().get('message', 'Unknown Error')
                    print(f"\n{FAIL} {timestamp} | {KC.ERROR}ɪɴᴠᴀʟɪᴅ{KC.RESET}  | {token_display} {status} {KC.BORDER}{message}{KC.RESET}")
                    self.invalid_checker_count += 1
                    break
            except Exception as e:
                print(f"\n{FAIL} {timestamp} | {KC.ERROR}ᴇʀʀᴏʀ{KC.RESET}    | {token_display} | {KC.BORDER}{e}{KC.RESET}")
                self.invalid_checker_count += 1
                break

    def check(self):
        folder_path = "input"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        for file_name in ['proxies.txt', 'tokens.txt']:
            file_path = os.path.join(folder_path, file_name)
            if not os.path.exists(file_path):
                with open(file_path, "w") as file:
                    if "proxies" in file_name:
                        file.write("# Add proxies here (optional): user:pass@ip:port or ip:port\n")
                    else:
                        file.write("# Add your Discord tokens here, one per line\n")
        
        self.load_tokens()
        self.load_proxies()

    def load_tokens(self):
        self.tokens = []
        try:
            with open("input/tokens.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.tokens.append(line.split(":")[-1])
            self.total_tokens_to_process = len(self.tokens)
        except FileNotFoundError:
            self.tokens = []
            self.total_tokens_to_process = 0

    def load_proxies(self):
        self.proxies = []
        try:
            with open("input/proxies.txt", "r", encoding="utf-8") as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        self.proxies.append(line)
        except FileNotFoundError:
            pass

    def print_results_box(self, title, results):
        """Sonuçları kutu içinde göster"""
        print(f"\n{KC.BORDER}{KC.BRIGHT}╔═══════════════════════════════════════════════════════════════╗{KC.RESET}")
        print(f"{KC.BORDER}{KC.BRIGHT}║{KC.INFO}                 {title:<25}           {KC.BORDER}{KC.BRIGHT}║{KC.RESET}")
        print(f"{KC.BORDER}{KC.BRIGHT}╠═══════════════════════════════════════════════════════════════╣{KC.RESET}")
        
        for i, (label, value, color) in enumerate(results):
            if i < len(results) - 1:
                print(f"{KC.BORDER}{KC.BRIGHT}║  {color}{label:<30}{KC.RESET}{KC.BORDER}{KC.BRIGHT}: {KC.WHITE}{value:<20}{KC.BORDER}{KC.BRIGHT}║{KC.RESET}")
            else:
                print(f"{KC.BORDER}{KC.BRIGHT}║  {color}{label:<30}{KC.RESET}{KC.BORDER}{KC.BRIGHT}: {KC.WHITE}{value:<20}{KC.BORDER}{KC.BRIGHT}║{KC.RESET}")
        
        print(f"{KC.BORDER}{KC.BRIGHT}╚═══════════════════════════════════════════════════════════════╝{KC.RESET}")

    def print_joiner_results(self):
        total_processed = self.joined_count + self.invalid_count + self.hcaptcha_count
        results = [
            ("✓ Successfully Joined", self.joined_count, KC.SUCCESS),
            ("✗ Invalid Token", self.invalid_count, KC.ERROR),
            ("! HCaptcha Required", self.hcaptcha_count, KC.WARNING),
            ("Total Processed", total_processed, KC.PRIMARY)
        ]
        self.print_results_box("JOINER RESULTS", results)

    def print_button_results(self):
        total_processed = self.clicked_count + self.button_fail_count
        results = [
            ("✓ Successfully Clicked", self.clicked_count, KC.SUCCESS),
            ("✗ Failed to Click", self.button_fail_count, KC.ERROR),
            ("Total Processed", total_processed, KC.PRIMARY)
        ]
        self.print_results_box("BUTTON CLICKER RESULTS", results)
        
    def print_reactor_results(self):
        total = self.reacted_count + self.reaction_fail_count
        results = [
            ("✓ Successfully Reacted", self.reacted_count, KC.SUCCESS),
            ("✗ Failed to React", self.reaction_fail_count, KC.ERROR),
            ("Total Processed", total, KC.PRIMARY)
        ]
        self.print_results_box("REACTOR RESULTS", results)

    def print_rules_results(self):
        total_processed = self.rules_accepted_count + self.rules_fail_count
        results = [
            ("✓ Successfully Accepted", self.rules_accepted_count, KC.SUCCESS),
            ("✗ Failed to Accept", self.rules_fail_count, KC.ERROR),
            ("Total Processed", total_processed, KC.PRIMARY)
        ]
        self.print_results_box("RULES ACCEPTER RESULTS", results)
        
    def print_onboarding_results(self):
        total = self.onboarding_success_count + self.onboarding_fail_count
        results = [
            ("✓ Successfully Onboarded", self.onboarding_success_count, KC.SUCCESS),
            ("✗ Failed to Onboard", self.onboarding_fail_count, KC.ERROR),
            ("Total Processed", total, KC.PRIMARY)
        ]
        self.print_results_box("ONBOARDING RESULTS", results)

    def print_leaver_results(self):
        total = self.left_count + self.leave_fail_count
        results = [
            ("✓ Successfully Left", self.left_count, KC.SUCCESS),
            ("✗ Failed to Leave", self.leave_fail_count, KC.ERROR),
            ("Total Processed", total, KC.PRIMARY)
        ]
        self.print_results_box("GUILD LEAVER RESULTS", results)

    def print_checker_results(self):
        total = self.valid_count + self.locked_count + self.invalid_checker_count
        results = [
            ("✓ Valid", self.valid_count, KC.SUCCESS),
            ("! Locked", self.locked_count, KC.WARNING),
            ("✗ Invalid", self.invalid_checker_count, KC.ERROR),
            ("Total Processed", total, KC.PRIMARY)
        ]
        self.print_results_box("TOKEN CHECKER RESULTS", results)

    def wait_for_completion(self):
        for thread in self.threads:
            thread.join()
        self.threads = []

    def start_invite_joiner(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title Discord Multi-Tools v2.0 - Server Joiner - Made by Kenz")
        
        print(print_banner())
        print(print_stats_box(len(self.tokens), len(self.proxies)))
        print(f"{KC.BORDER}{'-'*65}{KC.RESET}\n")
        
        invite_input = input(f"{INPUT} {KC.INPUT}Invite Link : {KC.RESET}")
        delay_input = input(f"{INPUT} {KC.INPUT}Delay (seconds) : {KC.RESET}")
        
        if not invite_input:
            print(f"\n{FAIL} {KC.ERROR}No invite link provided{KC.RESET}")
            return
        
        try:
            delay = float(delay_input) if delay_input else 0
        except ValueError:
            delay = 0
        
        invite_code = invite_input.strip().split('/')[-1]
        
        print(f"\n{INFO} {KC.INFO}Starting joiner with {KC.WHITE}{len(self.tokens)}{KC.INFO} tokens...{KC.RESET}")
        print(f"{INFO} {KC.INFO}Invite Code: {KC.WHITE}{invite_code}{KC.RESET}")
        
        self.iterator = iter(self.proxies)
        for i, token in enumerate(self.tokens, 1):
            proxy = None
            if self.proxies:
                try:
                    proxy = next(self.iterator)
                except StopIteration:
                    self.iterator = iter(self.proxies)
                    proxy = next(self.iterator)
            
            if delay > 0 and i > 1:
                time.sleep(delay)
            
            thread = threading.Thread(target=self.accept_invite, args=(token, invite_code, proxy))
            self.threads.append(thread)
            thread.start()
        
        self.wait_for_completion()
        print(f"\n{KC.BORDER}{'-'*65}{KC.RESET}")
        self.print_joiner_results()

    def start_button_clicker(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title Discord Multi-Tools v2.0 - Button Clicker - Made by Kenz")
        
        print(print_banner())
        print(print_stats_box(len(self.tokens), len(self.proxies)))
        print(f"{KC.BORDER}{'-'*65}{KC.RESET}\n")
        
        message_link = input(f"{INPUT} {KC.INPUT}Message Link : {KC.RESET}")
        
        if not message_link.startswith("https://discord.com/channels/"):
            print(f"\n{FAIL} {KC.ERROR}Invalid message link format{KC.RESET}")
            return
        
        parts = message_link.strip().split('/')
        if len(parts) < 7:
            print(f"\n{FAIL} {KC.ERROR}Invalid message link{KC.RESET}")
            return
        
        guild_id, channel_id, message_id = parts[4], parts[5], parts[6]
        
        print(f"\n{INFO} {KC.INFO}Starting button clicker...{KC.RESET}")
        print(f"{INFO} {KC.INFO}Guild ID: {KC.WHITE}{guild_id}{KC.RESET}")
        print(f"{INFO} {KC.INFO}Channel ID: {KC.WHITE}{channel_id}{KC.RESET}")
        print(f"{INFO} {KC.INFO}Message ID: {KC.WHITE}{message_id}{KC.RESET}")
        
        self.iterator = iter(self.proxies)
        for token in self.tokens:
            proxy = None
            if self.proxies:
                try:
                    proxy = next(self.iterator)
                except StopIteration:
                    self.iterator = iter(self.proxies)
                    proxy = next(self.iterator)
            
            thread = threading.Thread(target=self.button_bypass, args=(token, message_id, channel_id, guild_id, proxy))
            self.threads.append(thread)
            thread.start()
        
        self.wait_for_completion()
        print(f"\n{KC.BORDER}{'-'*65}{KC.RESET}")
        self.print_button_results()

    def start_reactor(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title Discord Multi-Tools v2.0 - Reactor - Made by Kenz")
        
        print(print_banner())
        print(print_stats_box(len(self.tokens), len(self.proxies)))
        print(f"{KC.BORDER}{'-'*65}{KC.RESET}\n")
        
        message_link = input(f"{INPUT} {KC.INPUT}Message Link : {KC.RESET}")
        
        if not message_link.startswith("https://discord.com/channels/"):
            print(f"\n{FAIL} {KC.ERROR}Invalid message link format{KC.RESET}")
            return
        
        parts = message_link.strip().split('/')
        if len(parts) < 7:
            print(f"\n{FAIL} {KC.ERROR}Invalid message link{KC.RESET}")
            return
        
        guild_id, channel_id, message_id = parts[4], parts[5], parts[6]
        
        print(f"\n{INFO} {KC.INFO}Fetching message reactions...{KC.RESET}")
        
        emojis = []
        has_fetched_emojis = False
        
        for token in self.tokens[:5]:  # İlk 5 token ile dene
            try:
                res = self.client.get(
                    f"https://discord.com/api/v10/channels/{channel_id}/messages",
                    headers=self.headers(token),
                    params={"around": message_id, "limit": 50}
                )
                
                if res.status_code == 200:
                    data = res.json()
                    for msg in data:
                        if msg["id"] == message_id:
                            has_fetched_emojis = True
                            if "reactions" in msg:
                                for emois in msg["reactions"]:
                                    if emois:
                                        emoji_id = emois["emoji"]["id"]
                                        emoji_name = emois["emoji"]["name"]
                                        
                                        if emoji_id is None:
                                            emojis.append(emoji_name)
                                        else:
                                            emojis.append(f"{emoji_name}:{emoji_id}")
                            break
            except Exception:
                continue
        
        if not has_fetched_emojis:
            print(f"\n{FAIL} {KC.ERROR}Could not access message{KC.RESET}")
            custom_emoji = input(f"{INPUT} {KC.INPUT}Enter emoji manually (or name:id) : {KC.RESET}")
            if not custom_emoji:
                return
            selected_emoji = custom_emoji
        else:
            if not emojis:
                print(f"\n{INFO} {KC.WARNING}No reactions found{KC.RESET}")
                custom_emoji = input(f"{INPUT} {KC.INPUT}Enter emoji manually (or name:id) : {KC.RESET}")
                if not custom_emoji:
                    return
                selected_emoji = custom_emoji
            else:
                print(f"\n{INFO} {KC.INFO}Available reactions:{KC.RESET}")
                for i, emoji in enumerate(emojis, 1):
                    display_emoji = f":{emoji.split(':')[0]}:" if ':' in emoji else emoji
                    print(f"  {KC.BRIGHT}[{KC.PRIMARY}{i}{KC.BRIGHT}]{KC.RESET} {KC.WHITE}{display_emoji}{KC.RESET}")
                
                print(f"\n  {KC.BRIGHT}[{KC.PRIMARY}0{KC.BRIGHT}]{KC.RESET} {KC.WHITE}Custom emoji{KC.RESET}")
                
                choice_str = input(f"\n{INPUT} {KC.INPUT}Choose : {KC.RESET}")
                
                if not choice_str:
                    return
                
                if choice_str == "0":
                    custom_emoji = input(f"{INPUT} {KC.INPUT}Enter custom emoji : {KC.RESET}")
                    if not custom_emoji:
                        return
                    selected_emoji = custom_emoji
                else:
                    try:
                        choice = int(choice_str)
                        selected_emoji = emojis[choice - 1]
                    except (ValueError, IndexError):
                        print(f"\n{FAIL} {KC.ERROR}Invalid choice{KC.RESET}")
                        return
        
        display_selected_emoji = f":{selected_emoji.split(':')[0]}:" if ':' in selected_emoji else selected_emoji
        print(f"\n{INFO} {KC.INFO}Reacting with {KC.WHITE}{display_selected_emoji}{KC.INFO} using {KC.WHITE}{len(self.tokens)}{KC.INFO} tokens{KC.RESET}")
        
        self.iterator = iter(self.proxies)
        for token in self.tokens:
            proxy = None
            if self.proxies:
                try:
                    proxy = next(self.iterator)
                except StopIteration:
                    self.iterator = iter(self.proxies)
                    proxy = next(self.iterator)
            
            thread = threading.Thread(target=self.add_reaction, args=(token, channel_id, message_id, selected_emoji, proxy))
            self.threads.append(thread)
            thread.start()
        
        self.wait_for_completion()
        print(f"\n{KC.BORDER}{'-'*65}{KC.RESET}")
        self.print_reactor_results()

    def start_rules_accepter(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title Discord Multi-Tools v2.0 - Rules Accepter - Made by Kenz")
        
        print(print_banner())
        print(print_stats_box(len(self.tokens), len(self.proxies)))
        print(f"{KC.BORDER}{'-'*65}{KC.RESET}\n")
        
        guild_id = input(f"{INPUT} {KC.INPUT}Guild ID : {KC.RESET}")
        
        if not guild_id.isdigit():
            print(f"\n{FAIL} {KC.ERROR}Invalid Guild ID format{KC.RESET}")
            return
        
        print(f"\n{INFO} {KC.INFO}Accepting rules for {KC.WHITE}{len(self.tokens)}{KC.INFO} tokens...{KC.RESET}")
        
        self.iterator = iter(self.proxies)
        for token in self.tokens:
            proxy = next(self.iterator, None)
            thread = threading.Thread(target=self.accept_rules, args=(token, guild_id, proxy))
            self.threads.append(thread)
            thread.start()
        
        self.wait_for_completion()
        print(f"\n{KC.BORDER}{'-'*65}{KC.RESET}")
        self.print_rules_results()
        
    def start_onboarding_bypass(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title Discord Multi-Tools v2.0 - Onboarding Bypass - Made by Kenz")
        
        print(print_banner())
        print(print_stats_box(len(self.tokens), len(self.proxies)))
        print(f"{KC.BORDER}{'-'*65}{KC.RESET}\n")
        
        guild_id = input(f"{INPUT} {KC.INPUT}Guild ID : {KC.RESET}")
        
        if not guild_id.isdigit():
            print(f"\n{FAIL} {KC.ERROR}Invalid Guild ID{KC.RESET}")
            return
        
        print(f"\n{INFO} {KC.INFO}Bypassing onboarding for {KC.WHITE}{len(self.tokens)}{KC.INFO} tokens...{KC.RESET}")
        
        self.iterator = iter(self.proxies)
        for token in self.tokens:
            proxy = next(self.iterator, None)
            thread = threading.Thread(target=self.onboarding_bypass, args=(token, guild_id, proxy))
            self.threads.append(thread)
            thread.start()
        
        self.wait_for_completion()
        print(f"\n{KC.BORDER}{'-'*65}{KC.RESET}")
        self.print_onboarding_results()

    def start_guild_leaver(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title Discord Multi-Tools v2.0 - Guild Leaver - Made by Kenz")
        
        print(print_banner())
        print(print_stats_box(len(self.tokens), len(self.proxies)))
        print(f"{KC.BORDER}{'-'*65}{KC.RESET}\n")
        
        guild_id = input(f"{INPUT} {KC.INPUT}Guild ID : {KC.RESET}")
        
        if not guild_id.isdigit():
            print(f"\n{FAIL} {KC.ERROR}Invalid Guild ID{KC.RESET}")
            return
        
        print(f"\n{INFO} {KC.INFO}Leaving guild with {KC.WHITE}{len(self.tokens)}{KC.INFO} tokens...{KC.RESET}")
        
        self.iterator = iter(self.proxies)
        for token in self.tokens:
            proxy = next(self.iterator, None)
            thread = threading.Thread(target=self.guild_leaver, args=(token, guild_id, proxy))
            self.threads.append(thread)
            thread.start()
        
        self.wait_for_completion()
        print(f"\n{KC.BORDER}{'-'*65}{KC.RESET}")
        self.print_leaver_results()

    def start_token_checker(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system(f"title Discord Multi-Tools v2.0 - Token Checker - Made by Kenz")
        
        print(print_banner())
        print(print_stats_box(len(self.tokens), len(self.proxies)))
        print(f"{KC.BORDER}{'-'*65}{KC.RESET}\n")
        
        print(f"{INFO} {KC.INFO}Checking {KC.WHITE}{len(self.tokens)}{KC.INFO} tokens...{KC.RESET}")
        
        self.iterator = iter(self.proxies)
        for i, token in enumerate(self.tokens, 1):
            proxy = None
            if self.proxies:
                try:
                    proxy = next(self.iterator)
                except StopIteration:
                    self.iterator = iter(self.proxies)
                    proxy = next(self.iterator)
            
            thread = threading.Thread(target=self.token_checker, args=(token, proxy))
            self.threads.append(thread)
            thread.start()
            
            # İlerleme çubuğu
            if i % 5 == 0 or i == len(self.tokens):
                self.print_progress(i, len(self.tokens), f"{INFO} {KC.INFO}Progress: {KC.RESET}")
        
        print()  # Yeni satır
        self.wait_for_completion()
        
        # Geçerli token'ları kaydet
        try:
            with open("input/tokens.txt", "w", encoding="utf-8") as f:
                for token in self.valid_tokens_list:
                    f.write(f"{token}\n")
            print(f"\n{SUCCESS} {KC.SUCCESS}Saved {KC.WHITE}{len(self.valid_tokens_list)}{KC.SUCCESS} valid tokens to {KC.WHITE}input/tokens.txt{KC.RESET}")
        except Exception as e:
            print(f"\n{FAIL} {KC.ERROR}Could not save valid tokens: {KC.BORDER}{e}{KC.RESET}")
        
        print(f"\n{KC.BORDER}{'-'*65}{KC.RESET}")
        self.print_checker_results()

    def start(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            os.system(f"title Discord Multi-Tools v2.0 - Main Menu - Made by Kenz")
            
            print(print_banner())
            print(print_stats_box(len(self.tokens), len(self.proxies)))
            print(print_menu())
            
            if not self.tokens:
                print(f"\n{FAIL} {KC.ERROR}No tokens found in {KC.WHITE}input/tokens.txt{KC.RESET}")
                print(f"{INFO} {KC.INFO}Please add tokens to the file and restart.{KC.RESET}")
                input(f"\n{INPUT} {KC.INPUT}Press Enter to exit...{KC.RESET}")
                return
            
            choice = input(f"\n{INPUT} {KC.INPUT}Select option : {KC.RESET}")
            
            if choice == '1':
                self.start_invite_joiner()
            elif choice == '2':
                self.start_guild_leaver()
            elif choice == '3':
                self.start_token_checker()
            elif choice == '4':
                self.start_button_clicker()
            elif choice == '5':
                self.start_reactor()
            elif choice == '6':
                self.start_rules_accepter()
            elif choice == '7':
                self.start_onboarding_bypass()
            elif choice == '8':
                print(f"\n{INFO} {KC.INFO}Exiting... Goodbye!{KC.RESET}")
                time.sleep(1)
                sys.exit(0)
            elif choice == '0':
                # Verileri yenile
                self.load_tokens()
                self.load_proxies()
                print(f"\n{SUCCESS} {KC.SUCCESS}Data refreshed!{KC.RESET}")
                time.sleep(1)
                continue
            else:
                print(f"\n{FAIL} {KC.ERROR}Invalid option!{KC.RESET}")
                time.sleep(1)
                continue
            
            # İşlem tamamlandıktan sonra
            restart = input(f"\n{INPUT} {KC.INPUT}Press Enter to return to menu...{KC.RESET}")
            if restart.lower() == 'exit':
                print(f"\n{INFO} {KC.INFO}Exiting... Goodbye!{KC.RESET}")
                time.sleep(1)
                sys.exit(0)
            
            # İstatistikleri sıfırla
            self.joined_count = 0
            self.invalid_count = 0
            self.hcaptcha_count = 0
            self.clicked_count = 0
            self.button_fail_count = 0
            self.reacted_count = 0
            self.reaction_fail_count = 0
            self.rules_accepted_count = 0
            self.rules_fail_count = 0
            self.onboarding_fail_count = 0
            self.onboarding_success_count = 0
            self.left_count = 0
            self.leave_fail_count = 0
            self.valid_count = 0
            self.locked_count = 0
            self.invalid_checker_count = 0
            self.valid_tokens_list = []


if __name__ == '__main__':
    try:
        tool = DiscordJoinerPY()
        tool.start()
    except KeyboardInterrupt:
        print(f"\n\n{INFO} {KC.INFO}Program interrupted by user.{KC.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{FAIL} {KC.ERROR}Fatal error: {KC.BORDER}{e}{KC.RESET}")
        input(f"\n{INPUT} {KC.INPUT}Press Enter to exit...{KC.RESET}")