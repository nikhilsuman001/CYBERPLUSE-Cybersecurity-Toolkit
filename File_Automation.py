"""
File & Folder Automation Tool
Provides file creation, reading, writing, and automated directory organization by file type.
"""

import os
import shutil
from datetime import datetime


# Parent Base Class
class BaseTool:
    def __init__(self, name="File Automation Tool"):
        self.name = name
        self._status = "Ready"

    def get_status(self):
        return self._status


# Child Class (Inheritance & Encapsulation)
class FileAutomationTool(BaseTool):
    # Mapping of file categories to extensions
    CATEGORIES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".csv", ".pptx", ".ppt", ".odt"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "Code_Data": [".py", ".js", ".html", ".css", ".json", ".xml", ".sql", ".java", ".c", ".cpp", ".php"],
        "Audio_Video": [".mp3", ".wav", ".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
        "Executables": [".exe", ".msi", ".bat", ".sh", ".cmd"]}

    def __init__(self):
        super().__init__("File & Folder Automation")

    def create_file(self, filepath, content=""):
        """Create a new file with optional initial content."""
        try:
            folder = os.path.dirname(filepath)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            self._status = f"File created: {os.path.basename(filepath)}"
            return True, f"File successfully created: {filepath}"
        except Exception as e:
            self._status = f"Error: {e}"
            return False, str(e)

    def read_file(self, filepath):
        """Read content from a text file."""
        try:
            if not os.path.exists(filepath):
                return False, f"File does not exist: {filepath}"
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            self._status = f"File read: {os.path.basename(filepath)}"
            return True, content
        except Exception as e:
            self._status = f"Error: {e}"
            return False, str(e)

    def write_file(self, filepath, content, mode="w"):
        """Write or append content to a file."""
        try:
            folder = os.path.dirname(filepath)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)

            with open(filepath, mode, encoding="utf-8") as f:
                f.write(content)
            self._status = f"File written ({mode}): {os.path.basename(filepath)}"
            return True, f"Content successfully written to: {filepath}"
        except Exception as e:
            self._status = f"Error: {e}"
            return False, str(e)

    def organize_folder(self, folder_path):
        """Organize files in the target directory into categorized subfolders."""
        if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
            return False, f"Target directory not found: {folder_path}", []

        results = []
        try:
            entries = os.listdir(folder_path)
            category_names = set(self.CATEGORIES.keys())
            category_names.add("Others")

            moved_count = 0
            for item in entries:
                src_path = os.path.join(folder_path, item)

                # Skip directories (including already created category folders)
                if os.path.isdir(src_path):
                    continue

                _, ext = os.path.splitext(item)
                ext = ext.lower()

                # Determine target category
                target_category = "Others"
                for cat, extensions in self.CATEGORIES.items():
                    if ext in extensions:
                        target_category = cat
                        break

                dest_dir = os.path.join(folder_path, target_category)
                os.makedirs(dest_dir, exist_ok=True)

                dest_path = os.path.join(dest_dir, item)
                shutil.move(src_path, dest_path)
                moved_count += 1
                results.append((item, target_category))

            self._status = f"Organized {moved_count} files"
            return True, f"Successfully organized {moved_count} files in: {folder_path}", results
        except Exception as e:
            self._status = f"Error: {e}"
            return False, str(e), results


def main():
    print("=" * 50)
    print("📁 FILE & FOLDER AUTOMATION TOOL")
    print("=" * 50)
    tool = FileAutomationTool()

    print("\n1. Create File")
    print("2. Read File")
    print("3. Write / Append to File")
    print("4. Organize Directory by Extension")
    choice = input("\nSelect Option (1-4): ").strip()

    if choice == "1":
        path = input("Enter file path to create: ").strip()
        data = input("Enter initial content (optional): ")
        success, msg = tool.create_file(path, data)
        print(f"[{'SUCCESS' if success else 'FAILED'}] {msg}")

    elif choice == "2":
        path = input("Enter file path to read: ").strip()
        success, msg = tool.read_file(path)
        if success:
            print(f"\n--- Content of {path} ---")
            print(msg)
        else:
            print(f"[FAILED] {msg}")

    elif choice == "3":
        path = input("Enter file path: ").strip()
        data = input("Enter text content: ")
        m = input("Mode ('w' for overwrite, 'a' for append): ").strip() or "w"
        success, msg = tool.write_file(path, data, mode=m)
        print(f"[{'SUCCESS' if success else 'FAILED'}] {msg}")

    elif choice == "4":
        folder = input("Enter directory path to organize: ").strip()
        success, msg, items = tool.organize_folder(folder)
        print(f"[{'SUCCESS' if success else 'FAILED'}] {msg}")
        for item, cat in items:
            print(f"  → Moved {item} -> {cat}/")

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
