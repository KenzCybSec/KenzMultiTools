def count_accounts(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            accounts = data.split("==============================")
            accounts = [account.strip() for account in accounts if account.strip()]
            return len(accounts)
    except FileNotFoundError:
        print("Die Datei wurde nicht gefunden.")
        return 0

filename = "password.txt"
num_accounts = count_accounts(filename)
print("Info: It will probably display a bit more accounts than you actually generated, idk why")
print("Number of Accounts:", num_accounts);input("")