import requests

#Parent Class
class Scanner:

    def __init__(self, url):
        self.url = url
        self._found = 0     

    def show_summary(self):
        print("\nScan Complete !!!")
        print(f"Total SQL Errors Found : {self._found}")

#Child Class (Inheritance)
class SQLInjectionScanner(Scanner):

    def __init__(self, url, username):

        super().__init__(url)
        self.__username = username      
        self.__sql_errors = ["sql syntax", "invalid query", "mysql", "sql state error", "syntax error", "database error", "unclosed quotation", "unknown column"]
        self.__test_passwords = ["", "\"", "'", "\"\"", ";", "'OR 1=1 --"]

    #Encapsulation
    def __test_sqli(self, password):

        try:
            payload = {self.__username: password}
            response = requests.get(self.url, params=payload, timeout=5)
            text = response.text.lower()
            for error in self.__sql_errors:
                if error in text:
                    return True

        except Exception as error:
            print("Error:", error)
        return False

    #Main Scanning Program 
    def scan(self):
        print("\nScanning For SQL Injection...\n")

        for passwd in self.__test_passwords:
            if self.__test_sqli(passwd):

                self._found += 1
                print(f"[VULNERABLE] SQL Error Found ---> Input Used: {passwd}")

            else:
                print(f"[SAFE] No SQL Error Found ---> Input Used: {passwd}")

#Main Function...
def main():
    print("\n========== SQL Injection Tester ==========")


    url = input("Enter URL : ")
    username = input("Enter Username to test : ")

    scanner = SQLInjectionScanner(url, username)
    scanner.scan()
    scanner.show_summary()

if __name__ == "__main__":
    main()







###Password Strength & Brute Force Simulator

import hashlib
import time

#Parent Class
class SecurityTool:

    def __init__(self):
        self._attempts = 0      

    def show_summary(self):
        print(f"\nTotal Attempts : {self._attempts}")

#Child Class (Inheritance)
class PasswordCracker(SecurityTool):

    def __init__(self, password):
        super().__init__()

        #Encapsulation
        self.__password = password

        #Fixed wordlist File
        self.__wordlist_file = "test_pass.txt"

        #Save Original password hash
        self.__saved_hash = self.__hash_password(password)

    #Private method
    def __hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    #Show saved hash...
    def show_saved_hash(self):
        print("\nSaved Data")
        print(f"Original Password : {self.__password}")
        print(f"SHA-256 Hash      : {self.__saved_hash}")

    #Password Cracking...
    def crack_password(self):
        print("\nScanning Password in test_pass.txt file...\n")
        start_time = time.time()
        try:
            with open(self.__wordlist_file,"r") as file:
                for word in file:
                    #remove spaces
                    guess_password = word.strip()
                    self._attempts += 1
                    
                    guess_hash = self.__hash_password(guess_password)
                    print(f"Trying Password {self._attempts} ---> {guess_password}")

                    #Compare hashes
                    if guess_hash == self.__saved_hash:
                        end_time = time.time()

                        print("\n----- Password Found -----")
                        print(f"Matched Password : {guess_password}")
                        print(f"Matched Hash     : {guess_hash}")
                        print(f"Time Taken       : {round(end_time - start_time, 2)} Seconds")
                        return

        except FileNotFoundError:
            print("test_pass.txt File Not Found!")
        print(f"\nPassword Not Found in test_pass.txt file!")

def main():
    print("\n========== PASSWORD STRENGTH & BRUTE FORCE SIMULATOR ==========")

    password = input("\nEnter password to crack : ")

    #Objects
    cracker = PasswordCracker(password)
    cracker.show_saved_hash()
    cracker.crack_password()
    cracker.show_summary()

if __name__ == "__main__":
    main()



