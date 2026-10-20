# ==============================================================================
# CYBERPULSE // MODULAR SECURITY & AUTOMATION TOOLKIT
# Professional Cybersecurity Suite & Operational Intelligence Center
# Automated cyber security suite by cybernikhil001
# ==============================================================================

import os
import sys
import time
import socket
import ssl
import json
import string
import hashlib
import threading
from datetime import datetime

import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image
import requests
import psutil
import pyautogui

try:
    from openpyxl import Workbook
    from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

# Ensure workspace paths exist in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import Modular Security Tools
from File_Automation import FileAutomationTool
from File_Cryptography import HashUtility, FileEncryptor, PasswordGenerator
from API_Tester import APITester
from Subdomain_Port_Scanner import SubdomainScanner, PortScanner
from SQLI_Password import SQLInjectionScanner, PasswordCracker
from System_Monitoring import ActivityLogger


# ==============================================================================
# REPORT GENERATOR (EXECUTIVE AUDIT LOGGER & EXCEL EXPORTER)
# ==============================================================================

class ReportGenerator:
    """Enterprise-grade audit logger and stylized Excel report generator."""

    def __init__(self):
        self.records = []

    def add_result(self, module, target, result, severity="INFO"):
        record = {
            "id": len(self.records) + 1,
            "module": str(module),
            "target": str(target),
            "severity": str(severity).upper(),
            "result": str(result),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.records.append(record)
        return record

    def clear(self):
        self.records.clear()

    def save_report(self, filepath="security_report.xlsx"):
        if not HAS_OPENPYXL:
            raise RuntimeError("openpyxl library is required for Excel export.")

        wb = Workbook()
        ws = wb.active
        ws.title = "Executive Audit Log"
        ws.views.sheetView[0].showGridLines = True

        # Document Header
        ws.merge_cells("A1:F1")
        title_cell = ws["A1"]
        title_cell.value = "CYBERPULSE SECURITY INTELLIGENCE - AUDIT REPORT"
        title_cell.font = Font(name="Segoe UI", size=15, bold=True, color="FFFFFF")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        title_cell.fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
        ws.row_dimensions[1].height = 36

        # Subtitle Info
        ws.merge_cells("A2:F2")
        meta_cell = ws["A2"]
        meta_cell.value = f"Author: cybernikhil001  |  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  Records: {len(self.records)}"
        meta_cell.font = Font(name="Segoe UI", size=10, italic=True, color="94A3B8")
        meta_cell.alignment = Alignment(horizontal="center", vertical="center")
        meta_cell.fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        ws.row_dimensions[2].height = 22

        headers = ["#", "Module / Tool", "Target / Asset", "Severity / Status", "Finding & Summary", "Timestamp"]
        ws.append([])  # Spacer
        ws.append(headers)

        header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
        header_font = Font(name="Segoe UI", size=11, bold=True, color="38BDF8")
        thin_border = Border(
            left=Side(style="thin", color="334155"),
            right=Side(style="thin", color="334155"),
            top=Side(style="thin", color="334155"),
            bottom=Side(style="thin", color="334155")
        )

        ws.row_dimensions[4].height = 26
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=4, column=col_idx)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        for i, rec in enumerate(self.records, start=5):
            ws.row_dimensions[i].height = 22
            row_data = [rec["id"], rec["module"], rec["target"], rec["severity"], rec["result"], rec["timestamp"]]
            ws.append(row_data)

            is_even = (i % 2 == 0)
            zebra_fill = PatternFill(start_color="F8FAFC" if is_even else "FFFFFF", fill_type="solid")

            for col_idx in range(1, 7):
                c = ws.cell(row=i, column=col_idx)
                c.fill = zebra_fill
                c.font = Font(name="Segoe UI", size=10, color="0F172A")
                c.border = thin_border
                c.alignment = Alignment(vertical="center", horizontal="center" if col_idx in [1, 4, 6] else "left")

        for col in ws.columns:
            col_letter = get_column_letter(col[0].column)
            max_len = max((len(str(cell.value or "")) for cell in col), default=12)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        wb.save(filepath)
        return filepath


# ==============================================================================
# MAIN GUI CLASS - CYBERPULSE SUITE
# ==============================================================================

class CyberToolkitGUI:

    AUTH_USER = "cybernikhil001"
    AUTH_PASS = "Secure#$995"

    def __init__(self, root):
        self.root = root
        self.root.title("CYBERPULSE // Modular Security & Automation Toolkit")
        self.root.geometry("1240x780")
        self.root.minsize(1120, 680)

        # Apply Modern CustomTkinter Appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # System State
        self.running_event = threading.Event()
        self.report = ReportGenerator()
        self.is_authenticated = False

        # Tools Backend Instances
        self.file_tool = FileAutomationTool()
        self.crypto_tool = HashUtility()
        self.api_tool = APITester()

        # Color Theme Constants
        self.colors = {
            "bg_dark": "#0B0F19",
            "sidebar_bg": "#0D1117",
            "card_bg": "#161B22",
            "card_border": "#21262D",
            "accent_cyan": "#00D2FF",
            "accent_blue": "#2563EB",
            "accent_green": "#10B981",
            "accent_red": "#EF4444",
            "accent_purple": "#8B5CF6",
            "accent_amber": "#F59E0B",
            "text_light": "#F8FAFC",
            "text_muted": "#94A3B8",
            "console_bg": "#070A10"
        }

        # Build Login & Main Framework
        self.build_login_screen()

    # --------------------------------------------------------------------------
    # AUTHENTICATION SCREEN (LOGIN GATEWAY)
    # --------------------------------------------------------------------------

    def build_login_screen(self):
        self.login_frame = ctk.CTkFrame(self.root, fg_color=self.colors["bg_dark"], corner_radius=0)
        self.login_frame.pack(fill="both", expand=True)

        center_card = ctk.CTkFrame(
            self.login_frame,
            width=460,
            fg_color=self.colors["card_bg"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["card_border"]
        )
        center_card.place(relx=0.5, rely=0.5, anchor="center")

        c_inner = ctk.CTkFrame(center_card, fg_color="transparent")
        c_inner.pack(padx=36, pady=36, fill="x")

        logo_lbl = ctk.CTkLabel(
            c_inner,
            text="🛡️ CYBERPULSE",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        logo_lbl.pack(pady=(0, 2))

        sub_lbl = ctk.CTkLabel(
            c_inner,
            text="Automated cyber security suite by cybernikhil001",
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            text_color=self.colors["text_light"]
        )
        sub_lbl.pack(pady=(0, 16))

        lock_badge = ctk.CTkLabel(
            c_inner,
            text="🔒 AUTHENTICATION REQUIRED",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.colors["accent_amber"],
            fg_color="#1E293B",
            corner_radius=6,
            height=26
        )
        lock_badge.pack(fill="x", pady=(0, 20))

        u_lbl = ctk.CTkLabel(c_inner, text="Operator Username:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_muted"])
        u_lbl.pack(anchor="w", pady=(0, 4))

        self.user_entry = ctk.CTkEntry(
            c_inner,
            height=40,
            placeholder_text="Enter username...",
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.user_entry.pack(fill="x", pady=(0, 14))
        self.user_entry.insert(0, "cybernikhil001")

        p_lbl = ctk.CTkLabel(c_inner, text="Security Password:", font=ctk.CTkFont(size=12, weight="bold"), text_color=self.colors["text_muted"])
        p_lbl.pack(anchor="w", pady=(0, 4))

        self.pass_entry = ctk.CTkEntry(
            c_inner,
            height=40,
            show="*",
            placeholder_text="Enter password...",
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.pass_entry.pack(fill="x", pady=(0, 14))

        self.show_pass_var = tk.BooleanVar(value=False)
        show_pass_cb = ctk.CTkCheckBox(
            c_inner,
            text="Show Password",
            variable=self.show_pass_var,
            font=ctk.CTkFont(size=11),
            text_color=self.colors["text_muted"],
            command=self._toggle_login_password
        )
        show_pass_cb.pack(anchor="w", pady=(0, 16))

        self.login_msg_lbl = ctk.CTkLabel(
            c_inner,
            text="",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["accent_red"]
        )
        self.login_msg_lbl.pack(pady=(0, 10))

        login_btn = ctk.CTkButton(
            c_inner,
            text="AUTHENTICATE & LAUNCH →",
            height=44,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=self.colors["accent_blue"],
            hover_color="#1D4ED8",
            command=self.authenticate
        )
        login_btn.pack(fill="x")

        self.user_entry.bind("<Return>", lambda e: self.authenticate())
        self.pass_entry.bind("<Return>", lambda e: self.authenticate())
        self.pass_entry.focus_set()

    def _toggle_login_password(self):
        self.pass_entry.configure(show="" if self.show_pass_var.get() else "*")

    def authenticate(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get()

        if u == self.AUTH_USER and p == self.AUTH_PASS:
            self.login_msg_lbl.configure(
                text="✓ Access Granted! Initializing CyberPulse...",
                text_color=self.colors["accent_green"]
            )
            self.is_authenticated = True
            self.root.after(350, self._unlock_suite)
        else:
            self.login_msg_lbl.configure(
                text="✕ Access Denied: Invalid Username or Password.",
                text_color=self.colors["accent_red"]
            )

    def _unlock_suite(self):
        self.login_frame.pack_forget()
        self.main_container = ctk.CTkFrame(self.root, fg_color="transparent", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)

        self.build_shell()
        self.build_pages()
        self.show_page("dashboard")
        self.start_telemetry_loop()

    def logout(self):
        self.is_authenticated = False
        self.main_container.destroy()
        self.build_login_screen()

    # --------------------------------------------------------------------------
    # SHELL & SIDEBAR NAVIGATION
    # --------------------------------------------------------------------------

    def build_shell(self):
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Left Sidebar
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=270,
            corner_radius=0,
            fg_color=self.colors["sidebar_bg"],
            border_width=1,
            border_color=self.colors["card_border"]
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Branding
        brand_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        brand_frame.pack(fill="x", padx=16, pady=(18, 12))

        brand_badge = ctk.CTkLabel(
            brand_frame,
            text="🛡️ CYBERPULSE",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        brand_badge.pack(anchor="w")

        brand_subtitle = ctk.CTkLabel(
            brand_frame,
            text="Automated cyber security suite by cybernikhil001",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_muted"]
        )
        brand_subtitle.pack(anchor="w")

        divider = ctk.CTkFrame(self.sidebar, height=1, fg_color=self.colors["card_border"])
        divider.pack(fill="x", padx=14, pady=6)

        # 8 Core Toolkit Requirements Navigation
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊  Dashboard Overview"),
            ("file_auto", "📁  File & Folder Automation"),
            ("crypto", "🔒  Hashing & Encryption"),
            ("api_tester", "🌐  REST API Tester"),
            ("network", "⚡  Networking Tools"),
            ("brute_force", "🔑  Wordlist Brute-Force"),
            ("sqli", "🎯  SQL Injection Tester"),
            ("monitor", "🖥️  Activity & Screenshot"),
            ("report", "📑  Audit & Excel Reports")
        ]

        nav_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        nav_scroll.pack(fill="both", expand=True, padx=6, pady=4)

        for key, label in nav_items:
            btn = ctk.CTkButton(
                nav_scroll,
                text=label,
                anchor="w",
                font=ctk.CTkFont(family="Segoe UI", size=13, weight="normal"),
                fg_color="transparent",
                text_color=self.colors["text_light"],
                hover_color="#1E293B",
                height=38,
                corner_radius=8,
                command=lambda k=key: self.show_page(k)
            )
            btn.pack(fill="x", padx=6, pady=2)
            self.nav_buttons[key] = btn

        # Sidebar Footer
        footer_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=14, pady=12)

        self.status_pill = ctk.CTkLabel(
            footer_frame,
            text="● ENGINE: READY",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#10B981"
        )
        self.status_pill.pack(anchor="w", pady=(0, 6))

        op_row = ctk.CTkFrame(footer_frame, fg_color="#1E293B", corner_radius=6)
        op_row.pack(fill="x", pady=(0, 8))

        op_lbl = ctk.CTkLabel(
            op_row,
            text="👤 cybernikhil001",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        op_lbl.pack(side="left", padx=8, pady=4)

        logout_btn = ctk.CTkButton(
            op_row,
            text="Logout",
            width=54,
            height=22,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color="#334155",
            hover_color=self.colors["accent_red"],
            command=self.logout
        )
        logout_btn.pack(side="right", padx=6, pady=4)

        theme_row = ctk.CTkFrame(footer_frame, fg_color="transparent")
        theme_row.pack(fill="x", pady=2)

        theme_lbl = ctk.CTkLabel(
            theme_row,
            text="Dark Theme",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color=self.colors["text_muted"]
        )
        theme_lbl.pack(side="left")

        self.theme_switch = ctk.CTkSwitch(
            theme_row,
            text="",
            width=36,
            height=18,
            command=self.toggle_theme
        )
        self.theme_switch.select()
        self.theme_switch.pack(side="right")

        # Right Main Content Canvas
        self.content_area = ctk.CTkFrame(self.main_container, fg_color=self.colors["bg_dark"], corner_radius=0)
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")

    def set_engine_status(self, text, color="#10B981"):
        def _update():
            if hasattr(self, "status_pill"):
                self.status_pill.configure(text=f"● ENGINE: {text.upper()}", text_color=color)
        self.root.after(0, _update)

    # --------------------------------------------------------------------------
    # PAGE MANAGEMENT
    # --------------------------------------------------------------------------

    def build_pages(self):
        self.pages = {}
        pages_builders = {
            "dashboard": self.build_dashboard_page,
            "file_auto": self.build_file_auto_page,
            "crypto": self.build_crypto_page,
            "api_tester": self.build_api_page,
            "network": self.build_network_page,
            "brute_force": self.build_password_page,
            "sqli": self.build_sqli_page,
            "monitor": self.build_monitor_page,
            "report": self.build_report_page
        }

        for key, builder in pages_builders.items():
            page_frame = ctk.CTkScrollableFrame(self.content_area, fg_color="transparent", corner_radius=0)
            builder(page_frame)
            self.pages[key] = page_frame

    def show_page(self, key):
        for page in self.pages.values():
            page.grid_forget()

        if key in self.pages:
            self.pages[key].grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        for btn_key, btn in self.nav_buttons.items():
            if btn_key == key:
                btn.configure(
                    fg_color="#1E293B",
                    text_color=self.colors["accent_cyan"],
                    font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=self.colors["text_light"],
                    font=ctk.CTkFont(family="Segoe UI", size=13, weight="normal")
                )

    # --------------------------------------------------------------------------
    # HELPER: MODERN CONSOLE LOGGER
    # --------------------------------------------------------------------------

    def create_console_card(self, parent, height=220):
        card = ctk.CTkFrame(
            parent,
            fg_color=self.colors["card_bg"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["card_border"]
        )
        card.pack(fill="both", expand=True, pady=10)

        header_row = ctk.CTkFrame(card, fg_color="transparent")
        header_row.pack(fill="x", padx=14, pady=(10, 6))

        title = ctk.CTkLabel(
            header_row,
            text="⚡ REAL-TIME EXECUTION LOGS",
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            text_color=self.colors["accent_cyan"]
        )
        title.pack(side="left")

        clear_btn = ctk.CTkButton(
            header_row,
            text="Clear",
            width=64,
            height=24,
            font=ctk.CTkFont(size=11),
            fg_color="#334155",
            hover_color="#475569",
            command=lambda: textbox.delete("1.0", "end")
        )
        clear_btn.pack(side="right")

        textbox = ctk.CTkTextbox(
            card,
            height=height,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color=self.colors["console_bg"],
            text_color="#38BDF8",
            corner_radius=8
        )
        textbox.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        return textbox

    def log_to_box(self, textbox, message):
        def _append():
            ts = datetime.now().strftime("[%H:%M:%S] ")
            textbox.insert("end", f"{ts}{message}\n")
            textbox.see("end")
        self.root.after(0, _append)

    def stop_current_task(self):
        self.running_event.clear()
        self.set_engine_status("Interrupted", self.colors["accent_red"])

    # --------------------------------------------------------------------------
    # REQUIREMENT 1: CENTRAL DASHBOARD OVERVIEW
    # --------------------------------------------------------------------------

    def build_dashboard_page(self, parent):
        # Hero Banner
        hero = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=14, border_width=1, border_color=self.colors["card_border"])
        hero.pack(fill="x", pady=(0, 14), padx=2)

        hero_inner = ctk.CTkFrame(hero, fg_color="transparent")
        hero_inner.pack(fill="x", padx=20, pady=18)

        hero_title = ctk.CTkLabel(
            hero_inner,
            text="Welcome to CyberPulse Security Suite",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color=self.colors["text_light"]
        )
        hero_title.pack(anchor="w")

        hero_desc = ctk.CTkLabel(
            hero_inner,
            text="Automated cyber security suite by cybernikhil001 | Modular Python Security & Automation Center",
            font=ctk.CTkFont(family="Segoe UI", size=13),
            text_color=self.colors["text_muted"]
        )
        hero_desc.pack(anchor="w", pady=(4, 0))

        # Telemetry Gauges Grid
        gauges_grid = ctk.CTkFrame(parent, fg_color="transparent")
        gauges_grid.pack(fill="x", pady=6)
        gauges_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.cpu_card = self.create_metric_card(gauges_grid, 0, "💻 CPU UTILIZATION", "0%", self.colors["accent_cyan"])
        self.ram_card = self.create_metric_card(gauges_grid, 1, "🧠 MEMORY USAGE", "0%", self.colors["accent_purple"])
        self.disk_card = self.create_metric_card(gauges_grid, 2, "💾 DISK STORAGE", "0%", self.colors["accent_green"])
        self.host_card = self.create_metric_card(gauges_grid, 3, "🌐 LOCAL HOST", socket.gethostname()[:14], self.colors["accent_amber"])

        # Quick Modules Launchpad Grid
        launch_lbl = ctk.CTkLabel(
            parent,
            text="CENTRAL SECURITY MODULES LAUNCHPAD",
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            text_color=self.colors["text_muted"]
        )
        launch_lbl.pack(anchor="w", pady=(18, 8))

        launch_grid = ctk.CTkFrame(parent, fg_color="transparent")
        launch_grid.pack(fill="x")
        launch_grid.grid_columnconfigure((0, 1, 2, 3), weight=1)

        modules = [
            ("file_auto", "📁 File Automation", "Create, Read, Write & Organize", self.colors["accent_cyan"]),
            ("crypto", "🔒 Hashing & Encryption", "MD5, SHA-256 & Fernet AES", self.colors["accent_green"]),
            ("api_tester", "🌐 REST API Tester", "GET/POST & JSON Responses", self.colors["accent_purple"]),
            ("network", "⚡ Networking Tools", "Subdomain Finder & Port Scan", self.colors["accent_blue"]),
            ("brute_force", "🔑 Wordlist Simulator", "Safe Offline SHA-256 Crack", self.colors["accent_amber"]),
            ("sqli", "🎯 SQL Injection Tester", "Boundary Payloads & Error Check", self.colors["accent_red"]),
            ("monitor", "🖥️ Activity Monitor", "Surveillance Screenshots & Logs", "#EC4899"),
            ("report", "📑 Audit Reports", "Excel Spreadsheets & Summary", "#14B8A6")
        ]

        for i, (m_key, m_title, m_sub, m_col) in enumerate(modules):
            row = i // 4
            col = i % 4
            card = ctk.CTkFrame(
                launch_grid,
                fg_color=self.colors["card_bg"],
                corner_radius=12,
                border_width=1,
                border_color=self.colors["card_border"]
            )
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            c_title = ctk.CTkLabel(card, text=m_title, font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=m_col)
            c_title.pack(anchor="w", padx=14, pady=(12, 2))

            c_sub = ctk.CTkLabel(card, text=m_sub, font=ctk.CTkFont(size=11), text_color=self.colors["text_muted"])
            c_sub.pack(anchor="w", padx=14, pady=(0, 10))

            c_btn = ctk.CTkButton(
                card,
                text="Open Tool →",
                height=28,
                fg_color="#1E293B",
                hover_color=m_col,
                font=ctk.CTkFont(size=11, weight="bold"),
                command=lambda k=m_key: self.show_page(k)
            )
            c_btn.pack(fill="x", padx=14, pady=(0, 12))

    def create_metric_card(self, parent, col, title, value, accent):
        card = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        card.grid(row=0, column=col, padx=6, pady=6, sticky="nsew")

        lbl_t = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color=self.colors["text_muted"])
        lbl_t.pack(anchor="w", padx=14, pady=(12, 4))

        lbl_v = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=accent)
        lbl_v.pack(anchor="w", padx=14, pady=(0, 10))

        bar = ctk.CTkProgressBar(card, height=6, progress_color=accent, fg_color="#1E293B")
        bar.set(0.0)
        bar.pack(fill="x", padx=14, pady=(0, 12))
        return {"label": lbl_v, "bar": bar}

    def start_telemetry_loop(self):
        def _poll():
            if not getattr(self, "is_authenticated", False):
                return
            try:
                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory().percent
                disk = psutil.disk_usage("C:\\" if os.name == "nt" else "/").percent
                self.root.after(0, lambda: self._update_metrics(cpu, ram, disk))
            except Exception:
                pass
            self.root.after(2500, self.start_telemetry_loop)

        threading.Thread(target=_poll, daemon=True).start()

    def _update_metrics(self, cpu, ram, disk):
        if hasattr(self, "cpu_card") and self.cpu_card:
            self.cpu_card["label"].configure(text=f"{cpu:.1f}%")
            self.cpu_card["bar"].set(cpu / 100.0)
            self.ram_card["label"].configure(text=f"{ram:.1f}%")
            self.ram_card["bar"].set(ram / 100.0)
            self.disk_card["label"].configure(text=f"{disk:.1f}%")
            self.disk_card["bar"].set(disk / 100.0)

    # --------------------------------------------------------------------------
    # REQUIREMENT 2: FILE & FOLDER AUTOMATION TOOL
    # --------------------------------------------------------------------------

    def build_file_auto_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="📁 File & Folder Automation Tool", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["accent_cyan"])
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Create, read, write, and append files with automated directory categorization by file extensions.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        # Section 1: File Operations Card
        file_card = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        file_card.pack(fill="x", pady=6)

        ctk.CTkLabel(file_card, text="FILE OPERATIONS (CREATE / READ / WRITE)", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["accent_cyan"]).pack(anchor="w", padx=16, pady=(12, 6))

        row1 = ctk.CTkFrame(file_card, fg_color="transparent")
        row1.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(row1, text="Target File:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 8))
        self.fa_filepath_entry = ctk.CTkEntry(row1, placeholder_text="e.g., sample.txt", width=340)
        self.fa_filepath_entry.insert(0, os.path.join(BASE_DIR, "sample_test.txt"))
        self.fa_filepath_entry.pack(side="left", padx=4, fill="x", expand=True)

        browse_btn = ctk.CTkButton(row1, text="📂 Browse", width=80, fg_color="#334155", hover_color="#475569", command=self._browse_fa_file)
        browse_btn.pack(side="left", padx=4)

        self.fa_mode_combo = ctk.CTkComboBox(row1, values=["Read File", "Create File", "Write (Overwrite)", "Append to File"], width=160)
        self.fa_mode_combo.pack(side="left", padx=4)

        # File Content Input/Preview Textbox
        self.fa_content_box = ctk.CTkTextbox(file_card, height=90, font=ctk.CTkFont(family="Consolas", size=11))
        self.fa_content_box.pack(fill="x", padx=16, pady=6)
        self.fa_content_box.insert("1.0", "Hello from CyberPulse Security Toolkit!\nAutomated file handling demonstration.")

        btn_bar = ctk.CTkFrame(file_card, fg_color="transparent")
        btn_bar.pack(fill="x", padx=16, pady=(4, 12))

        exec_btn = ctk.CTkButton(btn_bar, text="▶ Execute File Action", width=170, fg_color=self.colors["accent_blue"], hover_color="#1D4ED8", font=ctk.CTkFont(weight="bold"), command=self.run_file_operation)
        exec_btn.pack(side="left")

        # Section 2: Folder Organizer Card
        folder_card = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        folder_card.pack(fill="x", pady=6)

        ctk.CTkLabel(folder_card, text="DIRECTORY ORGANIZER (AUTOMATIC EXTENSION SORTING)", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["accent_cyan"]).pack(anchor="w", padx=16, pady=(12, 6))

        row2 = ctk.CTkFrame(folder_card, fg_color="transparent")
        row2.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(row2, text="Folder Path:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 8))
        self.fa_folder_entry = ctk.CTkEntry(row2, placeholder_text="Select directory to organize...", width=380)
        self.fa_folder_entry.insert(0, BASE_DIR)
        self.fa_folder_entry.pack(side="left", padx=4, fill="x", expand=True)

        browse_dir_btn = ctk.CTkButton(row2, text="📁 Browse Folder", width=120, fg_color="#334155", hover_color="#475569", command=self._browse_fa_folder)
        browse_dir_btn.pack(side="left", padx=4)

        org_btn = ctk.CTkButton(folder_card, text="⚡ Organize Directory by Extensions", width=240, fg_color=self.colors["accent_green"], hover_color="#059669", font=ctk.CTkFont(weight="bold"), command=self.run_folder_organizer)
        org_btn.pack(anchor="w", padx=16, pady=(6, 14))

        self.fa_console = self.create_console_card(parent, height=190)

    def _browse_fa_file(self):
        f = filedialog.askopenfilename(initialdir=BASE_DIR, title="Select File")
        if f:
            self.fa_filepath_entry.delete(0, "end")
            self.fa_filepath_entry.insert(0, f)

    def _browse_fa_folder(self):
        d = filedialog.askdirectory(initialdir=BASE_DIR, title="Select Directory to Organize")
        if d:
            self.fa_folder_entry.delete(0, "end")
            self.fa_folder_entry.insert(0, d)

    def run_file_operation(self):
        path = self.fa_filepath_entry.get().strip()
        mode = self.fa_mode_combo.get()
        content = self.fa_content_box.get("1.0", "end-1c")

        if not path:
            messagebox.showwarning("Input Required", "Please specify a file path.")
            return

        if mode == "Create File":
            success, msg = self.file_tool.create_file(path, content)
            self.log_to_box(self.fa_console, f"[{'SUCCESS' if success else 'ERROR'}] {msg}")
            if success:
                self.report.add_result("File Automation", path, "File created", severity="INFO")

        elif mode == "Read File":
            success, msg = self.file_tool.read_file(path)
            if success:
                self.fa_content_box.delete("1.0", "end")
                self.fa_content_box.insert("1.0", msg)
                self.log_to_box(self.fa_console, f"[SUCCESS] Read {len(msg)} characters from: {path}")
                self.report.add_result("File Automation", path, f"File read ({len(msg)} chars)", severity="INFO")
            else:
                self.log_to_box(self.fa_console, f"[ERROR] Failed to read file: {msg}")

        elif mode in ["Write (Overwrite)", "Append to File"]:
            write_mode = "w" if "Overwrite" in mode else "a"
            success, msg = self.file_tool.write_file(path, content, mode=write_mode)
            self.log_to_box(self.fa_console, f"[{'SUCCESS' if success else 'ERROR'}] {msg}")
            if success:
                self.report.add_result("File Automation", path, f"File written ({write_mode})", severity="INFO")

    def run_folder_organizer(self):
        folder = self.fa_folder_entry.get().strip()
        if not folder or not os.path.exists(folder):
            messagebox.showwarning("Directory Missing", "Please select a valid directory.")
            return

        confirm = messagebox.askyesno("Confirm Organization", f"Are you sure you want to organize files in:\n{folder}\ninto category subfolders?")
        if not confirm:
            return

        success, msg, items = self.file_tool.organize_folder(folder)
        self.log_to_box(self.fa_console, f"[{'SUCCESS' if success else 'ERROR'}] {msg}")
        for filename, cat in items:
            self.log_to_box(self.fa_console, f"  ↳ Moved '{filename}' -> [{cat}/]")
        if success:
            self.report.add_result("File Automation", folder, f"Organized {len(items)} files", severity="COMPLETED")

    # --------------------------------------------------------------------------
    # REQUIREMENT 3: HASHING & ENCRYPTION UTILITIES
    # --------------------------------------------------------------------------

    def build_crypto_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="🔒 Hashing & Encryption Utilities", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["accent_green"])
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="MD5 and SHA-256 cryptographic hashing alongside Fernet AES-256 symmetric file encryption.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        ctrl = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        ctrl.pack(fill="x", pady=6)

        # Hashing Sub-Section
        ctk.CTkLabel(ctrl, text="CRYPTOGRAPHIC HASHING (MD5 / SHA-256)", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["accent_cyan"]).pack(anchor="w", padx=16, pady=(12, 6))

        h_grid = ctk.CTkFrame(ctrl, fg_color="transparent")
        h_grid.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(h_grid, text="Input String / File:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.crypto_hash_input = ctk.CTkEntry(h_grid, width=320, placeholder_text="Type text to hash OR select a file...")
        self.crypto_hash_input.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        self.crypto_hash_algo = ctk.CTkComboBox(h_grid, values=["SHA-256", "MD5"], width=110)
        self.crypto_hash_algo.grid(row=0, column=2, sticky="w", padx=4, pady=4)

        hash_btn = ctk.CTkButton(h_grid, text="⚡ Calculate Hash", width=140, fg_color=self.colors["accent_cyan"], text_color="#000", hover_color="#38BDF8", font=ctk.CTkFont(weight="bold"), command=self.calculate_hash_action)
        hash_btn.grid(row=0, column=3, sticky="w", padx=4, pady=4)

        self.crypto_hash_output = ctk.CTkEntry(ctrl, font=ctk.CTkFont(family="Consolas", size=12), justify="center", height=36)
        self.crypto_hash_output.pack(fill="x", padx=16, pady=(4, 10))

        # Fernet File Encryption Sub-Section
        divider = ctk.CTkFrame(ctrl, height=1, fg_color=self.colors["card_border"])
        divider.pack(fill="x", padx=14, pady=6)

        ctk.CTkLabel(ctrl, text="FERNET SYMMETRIC FILE ENCRYPTION (AES-256)", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["accent_green"]).pack(anchor="w", padx=16, pady=(8, 6))

        f_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        f_row.pack(fill="x", padx=16, pady=4)

        ctk.CTkLabel(f_row, text="Target File:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 8))
        self.crypto_file_entry = ctk.CTkEntry(f_row, width=360, placeholder_text="Select file path...")
        self.crypto_file_entry.pack(side="left", padx=4, fill="x", expand=True)

        browse_file_btn = ctk.CTkButton(f_row, text="📂 Browse", width=80, fg_color="#334155", hover_color="#475569", command=self.browse_crypto_file)
        browse_file_btn.pack(side="left", padx=4)

        btn_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(8, 14))

        enc_btn = ctk.CTkButton(btn_row, text="🔒 Encrypt File", width=140, fg_color=self.colors["accent_green"], hover_color="#059669", font=ctk.CTkFont(weight="bold"), command=self.encrypt_file_action)
        enc_btn.pack(side="left", padx=4)

        dec_btn = ctk.CTkButton(btn_row, text="🔓 Decrypt File", width=140, fg_color=self.colors["accent_blue"], hover_color="#1D4ED8", font=ctk.CTkFont(weight="bold"), command=self.decrypt_file_action)
        dec_btn.pack(side="left", padx=4)

        self.crypto_console = self.create_console_card(parent, height=200)

    def calculate_hash_action(self):
        val = self.crypto_hash_input.get().strip()
        algo = self.crypto_hash_algo.get().lower()

        if not val:
            messagebox.showwarning("Input Required", "Enter text or select a file to hash.")
            return

        # Check if input is a valid file
        if os.path.exists(val) and os.path.isfile(val):
            try:
                digest = self.crypto_tool.hash_file(val, algorithm=algo)
                self.crypto_hash_output.delete(0, "end")
                self.crypto_hash_output.insert(0, digest)
                self.log_to_box(self.crypto_console, f"[{algo.upper()}] File Hash: {digest} ({val})")
                self.report.add_result("Hashing Utility", os.path.basename(val), f"{algo.upper()}: {digest}", severity="INFO")
            except Exception as e:
                self.log_to_box(self.crypto_console, f"Error hashing file: {e}")
        else:
            digest = self.crypto_tool.hash_text(val, algorithm=algo)
            self.crypto_hash_output.delete(0, "end")
            self.crypto_hash_output.insert(0, digest)
            self.log_to_box(self.crypto_console, f"[{algo.upper()}] Text Hash: {digest}")
            self.report.add_result("Hashing Utility", f"Text: {val[:20]}", f"{algo.upper()}: {digest}", severity="INFO")

    def browse_crypto_file(self):
        f = filedialog.askopenfilename(initialdir=BASE_DIR, title="Select File to Encrypt or Decrypt")
        if f:
            self.crypto_file_entry.delete(0, "end")
            self.crypto_file_entry.insert(0, f)

    def encrypt_file_action(self):
        fname = self.crypto_file_entry.get().strip()
        if not fname or not os.path.exists(fname):
            messagebox.showwarning("File Missing", "Please select a valid existing file.")
            return

        try:
            encryptor = FileEncryptor(fname)
            key = encryptor.encrypt_file()
            self.log_to_box(self.crypto_console, f"🔒 [SUCCESS] Encrypted: {fname}")
            self.log_to_box(self.crypto_console, f"Key Saved in keys.json: {key}")
            self.report.add_result("File Cryptography", fname, "Encrypted with Fernet", severity="ENCRYPTED")
            messagebox.showinfo("Encrypted", "File encrypted successfully!\nKey saved in keys.json.")
        except Exception as e:
            self.log_to_box(self.crypto_console, f"✕ [ERROR] Encryption failed: {e}")
            messagebox.showerror("Error", f"Failed to encrypt file: {e}")

    def decrypt_file_action(self):
        fname = self.crypto_file_entry.get().strip()
        if not fname or not os.path.exists(fname):
            messagebox.showwarning("File Missing", "Please select a valid existing file.")
            return

        try:
            encryptor = FileEncryptor(fname)
            encryptor.decrypt_file()
            self.log_to_box(self.crypto_console, f"🔓 [SUCCESS] Decrypted: {fname}")
            self.report.add_result("File Cryptography", fname, "Decrypted with Fernet", severity="DECRYPTED")
            messagebox.showinfo("Decrypted", "File decrypted successfully back to original plaintext.")
        except Exception as e:
            self.log_to_box(self.crypto_console, f"✕ [ERROR] Decryption failed: {e}")
            messagebox.showerror("Error", f"Failed to decrypt file: {e}")

    # --------------------------------------------------------------------------
    # REQUIREMENT 4: REST API TESTER
    # --------------------------------------------------------------------------

    def build_api_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="🌐 REST API Tester", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["accent_purple"])
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Send GET and POST requests, inspect HTTP headers, response latency, and formatted JSON data.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        ctrl = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        ctrl.pack(fill="x", pady=6)

        c_grid = ctk.CTkFrame(ctrl, fg_color="transparent")
        c_grid.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(c_grid, text="Method:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.api_method_combo = ctk.CTkComboBox(c_grid, values=["GET", "POST"], width=100)
        self.api_method_combo.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ctk.CTkLabel(c_grid, text="Endpoint URL:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=8, pady=4)
        self.api_url_entry = ctk.CTkEntry(c_grid, width=380, placeholder_text="https://jsonplaceholder.typicode.com/posts/1")
        self.api_url_entry.insert(0, "https://jsonplaceholder.typicode.com/posts/1")
        self.api_url_entry.grid(row=0, column=3, sticky="w", padx=4, pady=4)

        send_btn = ctk.CTkButton(c_grid, text="▶ Send Request", width=140, fg_color=self.colors["accent_purple"], hover_color="#7C3AED", font=ctk.CTkFont(weight="bold"), command=self.send_api_request)
        send_btn.grid(row=0, column=4, sticky="w", padx=8, pady=4)

        # POST Body Entry
        body_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        body_row.pack(fill="x", padx=16, pady=(0, 10))

        ctk.CTkLabel(body_row, text="JSON Payload (for POST):", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0, 2))
        self.api_body_entry = ctk.CTkEntry(body_row, placeholder_text='{"title": "Test Title", "body": "CyberPulse Payload", "userId": 1}')
        self.api_body_entry.pack(fill="x")

        # Status Bar
        status_bar = ctk.CTkFrame(ctrl, fg_color="#1E293B", corner_radius=6)
        status_bar.pack(fill="x", padx=16, pady=(0, 14))

        self.api_status_badge = ctk.CTkLabel(status_bar, text="Status: Ready", font=ctk.CTkFont(weight="bold"), text_color=self.colors["accent_cyan"])
        self.api_status_badge.pack(side="left", padx=12, pady=6)

        self.api_latency_badge = ctk.CTkLabel(status_bar, text="Latency: -- ms", font=ctk.CTkFont(weight="bold"), text_color=self.colors["text_muted"])
        self.api_latency_badge.pack(side="right", padx=12, pady=6)

        # JSON Response Display
        self.api_console = self.create_console_card(parent, height=220)

    def send_api_request(self):
        url = self.api_url_entry.get().strip()
        method = self.api_method_combo.get().strip()
        body = self.api_body_entry.get().strip()

        if not url:
            messagebox.showwarning("Input Required", "Please enter an API URL.")
            return

        self.set_engine_status("API Request", self.colors["accent_purple"])
        self.log_to_box(self.api_console, f"Sending {method} request to: {url}")

        def _worker():
            res = self.api_tool.send_request(url, method=method, body=body)

            def _update_ui():
                if res.get("success"):
                    code = res["status_code"]
                    reason = res.get("status_reason", "")
                    latency = res["elapsed_ms"]
                    badge_color = "#10B981" if code < 400 else "#EF4444"

                    self.api_status_badge.configure(text=f"Status: {code} {reason}", text_color=badge_color)
                    self.api_latency_badge.configure(text=f"Latency: {latency} ms", text_color="#38BDF8")

                    self.log_to_box(self.api_console, f"✓ Response Received ({code} {reason}) in {latency}ms")
                    self.log_to_box(self.api_console, res["text"])
                    self.report.add_result("API Tester", f"{method} {url}", f"Status {code} ({latency}ms)", severity="INFO")
                else:
                    self.api_status_badge.configure(text="Status: Request Failed", text_color="#EF4444")
                    self.log_to_box(self.api_console, f"✕ Error: {res.get('error')}")

                self.set_engine_status("Ready", "#10B981")

            self.root.after(0, _update_ui)

        threading.Thread(target=_worker, daemon=True).start()

    # --------------------------------------------------------------------------
    # REQUIREMENT 5: NETWORKING TOOLS (PORT SCANNER & SUBDOMAIN FINDER)
    # --------------------------------------------------------------------------

    def build_network_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="⚡ Networking Tools (Subdomain & Port Scanner)", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["accent_blue"])
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Enumerate active subdomains with DNS resolution and perform TCP port security scans with banner grabbing.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        ctrl = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        ctrl.pack(fill="x", pady=6)

        c_grid = ctk.CTkFrame(ctrl, fg_color="transparent")
        c_grid.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(c_grid, text="Tool Mode:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.net_mode_combo = ctk.CTkComboBox(
            c_grid,
            values=["Port Scanner", "Subdomain Finder"],
            width=160,
            command=self._on_net_mode_change
        )
        self.net_mode_combo.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        self.net_target_lbl = ctk.CTkLabel(c_grid, text="Target IP / Host:", font=ctk.CTkFont(weight="bold"))
        self.net_target_lbl.grid(row=0, column=2, sticky="w", padx=8, pady=4)

        self.net_target_entry = ctk.CTkEntry(c_grid, width=240, placeholder_text="127.0.0.1 or scanme.nmap.org")
        self.net_target_entry.insert(0, "127.0.0.1")
        self.net_target_entry.grid(row=0, column=3, sticky="w", padx=4, pady=4)

        self.net_preset_combo = ctk.CTkComboBox(
            c_grid,
            values=["Common Services (14 Ports)", "Web (80,443,8080,8443)", "Database (3306,5432,1433,6379)", "Fast 1-100"],
            width=210
        )
        self.net_preset_combo.grid(row=0, column=4, sticky="w", padx=4, pady=4)

        btn_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(4, 14))

        self.net_start_btn = ctk.CTkButton(btn_row, text="▶ Start Scan", width=140, fg_color=self.colors["accent_blue"], hover_color="#1D4ED8", font=ctk.CTkFont(weight="bold"), command=self.start_network_action)
        self.net_start_btn.pack(side="left", padx=4)

        self.net_stop_btn = ctk.CTkButton(btn_row, text="⏹ Stop", width=90, fg_color=self.colors["accent_red"], hover_color="#B91C1C", state="disabled", command=self.stop_current_task)
        self.net_stop_btn.pack(side="left", padx=4)

        self.net_progress = ctk.CTkProgressBar(ctrl, height=8, progress_color=self.colors["accent_blue"])
        self.net_progress.set(0)
        self.net_progress.pack(fill="x", padx=20, pady=(0, 14))

        self.net_console = self.create_console_card(parent, height=220)

    def _on_net_mode_change(self, mode):
        if mode == "Subdomain Finder":
            self.net_target_lbl.configure(text="Domain Name:")
            self.net_target_entry.delete(0, "end")
            self.net_target_entry.insert(0, "google.com")
            self.net_preset_combo.configure(values=["Top 20 Common Subdomains", "Top 50 Subdomains", "Subdomains.txt Wordlist"])
            self.net_preset_combo.set("Top 20 Common Subdomains")
        else:
            self.net_target_lbl.configure(text="Target IP / Host:")
            self.net_target_entry.delete(0, "end")
            self.net_target_entry.insert(0, "127.0.0.1")
            self.net_preset_combo.configure(values=["Common Services (14 Ports)", "Web (80,443,8080,8443)", "Database (3306,5432,1433,6379)", "Fast 1-100"])
            self.net_preset_combo.set("Common Services (14 Ports)")

    def start_network_action(self):
        mode = self.net_mode_combo.get()
        target = self.net_target_entry.get().strip()

        if not target:
            messagebox.showwarning("Input Required", "Please specify a target hostname or IP.")
            return

        self.running_event.set()
        self.net_start_btn.configure(state="disabled")
        self.net_stop_btn.configure(state="normal")
        self.net_progress.set(0)

        if mode == "Subdomain Finder":
            self.set_engine_status("Subdomain Recon", self.colors["accent_cyan"])
            threading.Thread(target=self._run_subdomain_worker, args=(target,), daemon=True).start()
        else:
            self.set_engine_status("Port Audit", self.colors["accent_blue"])
            preset = self.net_preset_combo.get()
            threading.Thread(target=self._run_port_worker, args=(target, preset), daemon=True).start()

    def _run_subdomain_worker(self, domain):
        self.log_to_box(self.net_console, f"Initiating Subdomain Enumeration for: {domain}")
        candidates = ["www", "mail", "ftp", "admin", "webmail", "smtp", "api", "dev", "test", "portal", "cloud", "ns1", "ns2", "vpn", "blog", "app", "secure", "shop", "server", "mx"]

        found = 0
        total = len(candidates)

        for i, sub in enumerate(candidates):
            if not self.running_event.is_set():
                self.log_to_box(self.net_console, "Scan halted by user.")
                break

            host = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(host)
                found += 1
                self.log_to_box(self.net_console, f"✓ [ACTIVE] {host:<24} -> IP: {ip}")
                self.report.add_result("Subdomain Finder", host, f"Resolved IP: {ip}", severity="ACTIVE")
            except Exception:
                pass

            prog = (i + 1) / total
            self.root.after(0, lambda p=prog: self.net_progress.set(p))
            time.sleep(0.04)

        self.log_to_box(self.net_console, f"\nEnumeration Complete! Discovered {found} active subdomains.")
        self.report.add_result("Subdomain Finder", domain, f"Complete: {found} active hosts found", severity="COMPLETED")

        def _cleanup():
            self.net_start_btn.configure(state="normal")
            self.net_stop_btn.configure(state="disabled")
            self.set_engine_status("Ready", "#10B981")
        self.root.after(0, _cleanup)

    def _run_port_worker(self, target, preset):
        services = {21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 135: "MS-RPC", 143: "IMAP", 443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy"}

        if "Common" in preset:
            ports = [21, 22, 23, 25, 53, 80, 110, 135, 143, 443, 445, 3306, 3389, 8080]
        elif "Web" in preset:
            ports = [80, 443, 8000, 8080, 8443]
        elif "Database" in preset:
            ports = [1433, 1521, 3306, 5432, 6379, 27017]
        else:
            ports = list(range(1, 101))

        self.log_to_box(self.net_console, f"Initiating TCP Connect Scan on {target} ({len(ports)} ports)")

        try:
            ip = socket.gethostbyname(target)
            self.log_to_box(self.net_console, f"Resolved target to: {ip}")
        except Exception:
            ip = target

        open_ports = []
        total = len(ports)

        for i, port in enumerate(ports):
            if not self.running_event.is_set():
                self.log_to_box(self.net_console, "Scan halted by user.")
                break

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.35)
            res = s.connect_ex((ip, port))
            s.close()

            if res == 0:
                open_ports.append(port)
                svc = services.get(port, "Unknown")
                self.log_to_box(self.net_console, f"★ [OPEN] Port {port:<5}/TCP -> Service: {svc}")
                self.report.add_result("Port Scanner", f"{target}:{port}", f"OPEN ({svc})", severity="OPEN")

            prog = (i + 1) / total
            self.root.after(0, lambda p=prog: self.net_progress.set(p))

        self.log_to_box(self.net_console, f"\nScan Complete! Found {len(open_ports)} open ports.")
        self.report.add_result("Port Scanner", target, f"Completed: {len(open_ports)} open ports", severity="COMPLETED")

        def _cleanup():
            self.net_start_btn.configure(state="normal")
            self.net_stop_btn.configure(state="disabled")
            self.set_engine_status("Ready", "#10B981")
        self.root.after(0, _cleanup)

    # --------------------------------------------------------------------------
    # REQUIREMENT 6: WORDLIST BRUTE-FORCE SIMULATOR
    # --------------------------------------------------------------------------

    def build_password_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="🔑 Wordlist Brute-Force Simulator & Password Strength", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["accent_amber"])
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Offline & safe dictionary simulation against SHA-256 hashes with real-time complexity evaluation.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        grid_row = ctk.CTkFrame(parent, fg_color="transparent")
        grid_row.pack(fill="x", pady=6)
        grid_row.grid_columnconfigure((0, 1), weight=1)

        # Card 1: Strength Meter
        meter_card = ctk.CTkFrame(grid_row, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        meter_card.grid(row=0, column=0, padx=6, pady=6, sticky="nsew")

        ctk.CTkLabel(meter_card, text="REAL-TIME STRENGTH METER", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["accent_cyan"]).pack(anchor="w", padx=16, pady=(14, 6))

        self.strength_input = ctk.CTkEntry(meter_card, width=280, placeholder_text="Type password to evaluate...", show="*")
        self.strength_input.pack(fill="x", padx=16, pady=6)
        self.strength_input.bind("<KeyRelease>", self.update_password_strength)

        self.strength_bar = ctk.CTkProgressBar(meter_card, height=10, progress_color=self.colors["accent_amber"])
        self.strength_bar.set(0)
        self.strength_bar.pack(fill="x", padx=16, pady=10)

        self.strength_label = ctk.CTkLabel(meter_card, text="Score: 0% | Complexity: None", font=ctk.CTkFont(size=11), text_color=self.colors["text_muted"])
        self.strength_label.pack(anchor="w", padx=16, pady=(0, 14))

        # Card 2: Dictionary Simulator
        crack_card = ctk.CTkFrame(grid_row, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        crack_card.grid(row=0, column=1, padx=6, pady=6, sticky="nsew")

        ctk.CTkLabel(crack_card, text="OFFLINE WORDLIST SIMULATOR", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.colors["accent_amber"]).pack(anchor="w", padx=16, pady=(14, 6))

        c_row = ctk.CTkFrame(crack_card, fg_color="transparent")
        c_row.pack(fill="x", padx=16, pady=4)

        self.crack_target_entry = ctk.CTkEntry(c_row, width=200, placeholder_text="Target: admin123")
        self.crack_target_entry.insert(0, "admin123")
        self.crack_target_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        self.crack_start_btn = ctk.CTkButton(c_row, text="▶ Crack Hash", width=110, fg_color=self.colors["accent_amber"], hover_color="#D97706", font=ctk.CTkFont(weight="bold"), command=self.start_password_crack)
        self.crack_start_btn.pack(side="right")

        self.crack_stats_label = ctk.CTkLabel(crack_card, text="Wordlist: test_pass.txt | SHA-256 Offline Matcher", font=ctk.CTkFont(size=11), text_color=self.colors["text_muted"])
        self.crack_stats_label.pack(anchor="w", padx=16, pady=(6, 14))

        self.password_console = self.create_console_card(parent, height=220)

    def update_password_strength(self, event=None):
        pwd = self.strength_input.get()
        if not pwd:
            self.strength_bar.set(0)
            self.strength_label.configure(text="Score: 0% | Complexity: None", text_color=self.colors["text_muted"])
            return

        score = 0
        if len(pwd) >= 8:
            score += 25
        if len(pwd) >= 12:
            score += 15
        if any(c.isupper() for c in pwd):
            score += 15
        if any(c.islower() for c in pwd):
            score += 15
        if any(c.isdigit() for c in pwd):
            score += 15
        if any(c in string.punctuation for c in pwd):
            score += 15

        score = min(score, 100)
        self.strength_bar.set(score / 100.0)

        if score < 40:
            color = self.colors["accent_red"]
            lvl = "Weak / Vulnerable"
        elif score < 70:
            color = self.colors["accent_amber"]
            lvl = "Moderate / Acceptable"
        else:
            color = self.colors["accent_green"]
            lvl = "Strong / Cryptographic"

        self.strength_bar.configure(progress_color=color)
        self.strength_label.configure(text=f"Score: {score}% | Classification: {lvl}", text_color=color)

    def start_password_crack(self):
        target = self.crack_target_entry.get().strip()
        if not target:
            messagebox.showwarning("Input Required", "Please enter a target password or hash.")
            return

        self.running_event.set()
        self.crack_start_btn.configure(state="disabled")
        self.set_engine_status("Brute-Force", self.colors["accent_amber"])

        threading.Thread(target=self._run_crack_worker, args=(target,), daemon=True).start()

    def _run_crack_worker(self, target):
        # Determine if input is raw password or pre-computed hash
        if len(target) == 64 and all(c in string.hexdigits for c in target):
            target_hash = target.lower()
        else:
            target_hash = hashlib.sha256(target.encode()).hexdigest()

        self.log_to_box(self.password_console, f"Simulating offline dictionary attack against SHA-256 digest: {target_hash}")

        wordlist_path = os.path.join(BASE_DIR, "test_pass.txt")
        candidates = []
        if os.path.exists(wordlist_path):
            with open(wordlist_path, "r", errors="ignore") as f:
                candidates = [line.strip() for line in f if line.strip()]
        else:
            candidates = ["admin", "123456", "password", "root", "admin123", "toor", "test"]

        start_time = time.time()
        matched = False

        for i, word in enumerate(candidates):
            guess_hash = hashlib.sha256(word.encode()).hexdigest()
            self.log_to_box(self.password_console, f"Attempt {i+1:>2}: '{word}' -> Hash: {guess_hash[:16]}...")
            time.sleep(0.02)

            if guess_hash == target_hash:
                matched = True
                elapsed = round(time.time() - start_time, 3)
                self.log_to_box(self.password_console, f"\n🎉 [MATCH FOUND] Password cracked in {elapsed}s!")
                self.log_to_box(self.password_console, f"Plaintext: {word}")
                self.log_to_box(self.password_console, f"Digest:    {guess_hash}")
                self.report.add_result("Password Simulator", target, f"Cracked in {elapsed}s (Word: {word})", severity="VULNERABLE")
                break

        if not matched:
            self.log_to_box(self.password_console, f"\nPassword not matched in dictionary ({len(candidates)} candidates tested).")
            self.report.add_result("Password Simulator", target, "Brute-force exhausted with no match", severity="SAFE")

        def _cleanup():
            self.crack_start_btn.configure(state="normal")
            self.set_engine_status("Ready", "#10B981")
        self.root.after(0, _cleanup)

    # --------------------------------------------------------------------------
    # REQUIREMENT 7: SQL INJECTION TESTER
    # --------------------------------------------------------------------------

    def build_sqli_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="🎯 SQL Injection Vulnerability Auditor", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["accent_red"])
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Automated payload fuzzing to uncover SQL syntax errors, database disclosures, and abnormal responses.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        ctrl = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        ctrl.pack(fill="x", pady=6)

        c_grid = ctk.CTkFrame(ctrl, fg_color="transparent")
        c_grid.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(c_grid, text="Target URL:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.sqli_url_entry = ctk.CTkEntry(c_grid, width=320, placeholder_text="http://testphp.vulnweb.com/artists.php")
        self.sqli_url_entry.insert(0, "http://testphp.vulnweb.com/artists.php")
        self.sqli_url_entry.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        ctk.CTkLabel(c_grid, text="Test Parameter:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=12, pady=6)
        self.sqli_param_entry = ctk.CTkEntry(c_grid, width=160, placeholder_text="artist")
        self.sqli_param_entry.insert(0, "artist")
        self.sqli_param_entry.grid(row=0, column=3, sticky="w", padx=6, pady=6)

        btn_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 14))

        self.sqli_start_btn = ctk.CTkButton(btn_row, text="▶ Start SQLi Audit", width=150, fg_color=self.colors["accent_red"], hover_color="#DC2626", font=ctk.CTkFont(weight="bold"), command=self.start_sqli_test)
        self.sqli_start_btn.pack(side="left", padx=6)

        self.sqli_stop_btn = ctk.CTkButton(btn_row, text="⏹ Stop", width=90, fg_color="#475569", hover_color="#334155", state="disabled", command=self.stop_current_task)
        self.sqli_stop_btn.pack(side="left", padx=6)

        self.sqli_status_badge = ctk.CTkLabel(btn_row, text="STATUS: READY FOR AUDIT", font=ctk.CTkFont(size=11, weight="bold"), text_color=self.colors["text_muted"])
        self.sqli_status_badge.pack(side="right", padx=12)

        self.sqli_progress = ctk.CTkProgressBar(ctrl, height=8, progress_color=self.colors["accent_red"])
        self.sqli_progress.set(0)
        self.sqli_progress.pack(fill="x", padx=22, pady=(0, 14))

        self.sqli_console = self.create_console_card(parent, height=220)

    def start_sqli_test(self):
        url = self.sqli_url_entry.get().strip()
        param = self.sqli_param_entry.get().strip()

        if not url or not param:
            messagebox.showwarning("Input Required", "Target URL and parameter name are both required.")
            return

        self.running_event.set()
        self.sqli_start_btn.configure(state="disabled")
        self.sqli_stop_btn.configure(state="normal")
        self.sqli_progress.set(0)
        self.sqli_status_badge.configure(text="STATUS: RUNNING AUDIT...", text_color=self.colors["accent_red"])
        self.set_engine_status("SQLi Audit", self.colors["accent_red"])

        threading.Thread(target=self._run_sqli_worker, args=(url, param), daemon=True).start()

    def _run_sqli_worker(self, url, param):
        payloads = [
            ("Single Quote Syntax Break", "'"),
            ("Double Quote Syntax Break", "\""),
            ("Boolean Tautology Test 1", "' OR '1'='1"),
            ("Boolean Tautology Test 2", "' OR 1=1 --"),
            ("Admin Comment Bypass", "admin' --"),
            ("Universal Quote Bypass", "\"\""),
            ("Order By Clause Enumeration", "1' ORDER BY 1--"),
            ("Union Select Injection Probe", "1' UNION SELECT NULL--")
        ]

        sql_signatures = ["sql syntax", "invalid query", "mysql", "sql state error", "syntax error", "database error", "unclosed quotation", "unknown column", "odbc", "driver", "postgresql", "sqlite"]

        self.log_to_box(self.sqli_console, f"Launching SQL Injection Audit against {url} [Param: {param}]")
        vulnerable_found = 0
        total = len(payloads)

        for i, (name, payload) in enumerate(payloads):
            if not self.running_event.is_set():
                self.log_to_box(self.sqli_console, "Audit halted by user.")
                break

            try:
                start_t = time.time()
                resp = requests.get(url, params={param: payload}, timeout=4)
                latency = round((time.time() - start_t) * 1000, 1)
                text = resp.text.lower()

                matched = [sig for sig in sql_signatures if sig in text]
                if matched:
                    vulnerable_found += 1
                    msg = f"⚠ [VULNERABLE] Payload: {payload:<20} | Signature: '{matched[0]}' | Status: {resp.status_code} ({latency}ms)"
                    self.log_to_box(self.sqli_console, msg)
                    self.report.add_result("SQLi Audit", f"{url}?{param}={payload}", f"VULNERABLE: Signature '{matched[0]}'", severity="VULNERABLE")
                else:
                    msg = f"✓ [SAFE]       Payload: {payload:<20} | No database errors leaked | Status: {resp.status_code} ({latency}ms)"
                    self.log_to_box(self.sqli_console, msg)

            except Exception as e:
                self.log_to_box(self.sqli_console, f"✕ Request failed for payload '{payload}': {e}")

            prog = (i + 1) / total
            self.root.after(0, lambda p=prog: self.sqli_progress.set(p))
            time.sleep(0.06)

        badge_text = f"COMPLETED: {vulnerable_found} VULNERABILITY SIGNATURES FOUND" if vulnerable_found > 0 else "PASSED: TARGET RESILIENT"
        badge_color = "#EF4444" if vulnerable_found > 0 else "#10B981"
        self.log_to_box(self.sqli_console, f"\nAudit Complete! {vulnerable_found} vulnerabilities identified.")

        def _cleanup():
            self.sqli_status_badge.configure(text=badge_text, text_color=badge_color)
            self.sqli_start_btn.configure(state="normal")
            self.sqli_stop_btn.configure(state="disabled")
            self.set_engine_status("Ready", "#10B981")
        self.root.after(0, _cleanup)

    # --------------------------------------------------------------------------
    # REQUIREMENT 8: SYSTEM LOGGING & SCREENSHOT CAPTURE
    # --------------------------------------------------------------------------

    def build_monitor_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="🖥️ System Logging & Screenshot Capture", font=ctk.CTkFont(size=20, weight="bold"), text_color="#EC4899")
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Automated periodic screen capture, activity event logging, and real-time visual inspection.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        ctrl = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        ctrl.pack(fill="x", pady=6)

        c_grid = ctk.CTkFrame(ctrl, fg_color="transparent")
        c_grid.pack(fill="x", padx=16, pady=16)

        ctk.CTkLabel(c_grid, text="Capture Interval (sec):", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.mon_interval_entry = ctk.CTkEntry(c_grid, width=80)
        self.mon_interval_entry.insert(0, "2")
        self.mon_interval_entry.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        ctk.CTkLabel(c_grid, text="Total Captures:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, sticky="w", padx=12, pady=6)
        self.mon_total_entry = ctk.CTkEntry(c_grid, width=80)
        self.mon_total_entry.insert(0, "4")
        self.mon_total_entry.grid(row=0, column=3, sticky="w", padx=6, pady=6)

        btn_row = ctk.CTkFrame(ctrl, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=(0, 14))

        self.mon_start_btn = ctk.CTkButton(btn_row, text="▶ Start Monitoring", width=150, fg_color="#EC4899", hover_color="#DB2777", font=ctk.CTkFont(weight="bold"), command=self.start_monitoring_action)
        self.mon_start_btn.pack(side="left", padx=6)

        self.mon_stop_btn = ctk.CTkButton(btn_row, text="⏹ Stop", width=90, fg_color=self.colors["accent_red"], hover_color="#DC2626", state="disabled", command=self.stop_current_task)
        self.mon_stop_btn.pack(side="left", padx=6)

        open_folder_btn = ctk.CTkButton(btn_row, text="📁 Open Screenshots Folder", width=180, fg_color="#334155", hover_color="#475569", command=self.open_screenshots_folder)
        open_folder_btn.pack(side="left", padx=6)

        # Split Preview & Stats
        split_card = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        split_card.pack(fill="x", pady=8)

        s_grid = ctk.CTkFrame(split_card, fg_color="transparent")
        s_grid.pack(fill="x", padx=14, pady=12)
        s_grid.grid_columnconfigure((0, 1), weight=1)

        self.thumb_frame = ctk.CTkFrame(s_grid, fg_color="#0B0F19", corner_radius=8, width=320, height=170)
        self.thumb_frame.grid(row=0, column=0, padx=8, pady=4, sticky="nsew")

        self.thumb_label = ctk.CTkLabel(self.thumb_frame, text="Latest Screenshot Preview\n(Awaiting Capture)", text_color=self.colors["text_muted"])
        self.thumb_label.pack(expand=True, padx=8, pady=8)

        info_box = ctk.CTkFrame(s_grid, fg_color="transparent")
        info_box.grid(row=0, column=1, padx=8, pady=4, sticky="nsew")

        self.mon_status_lbl = ctk.CTkLabel(info_box, text="Monitoring Engine: IDLE", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=self.colors["text_light"])
        self.mon_status_lbl.pack(anchor="w", pady=(8, 4))

        self.mon_count_lbl = ctk.CTkLabel(info_box, text="Captured: 0 / 0", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        self.mon_count_lbl.pack(anchor="w", pady=2)

        self.mon_log_lbl = ctk.CTkLabel(info_box, text="Log File: activity_log.txt", font=ctk.CTkFont(size=11), text_color=self.colors["accent_cyan"])
        self.mon_log_lbl.pack(anchor="w", pady=4)

        self.mon_console = self.create_console_card(parent, height=190)

    def open_screenshots_folder(self):
        folder = os.path.join(BASE_DIR, "screenshots")
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        if os.name == "nt":
            os.startfile(folder)

    def start_monitoring_action(self):
        try:
            interval = int(self.mon_interval_entry.get().strip())
            total = int(self.mon_total_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid integers for interval and count.")
            return

        self.running_event.set()
        self.mon_start_btn.configure(state="disabled")
        self.mon_stop_btn.configure(state="normal")
        self.set_engine_status("Activity Surveillance", "#EC4899")

        threading.Thread(target=self._run_monitor_worker, args=(interval, total), daemon=True).start()

    def _run_monitor_worker(self, interval, total):
        logger = ActivityLogger(interval)
        folder = os.path.join(BASE_DIR, "screenshots")
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        self.log_to_box(self.mon_console, f"Monitoring started: capturing {total} frames every {interval}s")

        for i in range(total):
            if not self.running_event.is_set():
                self.log_to_box(self.mon_console, "Monitoring halted by operator.")
                break

            fname = os.path.join(folder, f"screenshot_{int(time.time())}_{i+1}.png")
            try:
                shot = pyautogui.screenshot()
                shot.save(fname)

                logger.log_event(f"Captured: {fname}")
                self.log_to_box(self.mon_console, f"📸 Screenshot {i+1}/{total} saved to {os.path.basename(fname)}")

                self._update_screenshot_thumb(fname)
                self.root.after(0, lambda curr=i+1: self.mon_count_lbl.configure(text=f"Captured: {curr} / {total}"))
            except Exception as e:
                self.log_to_box(self.mon_console, f"✕ Capture error: {e}")

            time.sleep(interval)

        self.log_to_box(self.mon_console, "✓ Activity logging completed.")
        self.report.add_result("Activity Monitor", "Desktop Surveillance", f"Captured {total} frames", severity="COMPLETED")

        def _cleanup():
            self.mon_start_btn.configure(state="normal")
            self.mon_stop_btn.configure(state="disabled")
            self.set_engine_status("Ready", "#10B981")
        self.root.after(0, _cleanup)

    def _update_screenshot_thumb(self, path):
        def _update():
            try:
                img = Image.open(path)
                img.thumbnail((300, 160))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                self.thumb_label.configure(image=ctk_img, text="")
            except Exception:
                pass
        self.root.after(0, _update)

    # --------------------------------------------------------------------------
    # EXECUTIVE AUDIT & EXCEL REPORTS
    # --------------------------------------------------------------------------

    def build_report_page(self, parent):
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        title = ctk.CTkLabel(header, text="📑 Executive Security Reports & Audit Logs", font=ctk.CTkFont(size=20, weight="bold"), text_color=self.colors["accent_amber"])
        title.pack(anchor="w")

        sub = ctk.CTkLabel(header, text="Inspect live audit trail records and export executive-styled Excel workbooks.", font=ctk.CTkFont(size=12), text_color=self.colors["text_muted"])
        sub.pack(anchor="w")

        btn_bar = ctk.CTkFrame(parent, fg_color="transparent")
        btn_bar.pack(fill="x", pady=6)

        export_btn = ctk.CTkButton(btn_bar, text="📊 Export Excel Report (.xlsx)", width=210, fg_color="#059669", hover_color="#047857", font=ctk.CTkFont(weight="bold"), command=self.export_excel_report)
        export_btn.pack(side="left", padx=4)

        open_btn = ctk.CTkButton(btn_bar, text="📂 Open Current Report", width=170, fg_color="#334155", hover_color="#475569", command=self.open_excel_file)
        open_btn.pack(side="left", padx=4)

        refresh_btn = ctk.CTkButton(btn_bar, text="🔄 Refresh View", width=120, fg_color="#1E293B", hover_color="#334155", command=self.refresh_report_table)
        refresh_btn.pack(side="left", padx=4)

        clear_btn = ctk.CTkButton(btn_bar, text="🗑 Clear Records", width=120, fg_color=self.colors["accent_red"], hover_color="#B91C1C", command=self.clear_report_records)
        clear_btn.pack(side="right", padx=4)

        table_card = ctk.CTkFrame(parent, fg_color=self.colors["card_bg"], corner_radius=12, border_width=1, border_color=self.colors["card_border"])
        table_card.pack(fill="both", expand=True, pady=8)

        t_header = ctk.CTkFrame(table_card, fg_color="#1E293B", corner_radius=6)
        t_header.pack(fill="x", padx=10, pady=(10, 4))
        t_header.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        cols = [("#", 30), ("Module", 140), ("Target Asset", 200), ("Severity", 110), ("Timestamp", 140)]
        for idx, (c_name, c_w) in enumerate(cols):
            lbl = ctk.CTkLabel(t_header, text=c_name, font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"), text_color=self.colors["accent_cyan"])
            lbl.grid(row=0, column=idx, padx=6, pady=6, sticky="w")

        self.table_scroll = ctk.CTkScrollableFrame(table_card, fg_color="transparent", height=320)
        self.table_scroll.pack(fill="both", expand=True, padx=8, pady=6)

        self.refresh_report_table()

    def refresh_report_table(self):
        for widget in self.table_scroll.winfo_children():
            widget.destroy()

        if not self.report.records:
            empty_lbl = ctk.CTkLabel(self.table_scroll, text="No audit records captured yet. Execute any tool to generate records.", text_color=self.colors["text_muted"])
            empty_lbl.pack(pady=30)
            return

        sev_colors = {"CRITICAL": "#EF4444", "VULNERABLE": "#EF4444", "WARNING": "#F59E0B", "OPEN": "#10B981", "ACTIVE": "#10B981", "ENCRYPTED": "#38BDF8", "DECRYPTED": "#38BDF8", "INFO": "#94A3B8", "COMPLETED": "#10B981"}

        for rec in reversed(self.report.records):
            row_frame = ctk.CTkFrame(self.table_scroll, fg_color="#111827", corner_radius=6)
            row_frame.pack(fill="x", pady=2)
            row_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

            ctk.CTkLabel(row_frame, text=str(rec["id"]), width=30).grid(row=0, column=0, padx=6, pady=4, sticky="w")
            ctk.CTkLabel(row_frame, text=rec["module"], width=140).grid(row=0, column=1, padx=6, pady=4, sticky="w")
            ctk.CTkLabel(row_frame, text=rec["target"][:30], width=200).grid(row=0, column=2, padx=6, pady=4, sticky="w")

            sev_color = sev_colors.get(rec["severity"], self.colors["text_muted"])
            ctk.CTkLabel(row_frame, text=rec["severity"], width=110, font=ctk.CTkFont(weight="bold"), text_color=sev_color).grid(row=0, column=3, padx=6, pady=4, sticky="w")
            ctk.CTkLabel(row_frame, text=rec["timestamp"], width=140, text_color=self.colors["text_muted"]).grid(row=0, column=4, padx=6, pady=4, sticky="w")

    def export_excel_report(self):
        default_name = f"security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        f = filedialog.asksaveasfilename(initialdir=BASE_DIR, initialfile=default_name, defaultextension=".xlsx", filetypes=[("Excel Workbook", "*.xlsx")])
        if f:
            try:
                self.report.save_report(f)
                res = messagebox.askyesno("Report Exported", f"Excel report generated successfully at:\n{f}\n\nWould you like to open it now?")
                if res and os.name == "nt":
                    os.startfile(f)
            except Exception as e:
                messagebox.showerror("Export Failed", f"Failed to save Excel file: {e}")

    def open_excel_file(self):
        f = os.path.join(BASE_DIR, "security_report.xlsx")
        if os.path.exists(f) and os.name == "nt":
            os.startfile(f)
        else:
            messagebox.showinfo("Report Missing", "No default security_report.xlsx exists yet. Please generate or export one first.")

    def clear_report_records(self):
        self.report.clear()
        self.refresh_report_table()
        messagebox.showinfo("Cleared", "Audit records wiped clean.")


# ==============================================================================
# MAIN APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    root = ctk.CTk()
    app = CyberToolkitGUI(root)
    root.mainloop()