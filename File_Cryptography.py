"""
Hashing & Encryption Utilities
Provides MD5 and SHA-256 text & file hashing, along with Fernet symmetric AES-256 file encryption/decryption.
"""

import os
import json
import secrets
import string
import hashlib
from cryptography.fernet import Fernet


# Parent Base Class
class SecurityTool:
    def __init__(self, name="Security Tool"):
        self.name = name
        self._status = "Ready"

    def show_status(self):
        print(f"\nTool Status : {self._status}")

    def get_status(self):
        return self._status


# Child Class: Hash Utility (MD5 & SHA256 for Text and Files)
class HashUtility(SecurityTool):
    def __init__(self):
        super().__init__("Hashing Utility")

    def hash_text(self, text, algorithm="sha256"):
        """Generate MD5 or SHA-256 hash digest of a text string."""
        algo = algorithm.lower().strip()
        data = text.encode("utf-8")
        if algo == "md5":
            digest = hashlib.md5(data).hexdigest()
        else:
            digest = hashlib.sha256(data).hexdigest()
        self._status = f"Hashed text ({algo.upper()})"
        return digest

    def hash_file(self, filepath, algorithm="sha256"):
        """Generate MD5 or SHA-256 hash digest of a file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        algo = algorithm.lower().strip()
        hasher = hashlib.md5() if algo == "md5" else hashlib.sha256()

        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)

        digest = hasher.hexdigest()
        self._status = f"Hashed file {os.path.basename(filepath)} ({algo.upper()})"
        return digest


# Child Class: File Encryptor (Fernet AES-256)
class FileEncryptor(SecurityTool):
    def __init__(self, filename):
        super().__init__("File Encryptor")
        self.__filename = filename
        self.__json_file = "keys.json"
        self.__key = None
        self.__fernet = None
        self.__load_or_create_key()

    def __load_or_create_key(self):
        keys_data = {}
        if os.path.exists(self.__json_file):
            try:
                with open(self.__json_file, "r") as file:
                    keys_data = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                keys_data = {}

        if self.__filename in keys_data:
            self.__key = keys_data[self.__filename].encode()
        else:
            self.__key = Fernet.generate_key()
            keys_data[self.__filename] = self.__key.decode()
            with open(self.__json_file, "w") as file:
                json.dump(keys_data, file, indent=4)

        self.__fernet = Fernet(self.__key)

    def get_key(self):
        return self.__key.decode() if self.__key else ""

    def encrypt_file(self):
        if not os.path.exists(self.__filename):
            raise FileNotFoundError(f"File not found: {self.__filename}")

        with open(self.__filename, "rb") as file:
            data = file.read()

        encrypted_data = self.__fernet.encrypt(data)
        with open(self.__filename, "wb") as file:
            file.write(encrypted_data)

        self._status = "File Encrypted"
        return self.get_key()

    def decrypt_file(self):
        if not os.path.exists(self.__filename):
            raise FileNotFoundError(f"File not found: {self.__filename}")

        with open(self.__filename, "rb") as file:
            encrypted_data = file.read()

        decrypted_data = self.__fernet.decrypt(encrypted_data)
        with open(self.__filename, "wb") as file:
            file.write(decrypted_data)

        self._status = "File Decrypted"
        return True


# Child Class: Password Generator
class PasswordGenerator(SecurityTool):
    def __init__(self, length=16):
        super().__init__("Password Generator")
        self.__length = max(length, 4)
        self.__password = ""
        self.__salt = ""
        self.__hashed_password = ""

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        self.__password = "".join(secrets.choice(characters) for _ in range(self.__length))
        self._status = "Password Generated"
        return self.__password

    def hash_password(self):
        self.__salt = secrets.token_hex(8)
        salted_password = self.__password + self.__salt
        self.__hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
        self._status = "Password Hashed"
        return self.__hashed_password

    def save_to_file(self, filename="password_data.txt"):
        try:
            with open(filename, "a") as file:
                file.write(f"\nPassword : {self.__password}\n")
                file.write(f"Salt     : {self.__salt}\n")
                file.write(f"Hash     : {self.__hashed_password}\n")
                file.write("-" * 30 + "\n")
            self._status = "Data Saved"
            return True
        except Exception as error:
            self._status = f"Error: {error}"
            return False

    def show_result(self):
        print("\n----- Generated Password -----")
        print(f"Password     : {self.__password}")
        print(f"Salt         : {self.__salt}")
        print(f"SHA-256 Hash : {self.__hashed_password}")


def main():
    print("=" * 50)
    print("🔒 HASHING & ENCRYPTION UTILITIES")
    print("=" * 50)
    print("1. Hash Text (MD5 / SHA-256)")
    print("2. Hash File (MD5 / SHA-256)")
    print("3. Encrypt File (Fernet)")
    print("4. Decrypt File (Fernet)")
    print("5. Generate Strong Password")

    choice = input("\nEnter Choice (1-5): ").strip()
    hasher = HashUtility()

    if choice == "1":
        text = input("Enter text to hash: ")
        algo = input("Algorithm (md5 / sha256) [Default: sha256]: ").strip() or "sha256"
        print(f"\n{algo.upper()} Digest: {hasher.hash_text(text, algo)}")

    elif choice == "2":
        path = input("Enter file path to hash: ").strip()
        algo = input("Algorithm (md5 / sha256) [Default: sha256]: ").strip() or "sha256"
        try:
            print(f"\n{algo.upper()} Digest: {hasher.hash_file(path, algo)}")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "3":
        fname = input("Enter file name to encrypt: ").strip()
        try:
            enc = FileEncryptor(fname)
            key = enc.encrypt_file()
            print(f"\n[SUCCESS] File encrypted successfully!")
            print(f"Secret Key: {key}")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "4":
        fname = input("Enter file name to decrypt: ").strip()
        try:
            enc = FileEncryptor(fname)
            enc.decrypt_file()
            print("\n[SUCCESS] File decrypted successfully!")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == "5":
        length = int(input("Enter length [Default: 16]: ").strip() or "16")
        gen = PasswordGenerator(length)
        gen.generate_password()
        gen.hash_password()
        gen.show_result()
        gen.save_to_file()
        print("Password saved to password_data.txt")

    else:
        print("Invalid Choice!")


if __name__ == "__main__":
    main()