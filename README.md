# 🛡️ CYBERPULSE // Modular Security & Automation Toolkit

> **A professional, modular Python cybersecurity and operational automation suite combining Object-Oriented Programming (OOP), file handling, CustomTkinter GUI, REST APIs, cryptography, automation, and network diagnostics into one unified dashboard.**

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Project Objectives](#-project-objectives)
- [Authentication & Login](#-authentication--login)
- [Key Features & 8 Core Modules](#-key-features--8-core-modules)
- [Project Directory Structure](#-project-directory-structure)
- [Technical Requirements](#-technical-requirements)
- [Installation & Quick Start](#-installation--quick-start)
- [Detailed Module Walkthrough](#-detailed-module-walkthrough)
- [Executive Reporting & Audit Log](#-executive-reporting--audit-log)
- [Standalone CLI Usage](#-standalone-cli-usage)
- [Ethical & Educational Disclaimer](#-ethical--educational-disclaimer)

---

## 🌟 Overview

**CyberPulse** is an enterprise-grade security and automation toolkit developed in Python 3. It brings together essential cybersecurity utilities, system monitoring, file automation, and cryptographic tools under a modern, dark-themed **CustomTkinter** graphical user interface.

The project is structured following clean **Object-Oriented Programming (OOP)** patterns (Inheritance, Encapsulation, and Polymorphism), separation of concerns, multi-threaded task management, and responsive background execution to ensure the user interface never freezes.

---

## 🎯 Project Objectives

- **Modular Architecture**: Clean separation between backend logic modules and the frontend presentation layer.
- **OOP Implementation**: Base parent classes with derived child classes encapsulating private state variables and methods.
- **Comprehensive Security Spectrum**:
  1. Central GUI Dashboard with hardware telemetry.
  2. File & Folder Automation with automated extension-based categorization.
  3. Cryptographic utilities (MD5, SHA-256 hashing, Fernet AES-256 file encryption).
  4. REST API Tester (GET / POST requests with JSON formatting).
  5. Networking tools (Subdomain enumeration and TCP port scanning).
  6. Wordlist Brute-Force Simulator (Offline & safe SHA-256 dictionary matching).
  7. SQL Injection Tester (Boundary payload fuzzing & error disclosure detection).
  8. System Surveillance & Activity Logging (Periodic screenshots & event trail).

---

## 🔒 Authentication & Login

The toolkit is protected by a gateway login screen. Only authenticated operators are granted access to the suite.

- **Default Operator Username**: `cybernikhil001`
- **Default Security Password**: `Secure#$995`

*(Features include show/hide password toggle, keyboard Enter binding, and animated access transition.)*

---

## 🚀 Key Features & 8 Core Modules

| # | Requirement | Implementation Module | Primary Capabilities |
| :---: | :--- | :--- | :--- |
| **1** | **Central Tkinter Dashboard** | `app.py` (`CyberToolkitGUI`) | Unified control center, CPU/RAM/Disk telemetry, host metrics, and quick launchpad cards for all tools. |
| **2** | **File & Folder Automation** | `File_Automation.py` (`FileAutomationTool`) | Create, read, overwrite, and append files; automatically organizes directories into categorized subfolders (`Images`, `Documents`, `Archives`, `Code_Data`, etc.). |
| **3** | **Hashing & Encryption** | `File_Cryptography.py` (`HashUtility`, `FileEncryptor`) | MD5 & SHA-256 text and file hashing; Fernet symmetric AES-256 file encryption/decryption with automatic key persistence in `keys.json`. |
| **4** | **REST API Tester** | `API_Tester.py` (`APITester`) | Send HTTP GET/POST requests, pass custom headers and JSON body, inspect response codes, measure latency, and view formatted JSON. |
| **5** | **Networking Tools** | `Subdomain_Port_Scanner.py` (`SubdomainScanner`, `PortScanner`) | Resolve active subdomains and scan TCP ports across target hosts with service identification and response metrics. |
| **6** | **Wordlist Brute-Force Simulator** | `SQLI_Password.py` (`PasswordCracker`) | Safe, offline dictionary matching against SHA-256 hashes using `test_pass.txt` + real-time password strength and entropy evaluator. |
| **7** | **SQL Injection Tester** | `SQLI_Password.py` (`SQLInjectionScanner`) | Probes target parameters with sample boundary payloads (`'`, `"`, `' OR 1=1 --`) to detect abnormal database error disclosures (CWE-209). |
| **8** | **System Activity & Screenshots** | `System_Monitoring.py` (`ActivityLogger`) | Automated periodic screen captures, live thumbnail preview in UI, and chronological timestamped event logging in `activity_log.txt`. |

---

## 📂 Project Directory Structure

```text
d:/Tool/ASD/
├── app.py                      # Main Tkinter/CustomTkinter GUI Application
├── File_Automation.py          # Module: File handling & Directory organizer (OOP)
├── File_Cryptography.py        # Module: MD5/SHA256 Hashing & Fernet AES-256 Encryptor
├── API_Tester.py               # Module: HTTP GET/POST REST API Tester
├── Subdomain_Port_Scanner.py   # Module: Subdomain Enumerator & TCP Port Scanner
├── SQLI_Password.py            # Module: SQL Injection Tester & Password Cracker
├── System_Monitoring.py        # Module: Desktop Screenshot & Activity Logger
├── requirements.txt            # Python package dependencies
├── README.md                   # Complete documentation
├── Project_Report_CyberPulse.docx # Editable Word Document Report
├── keys.json                   # Encrypted files Fernet key storage
├── activity_log.txt            # System monitoring event log
├── password_data.txt           # Generated cryptographic tokens storage
├── test_pass.txt               # Wordlist dictionary for offline brute-force demo
├── Subdomains.txt              # Subdomain wordlist dictionary
└── screenshots/                # Directory storing captured desktop screenshots
```

---

## 💻 Technical Requirements

- **Programming Language**: Python 3.10+ (Fully compatible with Python 3.11, 3.12, 3.13, 3.14)
- **GUI Framework**: `customtkinter`, `tkinter`
- **Core Libraries**:
  - `requests` (HTTP API communication)
  - `cryptography` (Fernet AES-256 encryption)
  - `hashlib` (MD5 & SHA-256 message digests)
  - `psutil` (Hardware & resource telemetry)
  - `pyautogui` & `Pillow` (Screenshot capture & image handling)
  - `openpyxl` (Executive Excel audit report generation)
  - `socket` & `ssl` (Low-level TCP networking & banner probing)
  - `json` & `os` (File manipulation & data serialization)

---

## ⚙️ Installation & Quick Start

### 1. Clone or Open the Workspace
```powershell
cd d:\Tool\ASD
```

### 2. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Launch the Application
```powershell
python app.py
```

### 4. Authenticate
Enter credentials:
- **Username**: `cybernikhil001`
- **Password**: `Secure#$995`
- Click **"AUTHENTICATE & LAUNCH →"** or press **Enter**.

---

## 🔍 Detailed Module Walkthrough

### 1. Dashboard Overview
- Real-time CPU, RAM, Disk, and Hostname telemetry updated dynamically via background threads.
- Modular launchpad cards providing one-click access to each tool in the suite.

### 2. File & Folder Automation Tool
- **File Management**: Create files, read text files, overwrite or append content safely.
- **Directory Organizer**: Automatically scans any target directory and moves files into organized folders:
  - `Images/` (`.jpg`, `.png`, `.gif`, `.svg`, `.webp`)
  - `Documents/` (`.pdf`, `.docx`, `.txt`, `.xlsx`, `.csv`)
  - `Archives/` (`.zip`, `.rar`, `.7z`, `.tar`, `.gz`)
  - `Code_Data/` (`.py`, `.js`, `.html`, `.css`, `.json`, `.sql`)
  - `Audio_Video/` (`.mp3`, `.mp4`, `.wav`, `.mkv`)
  - `Others/`

### 3. Hashing & Encryption Utilities
- **Hashing**: Computes MD5 and SHA-256 digests for arbitrary plaintext strings or complete binary files.
- **Fernet Encryption**: Performs symmetric AES-256 encryption on sensitive documents. Keys are automatically maintained and persisted in `keys.json`.

### 4. REST API Tester
- Supports both `GET` and `POST` methods.
- Accepts custom headers and JSON request bodies.
- Displays HTTP response code badges (e.g., `200 OK` in green, `404` in amber, `500` in red), execution latency in milliseconds, and prettified JSON outputs.

### 5. Networking Tools
- **Subdomain Finder**: Discovers active endpoints on a root domain using DNS queries and HTTP fallback verification.
- **Port Scanner**: Multi-threaded TCP connect scan across standard presets (Common Ports, Web Infrastructure, Database Engines, Fast 1-100) with banner identification.

### 6. Wordlist Brute-Force Simulator
- Evaluates real-time password strength, length, entropy, and character diversity.
- Demonstrates safe, offline dictionary matching against SHA-256 hashes using candidate entries from `test_pass.txt`.

### 7. SQL Injection Tester
- Sends boundary test payloads (e.g., single quotes, double quotes, boolean tautologies) to analyze web endpoint resilience against database error disclosure (CWE-209).

### 8. System Logging & Screenshot Capture
- Configurable interval (seconds) and capture count.
- Saves high-resolution desktop frames to the `screenshots/` directory.
- Logs events chronologically to `activity_log.txt`.
- Displays real-time thumbnail preview of the most recent capture directly within the GUI.

---

## 📑 Executive Reporting & Audit Log

The toolkit records operational actions in an audit trail:
- Displays a real-time table of past actions, targets, severities, and timestamps.
- **Export to Excel (.xlsx)**: Generates stylized, executive-level Excel workbooks complete with headers, color-coded severity tags, and borders using `openpyxl`.

---

## 💻 Standalone CLI Usage

Each backend module can also be executed directly from the terminal without launching the GUI:

```powershell
# File Automation
python File_Automation.py

# Cryptography & Hashing
python File_Cryptography.py

# REST API Tester
python API_Tester.py

# Subdomain & Port Scanner
python Subdomain_Port_Scanner.py

# SQLi Tester & Brute-Force Simulator
python SQLI_Password.py

# System Monitoring & Screenshots
python System_Monitoring.py
```

---

## ⚖️ Ethical & Educational Disclaimer

> **IMPORTANT**: This toolkit was created exclusively for educational, academic, and defensive security auditing purposes. All testing features (such as SQL injection testing, port scanning, and dictionary simulation) must only be performed on authorized systems, local test environments, or deliberately vulnerable sandbox applications (e.g., testphp.vulnweb.com). Unauthorized probing of third-party networks is illegal and strictly prohibited.
