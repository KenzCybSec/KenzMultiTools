import io
import time
import uuid
import concurrent.futures
from base64 import b64encode
from json import dumps, loads, JSONDecodeError
from pathlib import Path
from platform import system, release, version
from random import choice
from typing import Optional, List, Tuple, Any, Dict, Union

from PIL import Image
import tls_client
import websocket

# --- Mock Dependencies ---

class NexusColor:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

class GradientPrinter:
    @staticmethod
    def gradient_print(input_text, start_color, end_color, prefix=""):
        # Simplified to just print with the prefix
        print(f"{prefix}{input_text}")

class Logger:
    STATUS = ""
    LC = "[Humanizer] "

    @staticmethod
    def queue_log(worker_id, overwrite=False):
        print(f"[{worker_id}] {Logger.STATUS}{NexusColor.RESET}")

    @staticmethod
    def log_procces(overwrite=False):
        print(f"{Logger.LC}{Logger.STATUS}{NexusColor.RESET}")

class Config:
    # Default configuration
    config = {
        "bio": True,
        "display_name": True,
        "pronouns": True,
        "avatar": True,
        "hypesquad": True,
        "debug": False # Enable debug mode by default as requested
    }

# --- End Mock Dependencies ---

# --- From discord.py ---

class HeaderGenerator:
    def __init__(self) -> None:
        self.base_chrome_version: int = 120
        self.impersonate_target: str = f"chrome_{self.base_chrome_version}"
        self.session: tls_client.Session = tls_client.Session(client_identifier=self.impersonate_target)
        self.ua_details: Dict[str, Any] = self._generate_ua_details()
        self._header_cache: Dict[Any, Dict[str, Any]] = {}
        self._cookie_cache: Dict[str, Dict[str, Any]] = {}

    def _generate_ua_details(self) -> Dict[str, Any]:
        chrome_major: int = self.base_chrome_version
        full_version: str = f"{chrome_major}.0.0.0"

        os_spec: str = self._get_os_string()
        platform_ua: str = f"Windows NT {release()}; Win64; x64" if "Windows" in os_spec else os_spec

        return {
            "user_agent": (
                f"Mozilla/5.0 ({platform_ua}) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Chrome/{full_version} Safari/537.36 Edg/{full_version}"
            ),
            "chrome_version": full_version,
            "sec_ch_ua": [
                f'"Google Chrome";v="{chrome_major}"',
                f'"Chromium";v="{chrome_major}"',
                '"Not/A)Brand";v="99"'
            ]
        }

    def _get_os_string(self) -> str:
        os_map: Dict[str, str] = {
            "Windows": f"Windows NT 10.0; Win64; x64",
            "Linux": "X11; Linux x86_64",
            "Darwin": "Macintosh; Intel Mac OS X 10_15_7"
        }
        os_str: str = os_map.get(system(), "Windows NT 10.0; Win64; x64")

        if system() == "Windows":
            win_ver: list[str] = version().split('.')
            if len(win_ver) >= 2:
                os_str = f"Windows NT {win_ver[0]}.{win_ver[1]}; Win64; x64"

        return os_str

    def fetch_cookies(self, token: str) -> str:
        now: float = time.time()
        cache_entry: Optional[Dict[str, Any]] = self._cookie_cache.get(token)
        if cache_entry and now - cache_entry["timestamp"] < 86400:
            return cache_entry["cookie"]

        try:
            resp = self.session.get(
                "https://discord.com/api/v9/users/@me",
                headers={"Authorization": token}
                )

            cookies: list[str] = []
            if "set-cookie" in resp.headers:
                set_cookie: Union[str, list[str]] = resp.headers["set-cookie"]
                if isinstance(set_cookie, list):
                    set_cookie = ", ".join(set_cookie)

                for cookie in set_cookie.split(", "):
                    cookie_part = cookie.split(";")[0]
                    if "=" in cookie_part:
                        name, value = cookie_part.split("=", 1)
                        cookies.append(f"{name}={value}")

            cookie_str: str = "; ".join(cookies)
            self._cookie_cache[token] = {"cookie": cookie_str, "timestamp": now}
            return cookie_str
        except Exception as e:
            GradientPrinter.gradient_print(
                input_text=f"Cookie fetch failed: {e}",
                start_color="#ff08b5",
                end_color="#8308ff",
                prefix=Logger.LC
            )
            return ""

    def generate_super_properties(self) -> str:
        sp: Dict[str, Any] = {
            "os": system(),
            "browser": "Chrome",
            "device": "",
            "system_locale": "en-US",
            "browser_user_agent": self.ua_details["user_agent"],
            "browser_version": self.ua_details["chrome_version"].split(".0.")[0] + ".0.0.0",
            "os_version": str(release()),
            "referrer": "https://discord.com/",
            "referring_domain": "discord.com",
            "search_engine": "google",
            "release_channel": "stable",
            "client_build_number": 438971,
            "client_event_source": None,
            "has_client_mods": False,
            "client_launch_id": str(uuid.uuid4()),
            "launch_signature": str(uuid.uuid4()),
            "client_heartbeat_session_id": str(uuid.uuid4()),
            "client_app_state": "focused"
        }
        return b64encode(dumps(sp, separators=(',', ':')).encode()).decode()

    def generate_context_properties(self, location: str, **kwargs) -> str:
        valid_locations = {
            "Add Friend", "User Profile", "Guild Member List",
            "Accept Invite Page", "DM Header", "Friend Request Settings",
            "bite size profile popout", "Add Friends to DM", "Friends",
            "{}"
        }

        if location == "{}":
            return "e30="

        if location not in valid_locations:
            raise ValueError(f"Invalid location: {location}. Valid options: {valid_locations}")

        context: Dict[str, str] = {"location": location}
        return b64encode(dumps(context).encode()).decode()

    def generate_headers(self, token: str, location: Optional[str] = None, **kwargs) -> Dict[str, str]:
        x_context_props: Optional[str] = None
        if location:
            try:
                x_context_props = self.generate_context_properties(location, token=token, **kwargs)
            except Exception as e:
                GradientPrinter.gradient_print(
                    input_text=f"Context properties generation failed: {e}",
                    start_color="#ff08b5",
                    end_color="#8308ff",
                    prefix=Logger.LC
                )

        cache_key = ('no_context',) if x_context_props is None else ('has_context', x_context_props)
        now: float = time.time()
        cached_entry = self._header_cache.get(cache_key)

        if cached_entry and (now - cached_entry['timestamp'] < 86400):
            base_headers = cached_entry['headers'].copy()
        else:
            base_headers: Dict[str, str] = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br, zstd',
                'Accept-Language': 'en;q=1.0',
                'content-type': 'application/json',
                'origin': 'https://discord.com',
                'priority': 'u=1, i',
                "sec-ch-ua": ", ".join(self.ua_details["sec_ch_ua"]),
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                "user-agent": self.ua_details["user_agent"],
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-discord-timezone": "America/Los_Angeles",
                "x-super-properties": self.generate_super_properties()
            }

            if x_context_props:
                base_headers["x-context-properties"] = x_context_props

            self._header_cache[cache_key] = {"headers": base_headers.copy(), "timestamp": now}

        headers = base_headers.copy()
        headers["Authorization"] = token
        headers["cookie"] = self.fetch_cookies(token)

        return headers


def get_session_id(token: str) -> Tuple[Union[str, None], Optional[websocket.WebSocket], Optional[float]]:
    ws: websocket.WebSocket = websocket.WebSocket()
    try:
        ws.connect("wss://gateway.discord.gg/?v=9&encoding=json")

        hello: dict = loads(ws.recv())
        heartbeat_interval: float = hello["d"]["heartbeat_interval"] / 1000

        payload: dict = {
            "op": 2,
            "d": {
                "token": token,
                "properties": {"$os": "Windows"},
            },
        }

        ws.send(dumps(payload))

        while True:
            response: dict = loads(ws.recv())
            op: int = response.get("op", -1)
            event: Optional[str] = response.get("t")

            if event == "READY":
                return response["d"]["session_id"], ws, heartbeat_interval
            if op == 9:
                return "Invalid token", None, None
            if op == 429:
                return "Rate limited", None, None

    except websocket.WebSocketException as e:
        return f"WebSocket error: {e}", None, None
    except JSONDecodeError as e:
        return f"JSON error: {e}", None, None

# --- From huminazer.py ---

class DiscordHuminazer:
    def __init__(self, worker_id: int) -> None:
        self.header_gen: HeaderGenerator = HeaderGenerator()
        self.profile_dir: Path = Path("io/input/profiles")
        self.avatar_dir: Path = self.profile_dir / "avatars"
        self.config: dict = Config.config

        self.bios: Optional[List[str]] = self._load_from_file("bio.txt") if self.config.get("bio", True) else None
        self.names: Optional[List[str]] = self._load_from_file("names.txt") if self.config.get("display_name", True) else None
        self.pronouns_list: Optional[List[str]] = self._load_from_file("pronouns.txt") if self.config.get("pronouns", True) else None
        self.houses: List[str] = ["bravery", "brillance", "balance"]
        self.worker_id: int = worker_id

    def _log_debug(self, method: str, url: str, payload: Optional[dict] = None, response: Optional[Any] = None, error: Optional[str] = None):
        if not self.config.get("debug", False):
            return

        print(f"\n{NexusColor.YELLOW}[DEBUG] Request:{NexusColor.RESET}")
        print(f"  Method: {method}")
        print(f"  URL: {url}")
        if payload:
            print(f"  Payload: {dumps(payload, indent=2)}")
        
        if response:
            print(f"{NexusColor.YELLOW}[DEBUG] Response:{NexusColor.RESET}")
            print(f"  Status: {response.status_code}")
            try:
                print(f"  Body: {response.text}")
            except:
                print("  Body: <Could not read text>")
        
        if error:
            print(f"{NexusColor.RED}[DEBUG] Error: {error}{NexusColor.RESET}")
        print("-" * 50)
        
    def _load_from_file(self, filename: str) -> Optional[List[str]]:
        file_path = self.profile_dir / filename
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        return None

    def _get_random_bio(self) -> Optional[str]:
        return choice(self.bios) if self.bios else None

    def _get_random_display_name(self) -> Optional[str]:
        return choice(self.names) if self.names else None

    def _get_random_pronouns(self) -> Optional[str]:
        return choice(self.pronouns_list) if self.pronouns_list else None

    def _get_random_avatar(self) -> Optional[Path]:
        if not self.config.get("avatar", True):
            return None
        avatar_files = list(self.avatar_dir.glob("*.png")) + list(self.avatar_dir.glob("*.jpg"))
        return choice(avatar_files) if avatar_files else None

    def _prepare_avatar(self, path: Path, max_size_mb: int = 8) -> Optional[str]:
        max_bytes: int = max_size_mb * 1024 * 1024

        with Image.open(path) as img:
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            data = buffer.getvalue()

            while len(data) > max_bytes:
                w, h = img.size
                if w < 64 or h < 64:
                    break
                img = img.resize((w // 2, h // 2), Image.LANCZOS)
                buffer = io.BytesIO()
                img.save(buffer, format="PNG", optimize=True)
                data = buffer.getvalue()

        if len(data) > max_bytes:
            return None
        return b64encode(data).decode("utf-8")

    def humanize_account(self, token: str, proxy_dict: dict) -> bool:
        try:
            server_url: str = proxy_dict['server']
            if server_url.startswith('http://'):
                server_url = server_url[7:]

            proxy_url: str
            if 'username' in proxy_dict and 'password' in proxy_dict:
                proxy_url = f"http://{proxy_dict['username']}:{proxy_dict['password']}@{server_url}"
            else:
                proxy_url = f"http://{server_url}"

            return self._update_profile(token, proxy_url)
        except Exception as e:
            Logger.STATUS = f"{NexusColor.RED}Error during humanization."
            Logger.queue_log(worker_id=self.worker_id, overwrite=False)
            return False

    def _update_profile(self, token: str, proxy_url: str) -> bool:
        try:
            headers: dict = self.header_gen.generate_headers(token, location="User Profile")

            with tls_client.Session(client_identifier="chrome_120", random_tls_extension_order=True) as session:
                session.proxies = {'http': proxy_url, 'https': proxy_url}
                session.headers.update(headers)
                success: bool = True

                if self.config.get("bio", True):
                    bio = self._get_random_bio()
                    if bio:
                        self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload={"bio": bio})
                        r = session.patch("https://discord.com/api/v9/users/@me", json={"bio": bio})
                        self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload={"bio": bio}, response=r)
                        if r.status_code != 200:
                            Logger.STATUS = f"{NexusColor.RED}Failed to update bio"
                            Logger.queue_log(worker_id=self.worker_id, overwrite=False)
                            success = False

                if self.config.get("pronouns", True):
                    pronouns = self._get_random_pronouns()
                    if pronouns:
                        self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload={"pronouns": pronouns})
                        r = session.patch("https://discord.com/api/v9/users/@me", json={"pronouns": pronouns})
                        self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload={"pronouns": pronouns}, response=r)
                        if r.status_code != 200:
                            Logger.STATUS = f"{NexusColor.RED}Failed to update pronouns"
                            Logger.queue_log(worker_id=self.worker_id, overwrite=False)
                            success = False

                if self.config.get("display_name", True):
                    display_name = self._get_random_display_name()
                    if display_name:
                        self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload={"global_name": display_name})
                        r = session.patch("https://discord.com/api/v9/users/@me", json={"global_name": display_name})
                        self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload={"global_name": display_name}, response=r)
                        if r.status_code != 200:
                            Logger.STATUS = f"{NexusColor.RED}Failed to update display name"
                            Logger.queue_log(worker_id=self.worker_id, overwrite=False)
                            success = False

                if self.config.get("hypesquad", True):
                    house = choice(self.houses)
                    house_id = self.houses.index(house) + 1
                    if house_id:
                        self._log_debug("POST", "https://discord.com/api/v9/hypesquad/online", payload={"house_id": house_id})
                        r = session.post(
                            "https://discord.com/api/v9/hypesquad/online",
                            json={"house_id": house_id}
                            )
                        self._log_debug("POST", "https://discord.com/api/v9/hypesquad/online", payload={"house_id": house_id}, response=r)
                        if r.status_code != 204:
                            Logger.STATUS = f"{NexusColor.RED}Failed to join Hypesquad"
                            Logger.log_procces(overwrite=False)
                            success = False

                if self.config.get("avatar", True):
                    avatar_path = self._get_random_avatar()
                    if avatar_path:
                        avatar_b64 = self._prepare_avatar(avatar_path)
                        if avatar_b64:
                            get_session_id(token)
                            payload = {"avatar": f"data:image/png;base64,{avatar_b64[:20]}..."} # Truncate for log
                            self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload=payload)
                            r = session.patch(
                                "https://discord.com/api/v9/users/@me",
                                json={"avatar": f"data:image/png;base64,{avatar_b64}"}
                                )
                            self._log_debug("PATCH", "https://discord.com/api/v9/users/@me", payload=payload, response=r)
                            if r.status_code != 200:
                                Logger.STATUS = f"{NexusColor.RED}Failed to update avatar"
                                Logger.queue_log(worker_id=self.worker_id, overwrite=False)
                                success = False

                return success
        except Exception as e:
            error_msg = str(e)
            self._log_debug("ERROR", "N/A", error=error_msg)
            if "connection refused" in error_msg.lower():
                Logger.STATUS = f"{NexusColor.RED}Proxy connection failed (Connection Refused)"
            elif "timeout" in error_msg.lower():
                Logger.STATUS = f"{NexusColor.RED}Proxy connection timed out"
            else:
                Logger.STATUS = f"{NexusColor.RED}Error updating profile: {error_msg}"
            
            Logger.queue_log(worker_id=self.worker_id, overwrite=False)
            return False

# --- New Components ---

class ProxyManager:
    def __init__(self, proxy_file: str = "io/input/proxies.txt"):
        self.proxy_file = Path(proxy_file)
        self.proxies = self._load_proxies()

    def _load_proxies(self) -> List[dict]:
        proxies = []
        if not self.proxy_file.exists():
            print(f"{NexusColor.RED}Proxy file not found: {self.proxy_file}{NexusColor.RESET}")
            return []
        
        with open(self.proxy_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split(':')
                if len(parts) == 2: # ip:port
                    proxies.append({'server': f"{parts[0]}:{parts[1]}"})
                elif len(parts) == 4: # ip:port:user:pass or user:pass:ip:port (assuming user:pass:ip:port based on common formats, but user asked for ip:port support. Let's support user:pass@ip:port format if passed as string, but here we parse parts)
                    # Common format is often ip:port:user:pass or user:pass:ip:port. 
                    # Let's assume user:pass:ip:port for 4 parts if not specified, but standard is often ip:port:user:pass.
                    # Actually, let's just support the standard user:pass@ip:port string construction here.
                    # If the line is just 4 parts separated by colons, it's ambiguous. 
                    # Let's try to detect. Usually ports are numbers.
                    # If parts[1] is numeric, it might be ip:port:user:pass
                    # If parts[3] is numeric, it might be user:pass:ip:port
                    
                    if parts[1].isdigit(): # ip:port:user:pass
                        proxies.append({
                            'server': f"{parts[0]}:{parts[1]}",
                            'username': parts[2],
                            'password': parts[3]
                        })
                    elif parts[3].isdigit(): # user:pass:ip:port
                        proxies.append({
                            'server': f"{parts[2]}:{parts[3]}",
                            'username': parts[0],
                            'password': parts[1]
                        })
                elif '@' in line: # user:pass@ip:port
                    user_pass, ip_port = line.split('@')
                    user, password = user_pass.split(':')
                    proxies.append({
                        'server': ip_port,
                        'username': user,
                        'password': password
                    })
                else:
                     proxies.append({'server': line}) # Fallback

        return proxies

    def get_random_proxy(self) -> Optional[dict]:
        return choice(self.proxies) if self.proxies else None

class TokenManager:
    def __init__(self, token_file: str = "io/input/tokens.txt"):
        self.token_file = Path(token_file)
        self.tokens = self._load_tokens()

    def _load_tokens(self) -> List[str]:
        tokens = []
        if not self.token_file.exists():
            print(f"{NexusColor.RED}Token file not found: {self.token_file}{NexusColor.RESET}")
            return []

        with open(self.token_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Extract token from email:pass:token, email:token, or just token
                # Simple heuristic: tokens are usually long strings. 
                # If there are colons, the token is likely the last part.
                parts = line.split(':')
                if len(parts) >= 2:
                    # Assume email:pass:token or email:token format, token is last
                    tokens.append(parts[-1])
                else:
                    # Assume just token
                    tokens.append(line)
        return tokens

def print_banner():
    banner = """
██╗  ██╗███████╗███╗   ██╗███████╗
██║ ██╔╝██╔════╝████╗  ██║╚══███╔╝
█████╔╝ █████╗  ██╔██╗ ██║  ███╔╝ 
██╔═██╗ ██╔══╝  ██║╚██╗██║ ███╔╝  
██║  ██╗███████╗██║ ╚████║███████╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝
                                      """
    GradientPrinter.gradient_print(banner, "#ff08b5", "#8308ff")
    print(f"{NexusColor.CYAN}          Discord Account Humanizer Tool{NexusColor.RESET}\n")

def process_token(token: str, proxy_manager: ProxyManager, worker_id: int):
    proxy = proxy_manager.get_random_proxy()
    if not proxy:
            print(f"{NexusColor.YELLOW}Warning: No proxies available. Running without proxy.{NexusColor.RESET}")
            proxy = {'server': ''} 
    
    humanizer = DiscordHuminazer(worker_id=worker_id)
    print(f"[{worker_id}] Processing token: {token[:20]}...")
    success = humanizer.humanize_account(token, proxy)
    
    status = f"{NexusColor.GREEN}Success{NexusColor.RESET}" if success else f"{NexusColor.RED}Failed{NexusColor.RESET}"
    print(f"[{worker_id}] Result: {status}")

if __name__ == "__main__":
    print_banner()
    
    token_manager = TokenManager()
    proxy_manager = ProxyManager()
    
    if not token_manager.tokens:
        print(f"{NexusColor.RED}No tokens found! Exiting...{NexusColor.RESET}")
        exit()
        
    print(f"{NexusColor.GREEN}Loaded {len(token_manager.tokens)} tokens.{NexusColor.RESET}")
    print(f"{NexusColor.GREEN}Loaded {len(proxy_manager.proxies)} proxies.{NexusColor.RESET}")
    
    max_workers = 50
    print(f"{NexusColor.CYAN}Starting with {max_workers} threads...{NexusColor.RESET}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for i, token in enumerate(token_manager.tokens, 1):
            futures.append(executor.submit(process_token, token, proxy_manager, i))
        
        concurrent.futures.wait(futures)

