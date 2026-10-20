import dns.resolver
import socket
import requests


#Parent Class
class Scanner:

    def __init__(self, domain):
        self.domain = domain
        self._count = 0      

    def show_result(self):
        print("\n----- Scanning Complete -----\n")
        print(f"Total Active Subdomains : {self._count}")


#Child Class (Inheritance)
class SubdomainScanner(Scanner):

    def __init__(self, domain, wordlist):
        super().__init__(domain)

        #Encapsulation
        self.__wordlist = wordlist
        self.__subdomains = []

    def load_subdomains(self):

        try:
            with open(self.__wordlist, "r") as file:
                self.__subdomains = (file.read().splitlines())

        except FileNotFoundError:
            print("Wordlist File Not Found!")

    #Main Scanning method
    def scan(self):
        print("\nScanning Active Subdomains...\n")

        for sub in self.__subdomains:

            #Subdomain create
            url = f"{sub}.{self.domain}"

            try:
                dns.resolver.resolve(url, "A")
                http_url = f"http://{url}"
                https_url = f"https://{url}"

                #first try HTTPS
                try:
                    response = requests.get(https_url,timeout=2)
                    active_url = https_url

                except:
                    #if HTTPS fail - try HTTP
                    response = requests.get(http_url, timeout=2)
                    active_url = http_url

                #Get IP address
                ip_add = socket.gethostbyname(url)

                #Counter
                self._count += 1
                print(f"Active Subdomain {self._count} ---> URL-{active_url} ---> IP Address-{ip_add} ---> Status Code-{response.status_code}")

            except dns.resolver.NXDOMAIN:
                pass
            except dns.resolver.NoAnswer:
                pass
            except requests.ConnectionError:
                pass
            except requests.Timeout:
                pass
            except Exception as error:
                print("Error:", error)

def main():
    print("\n========== SUBDOMAIN ENUMERATOR ==========")

    domain = input("Enter Domain : ")

    #Objects
    scanner = SubdomainScanner(domain, "Subdomains.txt")
    scanner.load_subdomains()
    scanner.scan()
    scanner.show_result()

if __name__ == "__main__":
    main()

#Status Codes Meaning
# Code  	Meaning
# 200	    Success
# 301	    Redirect
# 403   	Forbidden
# 404   	Not Found
# 405       Not Allowed
# 500       Server Error





##Port Scanner...


import socket
from datetime import datetime

#Parent Class
class Scanner:
    def __init__(self, target):
        #Encapsulation
        self.__target = target

    def get_target(self):
        return self.__target

    def start_message(self):
        print(f"Scanning Target IP: {self.__target}")
        print(f"Started At: {datetime.now()}\n")
        

#Child Class (Inheritance)
class PortScanner(Scanner):
    Common_Services = {20: "FTP Data",21: "FTP",22: "SSH", 23: "Telnet",25: "SMTP",53: "DNS",80: "HTTP",110: "POP3",143: "IMAP",443: "HTTPS",3306: "MySQL",8080: "HTTP Proxy"}

    def __init__(self, target, ports):
        #Parent constructor call
        super().__init__(target)
        #Encapsulation
        self.__ports = ports

    def scan_ports(self):
        self.start_message()

        self.found = False

        for port in self.__ports:
            self.__scan_single_port(port)

        if self.found == False:
            print("No open ports found OR IP not responding")

    #Private Method
    def __scan_single_port(self, port):

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)

            #Connect to target port
            result = sock.connect_ex((self.get_target(), port))

            if result == 0:
                self.found = True
                service = self.Common_Services.get(port, "Unknown Service")

                print(f"Open Port {port} ---> {service}")
            sock.close()

        except socket.gaierror:
            print("Hostname could not be resolved")

        except socket.error:
            print("Server not responding")


if __name__ == "__main__":
    print("\n========== PORT SCANNER ==========")

    target_ip = input("Enter Target IP Address: ")
    print("\nScanning Start...\n")

    ports_to_scan = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]

    # Objects
    scanner = PortScanner(target_ip, ports_to_scan)
    scanner.scan_ports()
    print("\nScanning Complete!\n")