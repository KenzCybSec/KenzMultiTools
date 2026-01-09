import requests
import socket
import json
import time
import concurrent.futures
from datetime import datetime
import sys
import os
import csv
from colorama import Fore, Style, init

# Initialize colors
init(autoreset=True)

class IPCheckerPro:
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
        self.results = []
        self.stats = {
            'total': 0,
            'online': 0,
            'offline': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
        
    def print_header(self):
        """Display application header"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{self.THEME['title']}╔{'═'*70}╗")
        print(f"{self.THEME['title']}║{' '*70}║")
        print(f"{self.THEME['title']}║{'IP CHECKER'.center(70)}║")
        print(f"{self.THEME['title']}║{'Created by Kenz'.center(70)}║")
        print(f"{self.THEME['title']}║{' '*70}║")
        print(f"{self.THEME['title']}╚{'═'*70}╝\n")
    
    def check_port(self, ip, port, timeout=1):
        """Check if port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def get_geo_info(self, ip):
        """Get geographical information for IP"""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    def get_service_name(self, port):
        """Get service name for port"""
        services = {
            20: "FTP Data", 21: "FTP Control", 22: "SSH", 23: "Telnet",
            25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 465: "SMTPS", 587: "SMTP Submission",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 3389: "RDP",
            5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP Proxy",
            8443: "HTTPS Alt", 27017: "MongoDB", 6379: "Redis"
        }
        return services.get(port, f"Port {port}")
    
    def check_single_ip(self, ip):
        """Check a single IP address"""
        result = {
            'ip': ip,
            'status': 'Unknown',
            'country': 'Unknown',
            'country_code': 'XX',
            'city': 'Unknown',
            'isp': 'Unknown',
            'org': 'Unknown',
            'lat': 0,
            'lon': 0,
            'open_ports': [],
            'services': [],
            'response_time': None,
            'checked_at': datetime.now().isoformat(),
            'error': None
        }
        
        start_time = time.time()
        
        try:
            # Get geo information
            geo_info = self.get_geo_info(ip)
            if geo_info and geo_info.get('status') == 'success':
                result.update({
                    'country': geo_info.get('country', 'Unknown'),
                    'country_code': geo_info.get('countryCode', 'XX'),
                    'city': geo_info.get('city', 'Unknown'),
                    'isp': geo_info.get('isp', 'Unknown'),
                    'org': geo_info.get('org', 'Unknown'),
                    'lat': geo_info.get('lat', 0),
                    'lon': geo_info.get('lon', 0),
                    'status': 'Online'
                })
            else:
                result['status'] = 'Offline'
            
            # Check common ports
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 
                          587, 993, 995, 3306, 3389, 8080, 8443]
            
            for port in common_ports[:8]:  # Check first 8 ports for speed
                if self.check_port(ip, port, timeout=0.5):
                    result['open_ports'].append(port)
                    result['services'].append(self.get_service_name(port))
            
            result['response_time'] = round((time.time() - start_time) * 1000, 2)
            
        except Exception as e:
            result['status'] = 'Error'
            result['error'] = str(e)
        
        return result
    
    def load_ip_list(self, source):
        """Load IP list from various sources"""
        ips = []
        
        if os.path.isfile(source):
            # Load from file
            try:
                with open(source, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Handle CIDR notation
                            if '/' in line:
                                try:
                                    import ipaddress
                                    network = ipaddress.ip_network(line, strict=False)
                                    for ip in network.hosts():
                                        ips.append(str(ip))
                                except:
                                    ips.append(line)
                            else:
                                ips.append(line)
            except Exception as e:
                print(f"{self.THEME['error']}[!] Error reading file: {e}")
                return []
        else:
            # Treat as comma-separated list
            ips = [ip.strip() for ip in source.split(',') if ip.strip()]
        
        return list(set(ips))  # Remove duplicates
    
    def check_batch(self, ips, max_workers=50):
        """Check batch of IPs using multithreading"""
        self.stats['start_time'] = time.time()
        self.stats['total'] = len(ips)
        
        print(f"{self.THEME['info']}[*] Checking {len(ips):,} IP addresses...")
        print(f"{self.THEME['info']}[*] Using {max_workers} concurrent workers\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_ip = {executor.submit(self.check_single_ip, ip): ip for ip in ips}
            
            for i, future in enumerate(concurrent.futures.as_completed(future_to_ip), 1):
                ip = future_to_ip[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    
                    # Update statistics
                    if result['status'] == 'Online':
                        self.stats['online'] += 1
                        status_color = self.THEME['success']
                    elif result['status'] == 'Offline':
                        self.stats['offline'] += 1
                        status_color = self.THEME['error']
                    else:
                        self.stats['errors'] += 1
                        status_color = self.THEME['warning']
                    
                    # Display progress
                    if i % 50 == 0 or i == len(ips):
                        progress = (i / len(ips)) * 100
                        print(f"{status_color}[{i}/{len(ips)}] {ip} - {result['country']} ({result['status']}) - {progress:.1f}%")
                    
                except Exception as e:
                    print(f"{self.THEME['error']}[!] Error checking {ip}: {e}")
        
        self.stats['end_time'] = time.time()
        self.stats['duration'] = self.stats['end_time'] - self.stats['start_time']
    
    def display_summary(self):
        """Display checking summary"""
        print(f"\n{self.THEME['title']}┌{'─'*68}┐")
        print(f"{self.THEME['title']}│{'CHECKING SUMMARY'.center(68)}│")
        print(f"{self.THEME['title']}└{'─'*68}┘")
        
        duration = self.stats['duration']
        ips_per_second = self.stats['total'] / duration if duration > 0 else 0
        
        print(f"{self.THEME['info']}  Total IPs checked: {self.stats['total']:,}")
        print(f"{self.THEME['success']}  Online: {self.stats['online']:,} ({self.stats['online']/self.stats['total']*100:.1f}%)")
        print(f"{self.THEME['error']}  Offline: {self.stats['offline']:,} ({self.stats['offline']/self.stats['total']*100:.1f}%)")
        print(f"{self.THEME['warning']}  Errors: {self.stats['errors']:,} ({self.stats['errors']/self.stats['total']*100:.1f}%)")
        print(f"{self.THEME['info']}  Duration: {duration:.2f} seconds")
        print(f"{self.THEME['info']}  Speed: {ips_per_second:.1f} IPs/second")
    
    def display_country_stats(self):
        """Display country statistics"""
        country_stats = {}
        for result in self.results:
            if result['status'] == 'Online':
                country = result['country']
                country_stats[country] = country_stats.get(country, 0) + 1
        
        if country_stats:
            print(f"\n{self.THEME['info']}Top countries by online IPs:")
            sorted_countries = sorted(country_stats.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for country, count in sorted_countries:
                percentage = (count / self.stats['online']) * 100
                print(f"{self.THEME['secondary']}  {country}: {count:,} ({percentage:.1f}%)")
    
    def display_port_stats(self):
        """Display port statistics"""
        port_stats = {}
        for result in self.results:
            for port in result.get('open_ports', []):
                port_stats[port] = port_stats.get(port, 0) + 1
        
        if port_stats:
            print(f"\n{self.THEME['info']}Most common open ports:")
            sorted_ports = sorted(port_stats.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for port, count in sorted_ports:
                service = self.get_service_name(port)
                print(f"{self.THEME['secondary']}  Port {port} ({service}): {count:,}")
    
    def save_results(self, format='all'):
        """Save results to file(s)"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format in ['json', 'all']:
            json_file = f"ip_check_results_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'metadata': {
                        'generated_at': datetime.now().isoformat(),
                        'total_ips': self.stats['total'],
                        'online_ips': self.stats['online'],
                        'duration_seconds': self.stats['duration']
                    },
                    'results': self.results
                }, f, indent=2, ensure_ascii=False)
            print(f"{self.THEME['success']}[✓] JSON results saved to {json_file}")
        
        if format in ['csv', 'all']:
            csv_file = f"ip_check_results_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['IP Address', 'Status', 'Country', 'City', 'ISP', 
                                'Organization', 'Open Ports', 'Services', 
                                'Response Time (ms)', 'Checked At'])
                
                for result in self.results:
                    open_ports = ','.join(map(str, result.get('open_ports', [])))
                    services = ','.join(result.get('services', []))
                    writer.writerow([
                        result['ip'],
                        result['status'],
                        result['country'],
                        result['city'],
                        result['isp'],
                        result['org'],
                        open_ports,
                        services,
                        result.get('response_time', ''),
                        result['checked_at']
                    ])
            print(f"{self.THEME['success']}[✓] CSV results saved to {csv_file}")
        
        if format in ['txt', 'all']:
            txt_file = f"online_ips_{timestamp}.txt"
            with open(txt_file, 'w', encoding='utf-8') as f:
                for result in self.results:
                    if result['status'] == 'Online':
                        f.write(f"{result['ip']}\n")
            print(f"{self.THEME['success']}[✓] Online IPs list saved to {txt_file}")
    
    def display_menu(self):
        """Display main menu"""
        print(f"\n{self.THEME['primary']}┌{'─'*68}┐")
        print(f"{self.THEME['primary']}│{'MAIN MENU'.center(68)}│")
        print(f"{self.THEME['primary']}└{'─'*68}┘")
        
        options = [
            "1. Check Single IP",
            "2. Check IP List from File",
            "3. Check Multiple IPs (Manual Input)",
            "4. Check CIDR Range",
            "5. Load Previous Results",
            "6. Export Settings",
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
                # Single IP check
                ip = input(f"{self.THEME['secondary']}[?] Enter IP address: ").strip()
                if ip:
                    result = self.check_single_ip(ip)
                    print(f"\n{self.THEME['info']}Results for {ip}:")
                    print(f"{self.THEME['secondary']}  Status: {result['status']}")
                    print(f"{self.THEME['secondary']}  Country: {result['country']}")
                    print(f"{self.THEME['secondary']}  City: {result['city']}")
                    print(f"{self.THEME['secondary']}  ISP: {result['isp']}")
                    if result['open_ports']:
                        print(f"{self.THEME['secondary']}  Open Ports: {', '.join(map(str, result['open_ports']))}")
                    print(f"{self.THEME['secondary']}  Response Time: {result.get('response_time', 'N/A')}ms")
            
            elif choice == '2':
                # File input
                filename = input(f"{self.THEME['secondary']}[?] Enter filename with IP list: ").strip()
                if os.path.exists(filename):
                    threads = input(f"{self.THEME['secondary']}[?] Concurrent threads (default 50): ").strip()
                    threads = int(threads) if threads.isdigit() else 50
                    
                    ips = self.load_ip_list(filename)
                    if ips:
                        self.check_batch(ips, threads)
                        self.display_summary()
                        
                        # Show detailed stats
                        detail = input(f"{self.THEME['secondary']}[?] Show detailed statistics? (y/n): ").lower()
                        if detail == 'y':
                            self.display_country_stats()
                            self.display_port_stats()
                        
                        # Save results
                        save = input(f"{self.THEME['secondary']}[?] Save results? (y/n): ").lower()
                        if save == 'y':
                            self.save_results()
                else:
                    print(f"{self.THEME['error']}[!] File not found: {filename}")
            
            elif choice == '3':
                # Manual input
                print(f"{self.THEME['info']}[*] Enter IP addresses (one per line, empty line to finish):")
                ips = []
                while True:
                    ip = input().strip()
                    if not ip:
                        break
                    ips.append(ip)
                
                if ips:
                    threads = input(f"{self.THEME['secondary']}[?] Concurrent threads (default 30): ").strip()
                    threads = int(threads) if threads.isdigit() else 30
                    
                    self.check_batch(ips, threads)
                    self.display_summary()
            
            elif choice == '4':
                # CIDR range
                cidr = input(f"{self.THEME['secondary']}[?] Enter CIDR (e.g., 192.168.1.0/24): ").strip()
                try:
                    import ipaddress
                    network = ipaddress.ip_network(cidr, strict=False)
                    ips = [str(ip) for ip in network.hosts()]
                    
                    print(f"{self.THEME['info']}[*] Network contains {len(ips):,} IP addresses")
                    
                    sample = input(f"{self.THEME['secondary']}[?] Check all or sample? (all/sample): ").lower()
                    if sample == 'sample':
                        sample_size = input(f"{self.THEME['secondary']}[?] Sample size (default 100): ").strip()
                        sample_size = int(sample_size) if sample_size.isdigit() else 100
                        ips = random.sample(ips, min(sample_size, len(ips)))
                    
                    if ips:
                        threads = input(f"{self.THEME['secondary']}[?] Concurrent threads (default 50): ").strip()
                        threads = int(threads) if threads.isdigit() else 50
                        
                        self.check_batch(ips, threads)
                        self.display_summary()
                
                except Exception as e:
                    print(f"{self.THEME['error']}[!] Invalid CIDR: {e}")
            
            elif choice == '5':
                # Load previous results
                filename = input(f"{self.THEME['secondary']}[?] Enter results JSON file: ").strip()
                if os.path.exists(filename):
                    try:
                        with open(filename, 'r') as f:
                            data = json.load(f)
                            self.results = data.get('results', [])
                            print(f"{self.THEME['success']}[✓] Loaded {len(self.results)} results")
                    except Exception as e:
                        print(f"{self.THEME['error']}[!] Error loading file: {e}")
                else:
                    print(f"{self.THEME['error']}[!] File not found")
            
            elif choice == '6':
                # Export settings
                print(f"\n{self.THEME['info']}Export formats:")
                print(f"{self.THEME['secondary']}  1. JSON (full data)")
                print(f"{self.THEME['secondary']}  2. CSV (spreadsheet)")
                print(f"{self.THEME['secondary']}  3. TXT (online IPs only)")
                print(f"{self.THEME['secondary']}  4. All formats")
                
                export_choice = input(f"{self.THEME['secondary']}[?] Select format: ").strip()
                formats = {'1': 'json', '2': 'csv', '3': 'txt', '4': 'all'}
                
                if export_choice in formats:
                    self.save_results(formats[export_choice])
            
            elif choice == '7':
                # Exit
                print(f"\n{self.THEME['warning']}[!] Exiting...")
                sys.exit(0)
            
            else:
                print(f"{self.THEME['error']}[!] Invalid option")
            
            input(f"\n{self.THEME['info']}[*] Press Enter to continue...")
            self.print_header()

# Main execution
if __name__ == "__main__":
    try:
        checker = IPCheckerPro()
        checker.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Program interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[!] Unexpected error: {e}")
        sys.exit(1)