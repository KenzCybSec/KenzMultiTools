import asyncio
import json
import re
import time
import random
import string
import requests
import os
from datetime import datetime

# TOKEN GEN BANNER
BANNER = """
████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗ ██████╗ ███████╗███╗   ██╗
╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║██╔════╝ ██╔════╝████╗  ██║
   ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║██║  ███╗█████╗  ██╔██╗ ██║
   ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║██║   ██║██╔══╝  ██║╚██╗██║
   ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║╚██████╔╝███████╗██║ ╚████║
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝
"""

session = requests.Session()
rate_limit = False
page = None
auth_token = None
verify_event = asyncio.Event()

BLOCKED_DOMAINS = ["chessgameland.com"]

# Token kayıt dosyası
TOKENS_FILE = "tokens.txt"

def clog(level: str, msg: str):
    """Custom log function"""
    level = level.lower()
    if level == "warn":
        level = "warning"
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] | [{level.upper():^5}] | {msg}")

def show_banner():
    """Show Token Gen banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    colors = ["cyan", "cyan", "cyan", "cyan", "cyan", "cyan"]
    banner_lines = BANNER.strip().split('\n')
    
    for i, line in enumerate(banner_lines):
        if i < len(colors):
            color = colors[i]
        else:
            color = "cyan"
        
        # Simple color printing
        if color == "cyan":
            print(f"\033[96m{line}\033[0m")
        else:
            print(line)
    
    print("\n" + "═" * 60)
    clog("info", "🚀 Starting Token Generator...")
    clog("info", f"📁 Tokens will be saved to: {TOKENS_FILE}")
    print("═" * 60 + "\n")

def random_username(length=12):
    return "".join(random.choices(string.ascii_letters, k=length)).lower()

def random_password(length=12):
    base = "kenz"
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length-4))
    return (base + random_chars).lower()

async def select_birthday_simple(page):
    """Simple birthday selection that works with most Discord versions"""
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    
    # Random birthday (1995-1999)
    year = random.randint(1995, 1999)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    month_name = months[month - 1]
    
    clog("info", f"📅 Selecting birthday: {day} {month_name} {year}")
    
    try:
        # Method 1: Try to find and click month dropdown
        month_selectors = [
            '[aria-label*="month"]',
            '[placeholder*="month"]',
            'select[name*="month"]',
            'div[class*="month"]',
            'button:has-text("Month")'
        ]
        
        month_selected = False
        for selector in month_selectors:
            try:
                if await page.locator(selector).count() > 0:
                    await page.locator(selector).first.click()
                    await asyncio.sleep(0.5)
                    await page.locator(f'div[role="option"]:has-text("{month_name}")').first.click()
                    await asyncio.sleep(0.5)
                    clog("success", f"✅ Month selected: {month_name}")
                    month_selected = True
                    break
            except:
                continue
        
        if not month_selected:
            # Try alternative method for month
            try:
                await page.evaluate(f"""
                    () => {{
                        const monthSelect = document.querySelector('select[name*="month"], [aria-label*="month"]');
                        if (monthSelect && monthSelect.tagName === 'SELECT') {{
                            monthSelect.value = "{month}";
                            monthSelect.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }}
                """)
                clog("info", f"📝 Month set via JavaScript: {month}")
            except:
                clog("warning", "⚠️ Could not select month")
        
        # Method 2: Try to find and click day dropdown
        day_selectors = [
            '[aria-label*="day"]',
            '[placeholder*="day"]',
            'select[name*="day"]',
            'div[class*="day"]',
            'button:has-text("Day")'
        ]
        
        day_selected = False
        for selector in day_selectors:
            try:
                if await page.locator(selector).count() > 0:
                    await page.locator(selector).first.click()
                    await asyncio.sleep(0.5)
                    await page.locator(f'div[role="option"]:has-text("{day}")').first.click()
                    await asyncio.sleep(0.5)
                    clog("success", f"✅ Day selected: {day}")
                    day_selected = True
                    break
            except:
                continue
        
        if not day_selected:
            # Try alternative method for day
            try:
                await page.evaluate(f"""
                    () => {{
                        const daySelect = document.querySelector('select[name*="day"], [aria-label*="day"]');
                        if (daySelect && daySelect.tagName === 'SELECT') {{
                            daySelect.value = "{day}";
                            daySelect.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }}
                """)
                clog("info", f"📝 Day set via JavaScript: {day}")
            except:
                clog("warning", "⚠️ Could not select day")
        
        # Method 3: Try to find and click year dropdown
        year_selectors = [
            '[aria-label*="year"]',
            '[placeholder*="year"]',
            'select[name*="year"]',
            'div[class*="year"]',
            'button:has-text("Year")'
        ]
        
        year_selected = False
        for selector in year_selectors:
            try:
                if await page.locator(selector).count() > 0:
                    await page.locator(selector).first.click()
                    await asyncio.sleep(0.5)
                    await page.locator(f'div[role="option"]:has-text("{year}")').first.click()
                    await asyncio.sleep(0.5)
                    clog("success", f"✅ Year selected: {year}")
                    year_selected = True
                    break
            except:
                continue
        
        if not year_selected:
            # Try alternative method for year
            try:
                await page.evaluate(f"""
                    () => {{
                        const yearSelect = document.querySelector('select[name*="year"], [aria-label*="year"]');
                        if (yearSelect && yearSelect.tagName === 'SELECT') {{
                            yearSelect.value = "{year}";
                            yearSelect.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }}
                """)
                clog("info", f"📝 Year set via JavaScript: {year}")
            except:
                clog("warning", "⚠️ Could not select year")
        
        clog("success", f"✅ Birthday selected: {day}/{month}/{year}")
        return True
        
    except Exception as e:
        clog("error", f"❌ Error selecting birthday: {e}")
        return False

def save_token(email, password, token):
    """Save token to tokens.txt in format: email:password:token"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(TOKENS_FILE) if os.path.dirname(TOKENS_FILE) else '.', exist_ok=True)
        
        # Format: email:password:token
        token_entry = f"{email}:{password}:{token}\n"
        
        # Check if token already exists
        token_exists = False
        if os.path.exists(TOKENS_FILE):
            with open(TOKENS_FILE, 'r', encoding='utf-8') as f:
                existing_tokens = f.readlines()
                for line in existing_tokens:
                    if token in line:
                        token_exists = True
                        break
        
        if not token_exists:
            with open(TOKENS_FILE, 'a', encoding='utf-8') as f:
                # Add timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"# Generated at: {timestamp}\n")
                f.write(token_entry)
                f.write("#" * 50 + "\n\n")
            
            clog("success", f"✅ Token saved to {TOKENS_FILE}")
            
            # Show token stats
            show_token_stats()
            return True
        else:
            clog("warning", f"⚠️ Token already exists in {TOKENS_FILE}")
            return False
            
    except Exception as e:
        clog("error", f"❌ Error saving token: {e}")
        return False

def show_token_stats():
    """Show statistics of saved tokens"""
    try:
        if os.path.exists(TOKENS_FILE):
            with open(TOKENS_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                # Count actual token lines (excluding comments)
                token_lines = [line for line in lines if ':' in line and not line.startswith('#')]
                total_tokens = len(token_lines)
                
                if total_tokens > 0:
                    clog("info", f"📊 Total tokens in {TOKENS_FILE}: {total_tokens}")
        else:
            clog("info", f"📁 {TOKENS_FILE} created - First token will be saved here")
            
    except Exception as e:
        clog("error", f"❌ Error reading token stats: {e}")

def is_blocked_domain(email):
    domain = email.split("@")[-1].lower()
    for blocked in BLOCKED_DOMAINS:
        if domain == blocked or domain.endswith("." + blocked):
            return True
    return False

class Kasawa:
    @staticmethod
    def get_email():
        for _ in range(10):
            try:
                domains = ["iusearch.lol", "hacktivc.com"]
                random_user = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
                domain = random.choice(domains)
                email = f"{random_user}@{domain}"
                
                r = session.get(f'https://api.barid.site/emails/{email}', timeout=15)
                r.raise_for_status()
                data = r.json()
                
                if data.get("success") and data.get("result") == []:
                    password = random_password(12)
                    clog("info", f"[Barid] New email: {email}")
                    return {"email": email, "token": email, "password": password}
                else:
                    clog("warn", f"[Barid] Email already exists, retrying...")
                    continue
                    
            except Exception as e:
                clog("error", f"[Barid] Error get_email: {e}")
                time.sleep(2)
        
        # Fallback
        fallback_email = f"fallback{random.randint(100,999)}@example.com"
        clog("warn", f"[Barid] Using fallback email: {fallback_email}")
        return {"email": fallback_email, "token": None, "password": random_password(12)}

    @staticmethod
    def get_inbox_data(email, timeout=180):
        if not email:
            return None
        
        start = time.time()
        attempt = 0
        clog("info", "[Barid] Polling inbox for verification email...")
        
        while time.time() - start < timeout:
            attempt += 1
            time.sleep(1.2)
            
            try:
                r = session.get(f"https://api.barid.site/emails/{email}", timeout=15)
                r.raise_for_status()
                data = r.json()
                
                if not data.get("success"):
                    continue
                
                emails = data.get("result", [])
                if not emails:
                    continue
                
                for email_item in emails:
                    subject = email_item.get("subject", "").lower()
                    if "discord" in subject and ("verify" in subject or "verification" in subject):
                        email_id = email_item.get("id")
                        inbox = session.get(f"https://api.barid.site/inbox/{email_id}", timeout=15)
                        inbox.raise_for_status()
                        inbox_data = inbox.json()
                        
                        if not inbox_data.get("success"):
                            continue
                        
                        content = inbox_data["result"].get("text_content", "") + inbox_data["result"].get("html_content", "")
                        
                        patterns = [
                            r'https://click\.discord\.com/ls/click\?[^\s"<]+',
                            r'https://discord\.com/verify[^\s"<]+',
                            r'https://discord\.com/api/v9/auth/verify[^\s"<]+',
                        ]
                        
                        for p in patterns:
                            links = re.findall(p, content)
                            if links:
                                clog("success", "[Barid] Found verification link!")
                                return links[0]
                                
            except Exception as e:
                clog("error", f"[Barid] Error checking inbox (attempt {attempt}): {e}")
        
        clog("warning", "[Barid] Verification email not found in time")
        return None

async def _handle_request2(request):
    global page, auth_token
    if not rate_limit and "https://discord.com/api/v9/auth/register" in request.url:
        response = await request.response()
        response_body = await response.text() if response else "No response body"
        try:
            response_body_json = json.loads(response_body)
        except json.JSONDecodeError:
            response_body_json = {"raw": response_body}
        if "retry_after" in response_body_json:
            try:
                retry_time = int(response_body_json["retry_after"])
            except Exception:
                retry_time = 5
            for i in range(retry_time, 0, -1):
                clog("info", f"Retrying in {i} seconds...")
                time.sleep(1)
            try:
                await page.locator("button[type='submit']").click()
                await asyncio.sleep(2)
                # Captcha handling removed for now
                await page.wait_for_url("https://discord.com/channels/@me", timeout=10000)
            except Exception as e:
                clog("error", f"[RequestHandler] Error during retry flow: {e}")
        if "token" in response_body_json:
            clog("info", f"Token: {response_body_json['token'][:50]}...")
            auth_token = response_body_json["token"]

async def _handle_response(response):
    if "https://discord.com/api/v9/auth/verify" in response.url:
        if response.status == 200:
            auth_header = response.request.headers.get("authorization")
            if auth_header:
                verify_event.set()

async def detect_phone():
    try:
        await page.wait_for_selector('button:has-text("Verify by Phone")', timeout=3000)
        return True
    except:
        return False

async def detectmail():
    try:
        await page.wait_for_selector('button:has-text("Verify by Email")', timeout=3000)
        return True
    except:
        return False

async def start():
    global page, auth_token

    show_banner()
    
    infomail = Kasawa.get_email()
    username = random_username()
    
    clog("info", f"📧 Email: {infomail['email']}")
    clog("info", f"👤 Username: {username}")
    clog("info", f"🔑 Password: {infomail['password']}")
    print("─" * 50)

    # Import Playwright
    try:
        from playwright.async_api import async_playwright
        playwrights = await async_playwright().start()
        
        # Create browser context
        browser = await playwrights.chromium.launch(headless=False)
        context = await browser.new_context(locale="en-US")
        page = await context.new_page()
        page.on("requestfinished", _handle_request2)

        await page.goto("https://discord.com/register")
        await page.wait_for_url("https://discord.com/register", timeout=30000)

        # Fill form
        await page.locator("input[name='email']").fill(infomail["email"])
        await page.locator("input[name='global_name']").fill(username)
        await page.locator("input[name='username']").fill(username)
        await page.locator("input[name='password']").fill(infomail["password"])
        
        # Select birthday - FIXED: using select_birthday_simple
        await select_birthday_simple(page)

        # Click submit button
        await page.locator("button[type='submit']").click()
        await asyncio.sleep(5)
        
        # Check for registration success
        try:
            await page.wait_for_url("https://discord.com/channels/@me", timeout=30000)
            clog("success", "✅ Registration successful!")
        except:
            clog("warning", "⚠️ Registration may not be complete, checking...")

        # Email verification
        inboxmail = Kasawa.get_inbox_data(infomail.get("email"))
        if inboxmail:
            clog("info", f"📨 Verification email found")
            page2 = await context.new_page()
            page2.on("response", _handle_response)

            try:
                await page2.goto(inboxmail, timeout=60000)
                await asyncio.sleep(3)

                try:
                    await asyncio.wait_for(verify_event.wait(), timeout=30)
                    clog("success", "✅ Email verification successful!")
                except asyncio.TimeoutError:
                    clog("error", "❌ Email verification timeout")

            except Exception as e:
                clog("error", f"❌ Email verification error: {e}")
            finally:
                await page2.close()
                verify_event.clear()
        else:
            clog("error", "❌ No verification email found")

        # Save token
        if auth_token:
            # Try to create server
            try:
                await page.locator("div.defaultColor__4bd52:text('Create My Own')").click(timeout=5000)
                await asyncio.sleep(1)
                await page.locator("a:has-text('Skip this question')").click(timeout=5000)
                await asyncio.sleep(1)
                await page.locator("button:has-text('Create')").click(timeout=5000)
                await asyncio.sleep(1)
            except:
                clog("warning", "⚠️ Could not complete server creation, but token is available")
            
            # Save token to tokens.txt
            saved = save_token(infomail['email'], infomail['password'], auth_token)
            
            if saved:
                print("\n" + "═" * 60)
                clog("success", "🎉 TOKEN SUCCESSFULLY GENERATED!")
                clog("info", f"📁 Saved to: {TOKENS_FILE}")
                clog("info", f"📝 Format: email:password:token")
                clog("info", f"📧 Email: {infomail['email']}")
                clog("info", f"🔑 Token: {auth_token[:50]}...")
                print("═" * 60 + "\n")
            else:
                clog("warning", "⚠️ Token not saved (already exists or error)")
                
        else:
            clog("error", "❌ No token generated!")
        
        # Success message
        print("\n" + "═" * 60)
        if auth_token:
            clog("success", f"✅ Token generation complete!")
        else:
            clog("warning", f"⚠️ Token generation failed!")
        print("═" * 60)
        
        await asyncio.sleep(5)
        await browser.close()
        
    except ImportError as e:
        clog("error", f"❌ Playwright not installed: {e}")
        clog("info", "Please install: pip install playwright")
        return
    except Exception as e:
        clog("error", f"❌ Error in start function: {e}")

if __name__ == "__main__":
    show_banner()
    clog("info", f"📂 Current directory: {os.getcwd()}")
    clog("info", f"📄 Token file: {os.path.join(os.getcwd(), TOKENS_FILE)}")
    
    while True:
        try:
            asyncio.run(start())
        except KeyboardInterrupt:
            clog("warning", "👋 Process interrupted by user")
            break
        except Exception as e:
            clog("error", f"❌ Main error: {e}")
            clog("info", "🔄 Restarting in 45 seconds...")
        time.sleep(45)