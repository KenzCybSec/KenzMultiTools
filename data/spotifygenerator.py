import json
import os
import ctypes
import subprocess
from urllib.request import urlopen
ctypes.windll.kernel32.SetConsoleTitleW("Kenz Spotify Account Generator")
try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    import pycountry
except ImportError:
        os.system("pip install selenium")
        os.system("pip install pycountry")
        os.system("cls" if os.name=="nt" else "clear")
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.by import By
        import pycountry
except Exception as e:
    print("An error this early should only happen when python or pip isnt correctly configured!")
    input(f"An Error Occured: {e}")
import random
import string
import time

# ================ RENK KODLARI (MOR TONLARI) ================
PURPLE = "\033[95m"
PURPLE_BRIGHT = "\033[35m"
PURPLE_DARK = "\033[35m"
MAGENTA = "\033[35m"
VIOLET = "\033[38;5;99m"
LAVENDER = "\033[38;5;183m"
PINK = "\033[38;5;213m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)
country_name = data['country']
country_code = pycountry.countries.lookup(country_name).alpha_2
print(f"{PURPLE_BRIGHT}[🌍] Using Country Code: {country_code}{RESET}")
country_code = country_code.lower()

def count_accounts(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            accounts = data.split("==============================")
            accounts = [account.strip() for account in accounts if account.strip()]
            return len(accounts)
    except FileNotFoundError:
        print(f"{RED}[!] File not found.{RESET}")
        return 0

def generate_random_string():
    length = random.randint(10, 15)
    numbers = ''.join(random.choices(string.digits, k=2))
    chars = ''.join(random.choices(string.ascii_letters + string.punctuation, k=length - 3))
    final_string = '$' + numbers + chars
    
    return final_string

def generate_birthdate():
    day = random.randint(1, 25)
    month = random.randint(1, 12)
    year = random.randint(1980, 2000)
    return day, month, year

def generate_usernames(n):
    usernames = []
    for i in range(n):
        # "kenz" ile başlayıp random sayılar ekle
        random_num = random.randint(1000, 9999999)
        username = f"kenz{random_num}"
        usernames.append(username)
    return usernames

def get_random_username(usernames):
    username = random.choice(usernames)
    usernames.remove(username)
    return username

def log_account_info(username, display_name, password, day, month, year, gender):
    with open("password.txt", mode="a") as f:
        f.write(f"Username: {username}@gmail.com\n")
        f.write(f"Display Name: {display_name}\n")
        f.write(f"Password: {password}\n")
        f.write(f"Birthdate: {day}/{month}/{year}\n")
        f.write(f"Gender: {gender}\n")
        f.write("="*30 + "\n")

os.system("title Made by Kenz")
os.system("cls" if os.name == "nt" else "clear")
print(f"{VIOLET}")
print("""
  ██████  ██▓███   ▒█████  ▄▄▄█████▓ ██▓  █████▒▓██   ██▓  ▄████ ▓█████  ███▄    █ 
▒██    ▒ ▓██░  ██▒▒██▒  ██▒▓  ██▒ ▓▒▓██▒▓██   ▒  ▒██  ██▒ ██▒ ▀█▒▓█   ▀  ██ ▀█   █ 
░ ▓██▄   ▓██░ ██▓▒▒██░  ██▒▒ ▓██░ ▒░▒██▒▒████ ░   ▒██ ██░▒██░▄▄▄░▒███   ▓██  ▀█ ██▒
  ▒   ██▒▒██▄█▓▒ ▒▒██   ██░░ ▓██▓ ░ ░██░░▓█▒  ░   ░ ▐██▓░░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒
▒██████▒▒▒██▒ ░  ░░ ████▓▒░  ▒██▒ ░ ░██░░▒█░      ░ ██▒▓░░▒▓███▀▒░▒████▒▒██░   ▓██░
▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▒░▒░   ▒ ░░   ░▓   ▒ ░       ██▒▒▒  ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒ 
░ ░▒  ░ ░░▒ ░       ░ ▒ ▒░     ░     ▒ ░ ░       ▓██ ░▒░   ░   ░  ░ ░  ░░ ░░   ░ ▒░
░  ░  ░  ░░       ░ ░ ░ ▒    ░       ▒ ░ ░ ░     ▒ ▒ ░░  ░ ░   ░    ░      ░   ░ ░ 
      ░               ░ ░            ░           ░ ░           ░    ░  ░         ░ 
                                                 ░ ░                              
""")
print(f"{RESET}")
print(f"{PURPLE}╔══════════════════════════════════════════════════════════════════════╗{RESET}")
print(f"{PURPLE}║                     KENZ SPOTIFY GENERATOR                          ║{RESET}")
print(f"{PURPLE}╚══════════════════════════════════════════════════════════════════════╝{RESET}")

print(f"\n{LAVENDER}Enter the number of accounts to create:{RESET}")
print(f"{PINK}[>] {RESET}", end="")
num_accounts = int(input())

print(f"\n{LAVENDER}Which Mode do you want to use?{RESET}")
print(f"{MAGENTA}  1 : Manuel | 2 : Automatic{RESET}")
print(f"{PINK}[>] {RESET}", end="")
mode = input()

modee = False
if int(mode) == 2:
    modee = True
    print(f"{MAGENTA}[ℹ] Manual mode selected{RESET}")
else:
    print(f"{MAGENTA}[ℹ] Automatic mode selected{RESET}")

user_list = generate_usernames(num_accounts + 20)

random_names = ["JohnD", "Alice", "Bob", "Eve", "Charlie", "Josef", "Kenz", "Franz", "Sepp",
                "Anos", "Vandear", "Bob Goldham", "KingPin", "EboySkills", "Waderpond", "FrenchDude", 
                "AustrianCrus4der", "ProGamer", "Sigi", "KingEM", "Cepheus", "Cicily", "Chismaa", "arefin", "RafEra"]

random_names += ["Zephyr", "Seraphina", "Kai", "Lilith", "Phoenix", "Cassandra", "Dexter", "Jasmine", 
                 "Nico", "Violet", "Atlas", "Scarlett", "Apollo", "Persephone", "Orion", "Nova", 
                 "Dante", "Celeste", "Cairo", "Luna", "Leia", "Zane", "Lyra", "Titus", "Athena", 
                 "Knox", "Aurora", "Roman", "Selene", "Cyrus", "Delilahaaa", "Evander", "Freya", 
                 "Ajax", "Cleo", "Cassius", "Rosalind", "Cyril", "Thalia", "Odysseus", "Ariadne", 
                 "Lincoln", "Juniper", "Caius", "Nova", "Lysander", "Maeve", "Aurelius", "Daphne", "RuskyDev"]
accnum = 0
random_names += ["Ruskyyyy", "Joooodatev"]
signup_url = f"https://www.spotify.com/{country_code}/signup"
driver = webdriver.Chrome()
random_names += ["Aurelia", "Balthazar", "Cassiopeia", "Dashiell", "Eulalia", "Finnian", "Gwyneira",
                "Hermione", "Ignatius", "Jocasta", "Kaius", "Lysander", "Matilda", "Nehemiah",
                "Octavia", "Persephone", "Quintus", "Rosamund", "Seraphina", "Thaddeus", "Ulysses",
                "Valentina", "Wilhelmina", "Xanthe", "Yseult", "Zephyrine"]
random_names = list(set(random_names))
accept_cookies = country_code != "CH" and country_code != "US" and country_code != "CA" and country_code != "AU" and country_code != "JP"

for _ in range(num_accounts):
    random_username = get_random_username(user_list)
    random_display_name = random.choice(random_names)
    day, month, year = generate_birthdate()
    os.system("cls")
    print(f"{CYAN}[📧] Used mail: {random_username}@gmail.com{RESET}")
    print(f"{CYAN}[👤] Used display name: {random_display_name}{RESET}")
    print(f"{CYAN}[🎂] Used birthdate: {day} / {month} / {year}{RESET}")
    print(f"{VIOLET}{'─'*50}{RESET}")

    driver.get(signup_url)
    time.sleep(0.2)
    email_input = driver.find_element(By.ID, "username")
    email_input.send_keys(f"{random_username}@gmail.com")

    time.sleep(0.5)
    if accept_cookies:
        try:
            accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_cookies_button.click()
        except Exception:
            time.sleep(0.5) # incase browser is slow
            try:
                accept_cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                accept_cookies_button.click()
            except Exception:
                print(f"{YELLOW}[ℹ] No cookies button to click{RESET}")
    time.sleep(0.55)
    next_button = driver.find_element(By.XPATH, "//button[@data-testid='submit']")
    next_button.click()

    time.sleep(0.55)
    password_input = driver.find_element(By.ID, "new-password")
    random_string = generate_random_string()
    password_input.send_keys(random_string)
    print(f"{GREEN}[🔑] Used Password: {random_string}{RESET}")

    time.sleep(0.55)
    next_button = driver.find_element(By.XPATH, "//button[@data-testid='submit']")
    next_button.click()

    time.sleep(0.55)
    display_name_input = driver.find_element(By.ID, "displayName")
    display_name_input.send_keys(random_display_name)

    time.sleep(0.12)
    day_input = driver.find_element(By.ID, "day")
    day_input.send_keys(day)

    time.sleep(0.10)
    month_select = driver.find_element(By.ID, "month")
    month_select.send_keys(Keys.ARROW_DOWN)  # Open the dropdown
    month_select.send_keys(Keys.ARROW_DOWN)  # Move down to select a random month
    month_select.send_keys(Keys.ENTER)  # Confirm selection

    time.sleep(0.13)
    year_input = driver.find_element(By.ID, "year")
    year_input.send_keys(year)

    time.sleep(0.14)
    gender_option_male = driver.find_element(By.XPATH, "//label[@for='gender_option_male']")
    gender_option_male.click()
    print(f"{GREEN}[🚹] Used Gender: Male{RESET}")
    time.sleep(0.40)
    next_button = driver.find_element(By.XPATH, "//button[@data-testid='submit']")
    next_button.click()

    time.sleep(0.30)
    sign_up_button = driver.find_element(By.XPATH, "//button[@data-testid='submit']")
    sign_up_button.click()
    
    log_account_info(random_username, random_display_name, random_string, day, month, year, "Male")
    accnum += 1
    left_accounts = num_accounts - accnum
    print(f"{GREEN}[✅] Done with account nr. {accnum}{RESET}")
    if left_accounts == 0:
        print(f"{GREEN}[🎉] Made {accnum} accounts | Accounts left: {left_accounts}{RESET}")
        input(f"{PINK}[⏸️] Finished with all accounts! Press Enter...{RESET}")
    elif accnum == 1:
        print(f"{GREEN}[📊] Made {accnum} account | Accounts left: {left_accounts}{RESET}")
    else:
        print(f"{GREEN}[📊] Made {accnum} accounts | Accounts left: {left_accounts}{RESET}")
    if accnum != num_accounts:
        if modee == True:
            input(f"{PINK}[⏸️] Waiting for an enter{RESET}")
        elif modee == False:
            time.sleep(2.5)  # wait before next acc
        driver.delete_all_cookies()
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        driver.execute_script("window.location.reload();")
        if num_accounts > 1:
            driver.execute_script(f"window.open('{signup_url}');")
            driver.switch_to.window(driver.window_handles[1])
            driver.switch_to.window(driver.window_handles[0])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

driver.quit()

filename = "password.txt"
num_accounts = count_accounts(filename)
print(f"\n{VIOLET}{'═'*50}{RESET}")
print(f"{PURPLE_BRIGHT}[📊] Current amount of accounts in {filename}{RESET}")
print(f"{PURPLE_BRIGHT}[✅] Number of Accounts: {num_accounts}{RESET}")
print(f"{VIOLET}{'═'*50}{RESET}")
input(f"{PINK}[⏹️] Press Enter to exit...{RESET}")