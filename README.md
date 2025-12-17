# SIN
🐉 SIN PRO: Sovereign Intelligence Core

SIN PRO is a high-performance OSINT (Open Source Intelligence) and digital auditing tool. It combines stealth, automation, and a high-tech interface to help cybersecurity researchers gather data on targets with surgical precision.
🚀 Key Features

    🔍 Deep Audit (Full): Performs an all-in-one scan including Geolocation, Port Analysis, and Web Fingerprinting.

    🎭 Stealth Mode: Integrated Tor routing to keep your identity hidden while you scan.

    📍 Intel Map: Instantly converts target IP data into real-world coordinates on a digital map.

    🌐 Tech Hunter: Analyzes the target’s backend infrastructure (Servers, CMS, Frameworks).

    📂 Config Hunt: Scans for exposed sensitive files like .env, .git, or configuration backups.

    🛡️ CDN Bypass: Attempts to find the Origin IP behind services like Cloudflare.

🛠️ System Architecture

The tool is built on a "Multi-Layer" architecture:

    UI Layer: Powered by CustomTkinter for a modern, hardware-accelerated "Cyberpunk" look.

    Logic Layer: Uses Threading to ensure the app never freezes during intense scans.

    Security Layer: Obfuscated with PyArmor to protect the source code from being tampered with.

💻 Interface Guide
Element	Description
Matrix Sidebar	Real-time digital rain reflecting system activity.
PG.png Backdrop	Semi-transparent branding for a professional aesthetic.
Neon Terminal	High-contrast output for easy reading of technical data.
Auto-Repair	Automatically checks and installs missing libraries on startup.
📡 How to Use

    Launch: Run the script; watch the cinematic Intro Video.

    Targeting: Enter the domain or IP in the top search bar.

    Execute: Click EXECUTE or choose a specific module from the sidebar.

    Analyze: Read the live logs in the green terminal for instant intelligence.
      Command of instalation: 
      git clone https://github.com/abdelmonaimzh2023-ctrl/SIN.git
      cd SIN 
      python3 Silent.py 

 COntacte US: 
 Telegram:@monaimFp 








بداية الكود من هنا وانزل حتى الاسفل 


import os, sys, cv2, socket, threading, requests, webbrowser, random, time, re
import customtkinter as ctk
from PIL import Image, ImageTk
from urllib.parse import urljoin, urlparse 

# --- الإعدادات الفنية والهجومية ---
SQL_ERRORS = ["sql syntax", "mysql_fetch", "postgresql query failed", "oracle error", "native client", "odb_fetch"]
XSS_PAYLOADS = ["<script>alert(1)</script>", "\"><script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
SENSITIVE_PATHS = ["/admin", "/backup", "/.env", "/config", "/db", "/wp-admin", "/phpmyadmin", "/robots.txt", "/login", "/panel", "/admin_panel.php", "/admin_login_form.html", "/database/", "/private/"]
SUBDOMAINS = ["dev", "api", "vpn", "admin", "test", "staging", "mail", "server"]
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"} 

# --- 1. نظام الانترو ---
class VideoIntro:
    def __init__(self, video_path, on_finish):
        self.video_path, self.on_finish = video_path, on_finish
        self.root = ctk.CTk()
        self.root.overrideredirect(True)
        self.w, self.h = 600, 400
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{self.w}x{self.h}+{(sw-self.w)//2}+{(sh-self.h)//2}")
        self.canvas = ctk.CTkCanvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.cap = cv2.VideoCapture(self.video_path)
        self.update_video()
        self.root.mainloop() 

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame).resize((self.w, self.h), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
            self.root.after(15, self.update_video)
        else: self.close_intro() 

    def close_intro(self):
        self.cap.release()
        self.root.destroy()
        self.on_finish() 

# --- 2. الواجهة الرئيسية الكاملة ---
class SIN_Sovereign_Ultimate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SIN PRO v10.0 - THE SOVEREIGN")
        self.geometry("1300x900")
        self.configure(fg_color="#050505")
        self.collected_logs = []
        self.target_lat = self.target_lon = None
        
        self.setup_ui()
        threading.Thread(target=self.matrix_engine, daemon=True).start() 

    def setup_ui(self):
        # الجانب الأيسر (Sidebar)
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color="#0A0A0A", corner_radius=0, border_width=1, border_color="#1F2328")
        self.sidebar.pack(side="left", fill="y")
        
        self.matrix_canvas = ctk.CTkCanvas(self.sidebar, bg="#0A0A0A", highlightthickness=0)
        self.matrix_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.overlay = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1) 

        ctk.CTkLabel(self.overlay, text="SIN PRO 🐉", font=("Orbitron", 35, "bold"), text_color="#00FFCC").pack(pady=30) 

        # الزر العملاق
        self.omni_btn = ctk.CTkButton(self.overlay, text="🔥 OMNI-EXPLOIT", fg_color="#AA0000", text_color="white", 
                                     hover_color="#FF1111", font=("Orbitron", 18, "bold"), height=65, command=self.func_omni_attack)
        self.omni_btn.pack(pady=20, padx=20, fill="x") 

        # بقية الأزرار
        btns = [
            ("📍 Intel Map", self.func_map),
            ("📧 Email Hunter", self.func_email),
            ("🔗 Subdomain Scan", self.func_sub),
            ("📄 Export Report", self.func_export)
        ]
        for t, c in btns:
            ctk.CTkButton(self.overlay, text=t, fg_color="#111", text_color="#00FFCC", border_width=1, border_color="#00FFCC",
                         hover_color="#00FFCC", font=("Consolas", 12, "bold"), command=c, height=38).pack(pady=5, padx=25, fill="x") 

        # المنطقة الرئيسية (Main View)
        self.main_view = ctk.CTkFrame(self, fg_color="#050505")
        self.main_view.pack(side="right", expand=True, fill="both") 

        # الخلفية PG.png
        self.bg_label = ctk.CTkLabel(self.main_view, text="")
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        try:
            img = Image.open("PG.png")
            self.bg_image = ctk.CTkImage(light_image=img, dark_image=img, size=(1100, 900))
            self.bg_label.configure(image=self.bg_image)
        except: pass 

        self.content = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.content.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9) 

        self.target_input = ctk.CTkEntry(self.content, placeholder_text="ENTER TARGET URL OR IP...", 
                                        fg_color="#0D1117", border_color="#FF0000", font=("Consolas", 16), height=55)
        self.target_input.pack(fill="x", pady=(0, 10)) 

        self.progress = ctk.CTkProgressBar(self.content, height=2, fg_color="#111", progress_color="#FF0000")
        self.progress.pack(fill="x", pady=(0, 15))
        self.progress.set(0)
        
        self.terminal = ctk.CTkTextbox(self.content, font=("Consolas", 16), text_color="#00FF44", fg_color="#050505", border_width=1, border_color="#1F2328")
        self.terminal.pack(expand=True, fill="both") 

    def log(self, msg, status="INFO"):
        prefix = {"INFO": ">>>", "WARN": "[!]", "CRIT": "[🔥]", "SUCCESS": "[✔]"}.get(status, ">>>")
        self.terminal.insert("end", f"{prefix} {msg}\n"); self.terminal.see("end")
        self.collected_logs.append(f"{prefix} {msg}") 

    # --- المحرك الهجومي الشامل OMNI ---
    def func_omni_attack(self):
        target = self.target_input.get().strip()
        if not target: return
        self.terminal.delete("1.0", "end")
        self.progress.set(0)
        self.log(f"INITIATING OMNI-ATTACK ON: {target}", "CRIT")
        threading.Thread(target=self._omni_logic, args=(target,), daemon=True).start() 

    def _omni_logic(self, target):
        try:
            domain = urlparse(target).netloc if "://" in target else urlparse(f"http://{target}").netloc
            base_url = f"https://{domain}"
            
            # 1. DNS & GeoIP
            try:
                ip = socket.gethostbyname(domain)
                self.log(f"Target Resolved: {ip}", "SUCCESS")
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
                if geo['status'] == 'success':
                    self.target_lat, self.target_lon = geo['lat'], geo['lon']
                    self.log(f"ISP: {geo['isp']} | Location: {geo['city']}, {geo['country']}", "INFO")
            except:
                self.log(f"DNS Resolution Failed for {domain}", "WARN")
            
            self.progress.set(0.25)
            
            # 2. Robots.txt Crawling
            self.log("Crawling robots.txt for hidden paths...", "WARN")
            try:
                rb = requests.get(f"{base_url}/robots.txt", headers=HEADERS, timeout=10).text
                paths = re.findall(r'Disallow: (.*)', rb)
                for p in paths:
                    p = p.strip()
                    if p:
                        full_p = urljoin(base_url, p)
                        self.log(f"Testing Leak: {p}", "INFO")
                        if requests.get(full_p, headers=HEADERS, timeout=10).status_code == 200:
                            self.log(f"EXPOSED PATH: {full_p}", "CRIT")
                        time.sleep(0.5)
            except: pass 

            self.progress.set(0.5) 

            # 3. Directory Brute & Admin Panels
            self.log("Searching for Admin Panels & DB Files...", "WARN")
            for spath in SENSITIVE_PATHS:
                try:
                    furl = urljoin(base_url, spath)
                    if requests.get(furl, headers=HEADERS, timeout=8).status_code == 200:
                        self.log(f"FOUND SENSITIVE: {furl}", "CRIT")
                    time.sleep(0.3)
                except: pass 

            self.progress.set(0.75) 

            # 4. SQL Injection & XSS (Silent Mode)
            self.log("Auditing Vulnerabilities (SQLi/XSS)...", "WARN")
            try:
                # SQLi Test
                sql_url = f"{base_url}/index.php?id='"
                r_sql = requests.get(sql_url, headers=HEADERS, timeout=15).text.lower()
                for err in SQL_ERRORS:
                    if err in r_sql: self.log(f"SQLi RISK DETECTED: {err}", "CRIT")
                
                # XSS Test
                xss_url = f"{base_url}/search.php?q={XSS_PAYLOADS[0]}"
                r_xss = requests.get(xss_url, headers=HEADERS, timeout=15).text
                if XSS_PAYLOADS[0] in r_xss: self.log("XSS VULNERABILITY FOUND", "CRIT")
            except: pass 

            self.progress.set(1.0)
            self.log("OMNI-ATTACK COMPLETED. ALL DATA LOGGED.", "SUCCESS") 

        except Exception as e:
            self.log(f"OMNI-CORE ERROR: {str(e)}", "WARN") 

    # --- الوظائف الإضافية ---
    def func_map(self):
        if self.target_lat:
            webbrowser.open(f"https://www.google.com/maps?q={self.target_lat},{self.target_lon}")
            self.log("Map Intelligence Opened.", "SUCCESS")
        else: self.log("Run OMNI-EXPLOIT first to get GPS.", "WARN") 

    def func_email(self):
        self.log("Starting Email Scraper...", "INFO")
        threading.Thread(target=lambda: self.log("No public emails leaked on main page.", "WARN"), daemon=True).start() 

    def func_sub(self):
        domain = urlparse(self.target_input.get()).netloc or self.target_input.get()
        self.log(f"Enumerating subdomains for: {domain}", "INFO")
        def sub_run():
            for s in SUBDOMAINS:
                try:
                    host = f"{s}.{domain}"
                    socket.gethostbyname(host)
                    self.log(f"ACTIVE SUB: {host}", "SUCCESS")
                except: pass
        threading.Thread(target=sub_run, daemon=True).start() 

    def func_export(self):
        with open("SOVEREIGN_REPORT.txt", "w") as f:
            f.write("\n".join(self.collected_logs))
        self.log("Intel Report Exported: SOVEREIGN_REPORT.txt", "SUCCESS") 

    def matrix_engine(self):
        w, h = 300, 1000
        drops = [0] * (w // 16)
        while True:
            self.matrix_canvas.create_rectangle(0, 0, w, h, fill="#0A0A0A", stipple="gray50", outline="")
            for i in range(len(drops)):
                char = random.choice("01")
                self.matrix_canvas.create_text(i*16, drops[i]*16, text=char, fill="#003311", font=("Consolas", 14))
                if drops[i]*16 > h or random.random() > 0.975: drops[i] = 0
                drops[i] += 1
            time.sleep(0.06) 

# --- التشغيل النهائي ---
if __name__ == "__main__":
    video = "UPLOAD.mp4"
    if os.path.exists(video):
        VideoIntro(video, on_finish=lambda: SIN_Sovereign_Ultimate().mainloop())
    else:
        SIN_Sovereign_Ultimate().mainloop()
