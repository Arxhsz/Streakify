#!/usr/bin/env python3
import os
import sys
import re
import time
import random
import threading
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import ctypes
import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# ——————————————————————————————————————————————
# Ensure Windows uses our .ico for the taskbar, not python.exe’s icon
APPID = "com.Arxhsz.streakrestore"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APPID)
# ——————————————————————————————————————————————

# Helper to locate bundled resources under PyInstaller
def resource_path(rel_path):
    base = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base, rel_path)

# Prevent destructor errors
uc.Chrome.__del__ = lambda self: None

# Filenames of your icons
ICO_NAME  = "icon.ico"   # Windows taskbar icon (must be .ico)
LOGO_NAME = "logo.png"   # PNG used for PhotoImage

# Constants
FORM_URL = (
    "https://help.snapchat.com/hc/en-us/requests/new?co=true&"
    "ticket_form_id=149423"
)
FIELD_MAP = {
    "request_custom_fields_24281229": "Username",
    "request_custom_fields_24335325": "Email",
    "request_custom_fields_24369716": "Phone",
    "request_custom_fields_24369736": "Friend's Username",
}
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.(com|net|org|co|io|us|gov)$", re.IGNORECASE)
PHONE_REGEX = re.compile(r"^\d{10}$")

# Secondary monitor defaults
win_x, win_y, win_w, win_h = 1920, 0, 1024, 768

# Colors
GREY        = "#D3D3D3"
BUTTON_GREY = "#717171"

# — Automation Helpers — #

def human_typing(el, text):
    for ch in text:
        el.send_keys(ch)
        time.sleep(random.uniform(0.1, 0.25))
    time.sleep(random.uniform(0.2, 0.4))

def human_pause(a=0.5, b=1.2):
    time.sleep(random.uniform(a, b))

def fill_field(driver, wait, fid, val, log):
    label = FIELD_MAP.get(fid, fid)
    log(f"Filling {label}…")
    el = wait.until(EC.presence_of_element_located((By.ID, fid)))
    ActionChains(driver).move_to_element(el).pause(0.2).click().perform()
    human_typing(el, val)
    errs = driver.find_elements(By.CSS_SELECTOR, ".errors-list__item")
    if errs:
        raise ValueError(errs[0].text)
    human_pause()

def restore_flow(user, email, phone, friend, log):
    log("Launching browser…")
    options = uc.ChromeOptions()
    options.add_argument("--disable-background-timer-throttling")
    options.add_argument("--disable-backgrounding-occluded-windows")
    options.add_argument("--disable-renderer-backgrounding")
    options.add_argument(f"--window-position={win_x},{win_y}")
    options.add_argument(f"--window-size={win_w},{win_h}")
    driver = uc.Chrome(options=options)
    try:
        driver.get("https://help.snapchat.com/hc/en-us")
        time.sleep(1)
        driver.add_cookie({
            "name":   "sc-cookies-accepted",
            "value":  "true",
            "domain": "help.snapchat.com",
            "path":   "/"
        })
        wait = WebDriverWait(driver, 20)
        driver.get(FORM_URL)

        # Corrected field IDs including friend's username
        fields = [
            ("request_custom_fields_24281229", user),     # Username
            ("request_custom_fields_24335325", email),    # Email
            ("request_custom_fields_24369716", phone),    # Phone
            ("request_custom_fields_24369736", friend),   # Friend's Username
        ]
        random.shuffle(fields)
        for fid, val in fields:
            fill_field(driver, wait, fid, val, log)

        log("Submitting form…")
        human_pause(1.5, 2.5)
        btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "input[type='submit'][name='commit']"
        )))
        ActionChains(driver).move_to_element(btn).click().perform()

        WebDriverWait(driver, 15).until(
            lambda d: "/hc/en-us/p/success" in d.current_url
                      or d.find_elements(By.CSS_SELECTOR, ".errors-list__item")
        )

        if "/hc/en-us/p/success" in driver.current_url:
            log("✅ Success!")
            messagebox.showinfo("Success", "Ticket submitted successfully.")
        else:
            errs = driver.find_elements(By.CSS_SELECTOR, ".errors-list__item")
            raise ValueError(errs[0].text if errs else "Unknown error")
    except Exception as e:
        log(f"❌ {e}")
        messagebox.showerror("Error", str(e))
    finally:
        driver.quit()

# — GUI Helpers — #

def append_log(msg):
    ts = time.strftime("%H:%M:%S")
    log_area.configure(state="normal")
    log_area.insert("end", f"[{ts}] {msg}\n")
    log_area.see("end")
    log_area.configure(state="disabled")

def validate_inputs(u, e, p, f):
    if len(u) < 3:
        return "Username must be 3 characters"
    if len(f) < 3:
        return "Friend's username must be 3 characters"
    if not EMAIL_REGEX.match(e):
        return "Invalid email"
    if not PHONE_REGEX.match(p):
        return "Phone must be 10 digits"
    return None

def on_restore():
    u, e, p, f = (
        e_user.get().strip(),
        e_email.get().strip(),
        e_phone.get().strip(),
        e_friend.get().strip()
    )
    err = validate_inputs(u, e, p, f)
    if err:
        messagebox.showwarning("Validation", err)
        return

    for w in (e_user, e_email, e_phone, e_friend, btn_restore, btn_clear):
        w.config(state="disabled")
    progress.start(12)
    append_log("Starting restore…")

    def task():
        try:
            restore_flow(u, e, p, f, append_log)
        finally:
            progress.stop()
            for w in (e_user, e_email, e_phone, e_friend, btn_restore, btn_clear):
                w.config(state="normal")
    threading.Thread(target=task, daemon=True).start()

def on_clear():
    for ent in (e_user, e_email, e_phone, e_friend):
        ent.delete(0, "end")
    log_area.configure(state="normal")
    log_area.delete("1.0", "end")
    log_area.configure(state="disabled")

def open_settings():
    def save():
        global win_x, win_y, win_w, win_h
        try:
            win_x = int(sx.get()); win_y = int(sy.get())
            win_w = int(sw.get()); win_h = int(sh.get())
            settings.destroy()
        except ValueError:
            messagebox.showwarning("Invalid", "Enter integers only")

    settings = tk.Toplevel(root)
    settings.title("Settings")
    settings.configure(bg=GREY)
    settings.attributes("-toolwindow", True)
    settings.resizable(False, False)

    labels = [
        ("X position", win_x),
        ("Y position", win_y),
        ("Width", win_w),
        ("Height", win_h),
    ]
    vars_ = {}
    for i, (lab, val) in enumerate(labels):
        ttk.Label(settings, text=f"{lab}:", background=GREY, foreground="#000", font=("Segoe UI",10))\
            .grid(row=i, column=0, sticky="e", padx=10, pady=6)
        var = tk.StringVar(value=str(val)); vars_[lab] = var
        ttk.Entry(settings, textvariable=var, width=8)\
            .grid(row=i, column=1, padx=10, pady=6)
    sx, sy, sw, sh = (
        vars_["X position"],
        vars_["Y position"],
        vars_["Width"],
        vars_["Height"]
    )

    ttk.Separator(settings).grid(row=4, columnspan=2, sticky="ew", pady=8)

    save_btn = ttk.Button(settings, text="Save", style="Save.TButton", command=save)
    save_btn.grid(row=5, column=0, columnspan=2, pady=10)

# — Build GUI — #

root = tk.Tk()

# Load taskbar icon (will work from disk or bundled exe)
try:
    root.iconbitmap(resource_path(ICO_NAME))
except Exception:
    pass

# Load PNG iconphoto (disk or bundled)
try:
    logo_img = tk.PhotoImage(file=resource_path(LOGO_NAME))
    root.iconphoto(False, logo_img)
except Exception:
    pass

root.title("Snapchat Streak Restore")
root.configure(bg=GREY)
root.geometry("560x620")
root.resizable(False, False)

# Menu
menubar = tk.Menu(root, background=GREY, foreground="#000", tearoff=0)
settings_menu = tk.Menu(menubar, tearoff=0, background=GREY, foreground="#000")
settings_menu.add_command(label="Window Position/Size…", command=open_settings)
menubar.add_cascade(label="Settings", menu=settings_menu)
root.config(menu=menubar)

# Styles
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TFrame", background=GREY)
style.configure("TLabelframe", background=GREY)
style.configure("TLabel", background=GREY, foreground="#000", font=("Segoe UI",11))
style.configure("TEntry", fieldbackground=GREY, foreground="#000", font=("Segoe UI",11))
style.configure("TButton", background=GREY, foreground="#000", font=("Segoe UI",12,"bold"), padding=8)
style.map("TButton", background=[("active","#CCCCCC")], relief=[("pressed","sunken"),("!pressed","flat")])
style.configure("Restore.TButton", background=BUTTON_GREY, foreground="#fff")
style.map("Restore.TButton", background=[("active",BUTTON_GREY)])
style.configure("Clear.TButton", background=BUTTON_GREY, foreground="#fff")
style.map("Clear.TButton", background=[("active",BUTTON_GREY)])
style.configure("Save.TButton", background=BUTTON_GREY, foreground="#fff")
style.map("Save.TButton", background=[("active",BUTTON_GREY)])

# Header spacer
ttk.Frame(root, height=10, style="TFrame").pack(fill="x")

# Input section
group = ttk.LabelFrame(root, text="Account Details", padding=(20,10), style="TLabelframe")
group.pack(fill="x", padx=20, pady=(0,10))
labels = ["Snapchat Username","Email","Phone Number","Friend's Username"]
entries = []
for i, txt in enumerate(labels):
    ttk.Label(group, text=f"{txt}:", style="TLabel").grid(row=i, column=0, sticky="w", pady=6)
    ent = ttk.Entry(group)
    ent.grid(row=i, column=1, sticky="ew", pady=6, padx=(10,0))
    entries.append(ent)
group.columnconfigure(1, weight=1)
e_user, e_email, e_phone, e_friend = entries

# Buttons
btn_frame = ttk.Frame(root, padding=(20,0))
btn_frame.pack(fill="x")
btn_restore = ttk.Button(btn_frame, text="Restore Streak", command=on_restore, style="Restore.TButton")
btn_restore.pack(side="left", expand=True, fill="x", padx=(0,10))
btn_clear   = ttk.Button(btn_frame, text="Clear", command=on_clear, style="Clear.TButton")
btn_clear.pack(side="left", expand=True, fill="x")

# Progress & log
progress = ttk.Progressbar(root, mode="indeterminate", style="TProgressbar")
progress.pack(fill="x", padx=20, pady=(10,5))
log_area = scrolledtext.ScrolledText(root, height=12, state="disabled", bg=GREY, fg="#000", font=("Consolas",10), insertbackground="#000")
log_area.pack(fill="both", expand=True, padx=20, pady=(0,20))

# Bind Enter
root.bind("<Return>", lambda e: on_restore())

root.mainloop()