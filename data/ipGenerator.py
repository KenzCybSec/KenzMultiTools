import random
import socket
import struct
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import json
import time
from datetime import datetime
import sys
import os
from colorama import Fore, Style, init

# Initialize colors
init(autoreset=True)

class IPGeneratorPro:
    def __init__(self):
        self.VERSION = "3.0"
        self.AUTHOR = "Lightmanta"
        self.THEME = {
            "primary": Fore.MAGENTA,
            "secondary": Fore.LIGHTCYAN_EX,
            "success": Fore.LIGHTGREEN_EX,
            "error": Fore.LIGHTRED_EX,
            "warning": Fore.LIGHTYELLOW_EX,
            "info": Fore.LIGHTCYAN_EX,
            "title": Fore.LIGHTMAGENTA_EX
        }
        
    def print_header(self):
        """Display application header"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.THEME['title']}╔{'═'*70}╗")
        print(f"{self.THEME['title']}║{' '*70}║")
        print(f"{self.THEME['title']}║{'IP GENERATOR PRO - v3.0'.center(70)}║")
        print(f"{self.THEME['title']}║{'Created by Lightmanta'.center(70)}║")
        print(f"{self.THEME['title']}║{'Violet Theme | Professional Edition'.center(70)}║")
        print(f"{self.THEME['title']}║{' '*70}║")
        print(f"{self.THEME['title']}╚{'═'*70}╝\n")
    
    def generate_random_ip(self, public_only=True):
        """Generate random valid IP address"""
        while True:
            ip_int = random.randint(1, 0xffffffff)
            ip = socket.inet_ntoa(struct.pack('>I', ip_int))
            if not public_only or (public_only and not ipaddress.ip_address(ip).is_private):
                return ip
    
    def generate_ip_range(self, start_ip, end_ip):
        """Generate IP range between two addresses"""
        try:
            start = struct.unpack('>I', socket.inet_aton(start_ip))[0]
            end = struct.unpack('>I', socket.inet_aton(end_ip))[0]
            
            if start > end:
                start, end = end, start
                
            ips = []
            for ip_int in range(start, end + 1):
                ips.append(socket.inet_ntoa(struct.pack('>I', ip_int)))
            return ips
        except socket.error:
            print(f"{self.THEME['error']}[!] Invalid IP address format")
            return []
    
    def generate_country_based(self, country_code, count=100):
        """Generate IPs based on country"""
        country_networks = {
            'US': ['8.0.0.0/8', '12.0.0.0/24', '24.0.0.0/12', '32.0.0.0/11'],
            'UK': ['5.62.56.0/24', '25.0.0.0/8', '31.0.0.0/16', '46.0.0.0/15'],
            'DE': ['5.0.0.0/16', '31.0.0.0/8', '46.0.0.0/15', '78.0.0.0/12'],
            'TR': ['78.160.0.0/11', '88.240.0.0/12', '95.0.0.0/12', '212.175.0.0/16'],
            'RU': ['5.0.0.0/16', '31.0.0.0/8', '46.0.0.0/15', '77.0.0.0/12'],
            'CN': ['1.0.0.0/24', '14.0.0.0/8', '27.0.0.0/13', '36.0.0.0/11'],
            'JP': ['1.0.0.0/8', '14.0.0.0/8', '27.0.0.0/13', '36.0.0.0/11'],
            'FR': ['5.0.0.0/8', '37.0.0.0/8', '78.0.0.0/9', '91.0.0.0/10'],
            'BR': ['177.0.0.0/8', '179.0.0.0/8', '186.0.0.0/8', '189.0.0.0/8'],
            'IN': ['1.0.0.0/8', '14.0.0.0/8', '27.0.0.0/13', '36.0.0.0/11']
        }
        
        ips = []
        if country_code in country_networks:
            networks = country_networks[country_code]
            for _ in range(count):
                network = random.choice(networks)
                net = ipaddress.ip_network(network)
                ip_int = random.randint(int(net.network_address), int(net.broadcast_address))
                ips.append(str(ipaddress.ip_address(ip_int)))
        
        return ips
    
    def generate_cidr_range(self, cidr, count=None):
        """Generate IPs from CIDR notation"""
        try:
            net = ipaddress.ip_network(cidr, strict=False)
            ips = [str(ip) for ip in net.hosts()]
            if count:
                return random.sample(ips, min(count, len(ips)))
            return ips
        except ValueError as e:
            print(f"{self.THEME['error']}[!] Invalid CIDR: {e}")
            return []
    
    def generate_multithread(self, count=10000, threads=100):
        """High-speed multithreaded IP generation"""
        print(f"{self.THEME['info']}[*] Generating {count:,} IPs using {threads} threads...")
        
        ips = []
        start_time = time.time()
        
        def generate_batch(batch_size):
            batch = []
            for _ in range(batch_size):
                batch.append(self.generate_random_ip())
            return batch
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            batch_size = count // threads
            futures = []
            
            for i in range(threads):
                if i == threads - 1:  # Last thread gets remainder
                    batch_size = count - (batch_size * (threads - 1))
                futures.append(executor.submit(generate_batch, batch_size))
            
            for future in as_completed(futures):
                ips.extend(future.result())
        
        elapsed = time.time() - start_time
        print(f"{self.THEME['success']}[✓] Generated {len(ips):,} IPs in {elapsed:.2f}s ({len(ips)/elapsed:.0f} IPs/sec)")
        return ips[:count]
    
    def analyze_ips(self, ips):
        """Analyze generated IPs"""
        analysis = {
            'total': len(ips),
            'unique': len(set(ips)),
            'class_a': 0,
            'class_b': 0,
            'class_c': 0,
            'private': 0,
            'reserved': 0
        }
        
        for ip_str in ips:
            try:
                ip = ipaddress.ip_address(ip_str)
                
                if ip.is_private:
                    analysis['private'] += 1
                elif ip.is_reserved:
                    analysis['reserved'] += 1
                else:
                    first_octet = int(ip_str.split('.')[0])
                    if 1 <= first_octet <= 126:
                        analysis['class_a'] += 1
                    elif 128 <= first_octet <= 191:
                        analysis['class_b'] += 1
                    elif 192 <= first_octet <= 223:
                        analysis['class_c'] += 1
            except:
                continue
        
        return analysis
    
    def save_ips(self, ips, filename=None):
        """Save IPs to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_ips_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for ip in ips:
                    f.write(ip + '\n')
            
            size_kb = os.path.getsize(filename) / 1024
            print(f"{self.THEME['success']}[✓] Saved {len(ips):,} IPs to '{filename}' ({size_kb:.1f} KB)")
            return filename
        except Exception as e:
            print(f"{self.THEME['error']}[!] Error saving file: {e}")
            return None
    
    def export_formats(self, ips):
        """Export in different formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON format
        json_file = f"ips_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'total_count': len(ips),
                'ips': list(set(ips))  # Remove duplicates
            }, f, indent=2)
        
        # CSV format
        csv_file = f"ips_{timestamp}.csv"
        with open(csv_file, 'w') as f:
            f.write("IP Address,First Octet,Class,Is Private\n")
            for ip in ips:
                try:
                    ip_obj = ipaddress.ip_address(ip)
                    first_octet = ip.split('.')[0]
                    ip_class = 'A' if 1 <= int(first_octet) <= 126 else \
                              'B' if 128 <= int(first_octet) <= 191 else \
                              'C' if 192 <= int(first_octet) <= 223 else 'Other'
                    is_private = 'Yes' if ip_obj.is_private else 'No'
                    f.write(f"{ip},{first_octet},{ip_class},{is_private}\n")
                except:
                    f.write(f"{ip},,,Unknown\n")
        
        print(f"{self.THEME['success']}[✓] Exported to {json_file} and {csv_file}")
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n{self.THEME['primary']}┌{'─'*68}┐")
        print(f"{self.THEME['primary']}│{'MAIN MENU'.center(68)}│")
        print(f"{self.THEME['primary']}└{'─'*68}┘")
        
        options = [
            "1. Random IP Generation",
            "2. IP Range Generation",
            "3. Country-Based IPs",
            "4. CIDR Network IPs",
            "5. High-Speed Bulk Generation",
            "6. Advanced Options",
            "7. Exit"
        ]
        
        for option in options:
            print(f"{self.THEME['info']}  {option}")
    
    def run(self):
        """Main execution"""
        self.print_header()
        
        while True:
            self.display_menu()
            choice = input(f"\n{self.THEME['primary']}[?] Select option (1-7): ").strip()
            
            if choice == '1':
                # Random IP Generation
                try:
                    count = int(input(f"{self.THEME['secondary']}[?] Number of IPs to generate: "))
                    public_only = input(f"{self.THEME['secondary']}[?] Public IPs only? (y/n): ").lower() == 'y'
                    
                    ips = []
                    for i in range(count):
                        ips.append(self.generate_random_ip(public_only))
                        if (i + 1) % 1000 == 0:
                            print(f"{self.THEME['info']}[*] Generated {i + 1:,} IPs...")
                    
                    analysis = self.analyze_ips(ips)
                    print(f"\n{self.THEME['success']}[✓] Generated {count:,} IPs")
                    print(f"{self.THEME['info']}   Class A: {analysis['class_a']:,}")
                    print(f"{self.THEME['info']}   Class B: {analysis['class_b']:,}")
                    print(f"{self.THEME['info']}   Class C: {analysis['class_c']:,}")
                    
                except ValueError:
                    print(f"{self.THEME['error']}[!] Invalid number")
                    continue
                    
            elif choice == '2':
                # IP Range
                start_ip = input(f"{self.THEME['secondary']}[?] Start IP: ")
                end_ip = input(f"{self.THEME['secondary']}[?] End IP: ")
                
                ips = self.generate_ip_range(start_ip, end_ip)
                if ips:
                    print(f"{self.THEME['success']}[✓] Generated {len(ips):,} IPs in range")
                    
            elif choice == '3':
                # Country Based
                print(f"\n{self.THEME['info']}Available countries: US, UK, DE, TR, RU, CN, JP, FR, BR, IN")
                country = input(f"{self.THEME['secondary']}[?] Country code: ").upper()
                count = int(input(f"{self.THEME['secondary']}[?] Number of IPs: "))
                
                ips = self.generate_country_based(country, count)
                if ips:
                    print(f"{self.THEME['success']}[✓] Generated {len(ips):,} IPs for {country}")
                    
            elif choice == '4':
                # CIDR
                cidr = input(f"{self.THEME['secondary']}[?] CIDR notation (e.g., 192.168.1.0/24): ")
                count_input = input(f"{self.THEME['secondary']}[?] Max IPs to generate (Enter for all): ")
                count = int(count_input) if count_input else None
                
                ips = self.generate_cidr_range(cidr, count)
                if ips:
                    print(f"{self.THEME['success']}[✓] Generated {len(ips):,} IPs from {cidr}")
                    
            elif choice == '5':
                # Bulk Generation
                try:
                    count = int(input(f"{self.THEME['secondary']}[?] Number of IPs (10,000-1,000,000): "))
                    count = max(10000, min(count, 1000000))
                    
                    ips = self.generate_multithread(count)
                    
                except ValueError:
                    print(f"{self.THEME['error']}[!] Invalid number")
                    continue
                    
            elif choice == '6':
                # Advanced Options
                print(f"\n{self.THEME['info']}Advanced options coming soon...")
                continue
                
            elif choice == '7':
                # Exit
                print(f"\n{self.THEME['warning']}[!] Exiting...")
                sys.exit(0)
                
            else:
                print(f"{self.THEME['error']}[!] Invalid option")
                continue
            
            # Post-generation options
            if 'ips' in locals() and ips:
                print(f"\n{self.THEME['primary']}┌{'─'*68}┐")
                print(f"{self.THEME['primary']}│{'POST-GENERATION OPTIONS'.center(68)}│")
                print(f"{self.THEME['primary']}└{'─'*68}┘")
                
                post_options = [
                    "1. Save to text file",
                    "2. Export to JSON & CSV",
                    "3. Analyze IP statistics",
                    "4. Generate more IPs",
                    "5. Return to main menu"
                ]
                
                for option in post_options:
                    print(f"{self.THEME['info']}  {option}")
                
                post_choice = input(f"\n{self.THEME['primary']}[?] Select option (1-5): ")
                
                if post_choice == '1':
                    filename = input(f"{self.THEME['secondary']}[?] Filename (Enter for auto): ")
                    self.save_ips(ips, filename if filename else None)
                    
                elif post_choice == '2':
                    self.export_formats(ips)
                    
                elif post_choice == '3':
                    analysis = self.analyze_ips(ips)
                    print(f"\n{self.THEME['info']}IP Analysis:")
                    print(f"{self.THEME['secondary']}  Total IPs: {analysis['total']:,}")
                    print(f"{self.THEME['secondary']}  Unique IPs: {analysis['unique']:,}")
                    print(f"{self.THEME['secondary']}  Class A: {analysis['class_a']:,}")
                    print(f"{self.THEME['secondary']}  Class B: {analysis['class_b']:,}")
                    print(f"{self.THEME['secondary']}  Class C: {analysis['class_c']:,}")
                    print(f"{self.THEME['secondary']}  Private: {analysis['private']:,}")
                    print(f"{self.THEME['secondary']}  Reserved: {analysis['reserved']:,}")
                    
                elif post_choice == '4':
                    continue
                
                input(f"\n{self.THEME['info']}[*] Press Enter to continue...")

# Main execution
if __name__ == "__main__":
    try:
        generator = IPGeneratorPro()
        generator.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error: {e}")
        sys.exit(1)