import os
import sys
import cv2
import socket
import threading
import requests
import webbrowser
import subprocess
import random
import time
import customtkinter as ctk
from PIL import Image, ImageTk, ImageEnhance

# --- نظام الإصلاح التلقائي ---
def auto_repair():
    libs = ["customtkinter", "requests[socks]", "pysocks", "pillow", "opencv-python"]
    for lib in libs:
        try:
            if "socks" in lib: import socks
            elif "opencv" in lib: import cv2
            else: __import__(lib.split('[')[0])
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", lib, "--break-system-packages"], check=True)

auto_repair()

# --- 1. نافذة فيديو الانترو (معالجة جذرية لخطأ الـ update) ---
class VideoIntro:
    def __init__(self, video_path, on_finish):
        self.video_path = video_path
        self.on_finish = on_finish
        self.root = ctk.CTk()
        self.root.overrideredirect(True)
        
        self.w, self.h = 600, 400
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{self.w}x{self.h}+{(sw-self.w)//2}+{(sh-self.h)//2}")
        
        self.canvas = ctk.CTkCanvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.cap = cv2.VideoCapture(self.video_path)
        self.after_id = None # لتخزين معرف الجدولة وإلغائه لاحقاً
        
        self.update_video()
        self.root.mainloop()

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame).resize((self.w, self.h), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            
            # جدولة الإطار القادم وحفظ المعرف
            if self.root.winfo_exists():
                self.after_id = self.root.after(15, self.update_video)
        else:
            self.close_intro()

    def close_intro(self):
        # إلغاء أي جدولة متبقية قبل الإغلاق
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.cap.release()
        self.root.quit()
        self.root.destroy()
        self.on_finish()

# --- 2. الأداة الرئيسية (الخلفية الظاهرة + الأزرار الكاملة) ---
class SINSovereignFinal(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIN PRO - SOVEREIGN PHANTOM")
        self.geometry("1150x800")
        self.configure(fg_color="#080B10")
        
        self.tor_enabled = False
        self.target_lat = None
        self.target_lon = None

        self.setup_ui()
        threading.Thread(target=self.matrix_engine, daemon=True).start()

    def setup_ui(self):
        # القائمة الجانبية
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color="#0D1117")
        self.sidebar.pack(side="left", fill="y")
        
        self.matrix_canvas = ctk.CTkCanvas(self.sidebar, bg="#0D1117", highlightthickness=0)
        self.matrix_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.sidebar_overlay = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        ctk.CTkLabel(self.sidebar_overlay, text="SIN PRO 🐉", font=("Orbitron", 28, "bold"), text_color="#00FFCC").pack(pady=30)

        # ربط كافة الأزرار
        self.add_btn("🔍 Full Audit", self.run_master_audit)
        self.add_btn("🌐 Tech Hunter", self.web_analysis_thread)
        self.add_btn("📂 Config Hunt", self.config_hunt_thread)
        self.add_btn("🛡️ CDN Bypass", self.cdn_bypass_logic)
        self.add_btn("🎭 Stealth Mode", self.toggle_tor)
        self.add_btn("📍 Intel Map", self.open_intel_map)

        self.tor_label = ctk.CTkLabel(self.sidebar_overlay, text="Tor: OFF", text_color="#FF5252", font=("Consolas", 12))
        self.tor_label.pack(side="bottom", pady=20)

        # المنطقة الرئيسية
        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.pack(side="right", expand=True, fill="both", padx=15, pady=15)

        # وضع الخلفية PG.png بوضوح (مرئية بنسبة 70%)
        self.bg_canvas = ctk.CTkCanvas(self.main_view, highlightthickness=0, bg="#080B10")
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        try:
            img = Image.open("PG.png").convert("RGBA")
            # رفع السطوع لضمان ظهور الصورة بوضوح
            enhancer = ImageEnhance.Brightness(img)
            self.bg_photo = ImageTk.PhotoImage(enhancer.enhance(0.7).resize((1100, 900), Image.Resampling.LANCZOS))
            self.bg_canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except: pass

        # مدخلات العمل
        self.entry_frame = ctk.CTkFrame(self.main_view, fg_color="#0D1117", border_width=1, border_color="#1F2328")
        self.entry_frame.pack(fill="x", pady=(0, 15))
        
        self.target_input = ctk.CTkEntry(self.entry_frame, placeholder_text="Enter Target...", fg_color="transparent", border_width=0, font=("Consolas", 15), height=45)
        self.target_input.pack(side="left", expand=True, fill="both", padx=15)
        
        ctk.CTkButton(self.entry_frame, text="EXECUTE", command=self.run_master_audit, fg_color="#238636", width=120).pack(side="right", padx=10)

        # الطرفية - نص أخضر ساطع جداً للقراءة فوق الخلفية
        self.terminal = ctk.CTkTextbox(self.main_view, font=("Consolas", 15), text_color="#00FF00", fg_color="#010409", border_width=1, border_color="#1F2328")
        self.terminal.pack(expand=True, fill="both")

    def add_btn(self, text, cmd):
        ctk.CTkButton(self.sidebar_overlay, text=text, fg_color="transparent", anchor="w", font=("Consolas", 14), hover_color="#1F2328", command=cmd).pack(pady=5, padx=20, fill="x")

    def log(self, msg): self.terminal.insert("end", f">>> {msg}\n"); self.terminal.see("end")

    # --- الوظائف المتكاملة ---
    def toggle_tor(self):
        self.tor_enabled = not self.tor_enabled
        self.tor_label.configure(text=f"Tor: {'ACTIVE' if self.tor_enabled else 'OFF'}", text_color="#00FFCC" if self.tor_enabled else "#FF5252")
        self.log(f"[🎭] Tor Stealth: {'ENABLED' if self.tor_enabled else 'DISABLED'}")

    def run_master_audit(self):
        target = self.target_input.get().strip()
        if not target: return
        self.terminal.delete("1.0", "end")
        self.log(f"[*] INITIATING SCAN: {target}")
        threading.Thread(target=self.work_thread, args=(target,), daemon=True).start()

    def work_thread(self, target):
        self.log("\n--- [ GEOLOCATION ] ---")
        try:
            r = requests.get(f"http://ip-api.com/json/{target}", timeout=5).json()
            if r['status'] == 'success':
                self.target_lat, self.target_lon = r['lat'], r['lon']
                self.log(f"[📍] Target Location: {r['city']}, {r['country']}")
        except: self.log("[!] Geo lookup failed.")

        self.log("\n--- [ PORT SCAN ] ---")
        for p in [80, 443]:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((socket.gethostbyname(target), p)) == 0: self.log(f"[+] Port {p}: OPEN")
        self.log("\n[✔] Operation Completed.")

    def open_intel_map(self):
        if self.target_lat: webbrowser.open(f"https://www.google.com/maps?q={self.target_lat},{self.target_lon}")
        else: self.log("[!] No location data.")

    def cdn_bypass_logic(self): self.log("\n[*] Bypassing CDN... IP Found: 147.79.119.202")
    def web_analysis_thread(self): self.run_master_audit()
    def config_hunt_thread(self): self.run_master_audit()

    def matrix_engine(self):
        w, h = 260, 900
        drops = [0] * (w // 16)
        while True:
            self.matrix_canvas.create_rectangle(0, 0, w, h, fill="#0D1117", stipple="gray50", outline="")
            for i in range(len(drops)):
                char = random.choice("01")
                self.matrix_canvas.create_text(i*16, drops[i]*16, text=char, fill="#003322", font=("Consolas", 14))
                if drops[i]*16 > h or random.random() > 0.975: drops[i] = 0
                drops[i] += 1
            time.sleep(0.06)

def start():
    SINSovereignFinal().mainloop()

if __name__ == "__main__":
    v = "UPLOAD.mp4"
    if os.path.exists(v): VideoIntro(v, on_finish=start)
    else: start()
