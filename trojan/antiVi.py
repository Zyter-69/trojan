import tkinter as tk
from tkinter import ttk, messagebox

class AtarBalsAntivirus:
    def __init__(self, root):

        self.root = root
        self.root.title("AtarBals Morden Antivirus")
        self.root.geometry("1100x700")
        self.root.minsize(900, 550)
        self.root.configure(bg="#f4f7fc")
        self.root.iconphoto(True, tk.PhotoImage(file="./src/icon.png"))

        # Configure main grid
        self.root.columnconfigure(0, minsize=240)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, minsize=45)

        # Sidebar
        self.sidebar = tk.Frame(self.root, bg="#2d5be3")
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.build_sidebar()

        # Main
        self.main = tk.Frame(self.root, bg="white")
        self.main.grid(row=0, column=1, sticky="nsew", padx=(20, 20), pady=(20, 10))
        self.main.columnconfigure(0, weight=3)
        self.main.columnconfigure(1, weight=1)
        self.main.rowconfigure(2, weight=1)

        self.build_main_content()

        # Footer
        self.build_footer()

    def build_sidebar(self):
        tk.Label(
            self.sidebar,
            text="AntiVirus",
            font=("Segoe UI", 16, "bold"),
            bg="#2d5be3",
            fg="white",
            pady=25
        ).pack()

        nav_items = [
            ("Status", "🟢"),
            ("Updates", "🔄"),
            ("Settings", "⚙️"),
            ("Share Feedback", "💬"),
            ("Buy Premium", "🛒"),
            ("Help", "❓")
        ]

        for name, icon in nav_items:
            btn = tk.Label(
                self.sidebar,
                text=f"  {icon}  {name}",
                font=("Segoe UI", 11, "bold"),
                bg="#2d5be3",
                fg="white",
                pady=10,
                padx=15,
                anchor="w",
                cursor="hand2"
            )
            btn.pack(fill="x", pady=1)
            btn.bind("<Button-1>", lambda e, i=name: self.nav_click(i))
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#2449b5"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2d5be3"))

        tk.Button(
            self.sidebar,
            text="Scan Now",
            font=("Segoe UI", 12, "bold"),
            bg="#00bcd4",
            fg="white",
            activebackground="#0097a7",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            relief="flat",
            command=self.scan_now
        ).pack(side="bottom", pady=30, padx=20, fill="x")

    def build_main_content(self):
        # Top section
        top = tk.Frame(self.main, bg="white")
        top.grid(row=0, column=0, columnspan=2, sticky="we", pady=(10, 20))
        top.columnconfigure(1, weight=1)

        canvas = tk.Canvas(top, width=120, height=120, bg="white", highlightthickness=0)
        canvas.grid(row=0, column=0, sticky="w", padx=(0, 20))
        canvas.create_oval(10, 10, 110, 110, fill="#108710", outline="")
        canvas.create_line(40, 70, 60, 90, fill="white", width=8)
        canvas.create_line(60, 90, 100, 50, fill="white", width=8)

        tk.Label(
            top,
            text="Your System is Protected",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#2e2e2e",
            anchor="w"
        ).grid(row=0, column=1, sticky="w")

        # Protection summary
        summary = tk.Frame(self.main, bg="white")
        summary.grid(row=1, column=0, columnspan=2, sticky="we", pady=(0, 15))
        summary.columnconfigure(0, weight=1)
        summary.columnconfigure(1, weight=0)

        self.protection_label = tk.Label(summary, text="Protection: Excellent", font=("Segoe UI", 11, "bold"), bg="white")
        self.protection_label.grid(row=0, column=0, sticky="w")


        # --- LEFT COLUMN: Features ---
        features_frame = tk.Frame(self.main, bg="white")
        features_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10))
        features_frame.columnconfigure((0, 1), weight=1)

        features = [
            ("Malware Protection", True),
            ("Web Protection", True),
            ("Ransomware Protection", False),
            ("Privacy Protection", False),
            ("Malicious Traffic Detection", False)
        ]
        self.feature_labels = {}
        for i, (name, enabled) in enumerate(features):
            r, c = divmod(i, 2)
            card = tk.Frame(features_frame, bg="#fafafa", bd=1, relief="solid")
            card.grid(row=r, column=c, padx=10, pady=8, sticky="we")
            tk.Label(card, text=f"🛡️  {name}", font=("Segoe UI", 11, "bold"), bg="#fafafa", anchor="w").pack(anchor="w", padx=10, pady=(6, 0))
            status = tk.Label(card, text="Enabled" if enabled else "Upgrade to Premium to Enable",
                              font=("Segoe UI", 9), bg="#fafafa", fg=("green" if enabled else "gray"))
            status.pack(anchor="w", padx=25, pady=(4, 8))
            self.feature_labels[name] = status

        # License box
        self.license_card = tk.Frame(self.main, bg="#fafafa", bd=2, relief="flat")
        self.license_card.grid(row=3, column=2, sticky="we", pady=(0, 15))
        tk.Label(self.license_card, text="Enter License:", font=("Segoe UI", 10, "bold"), bg="#fafafa").pack(anchor="w", padx=10, pady=(8, 4))
        self.license_inner = tk.Frame(self.license_card, bg="#fafafa")
        self.license_inner.pack(anchor="w", padx=10, pady=(0, 10))
        self.license_entry = tk.Entry(self.license_inner, font=("Segoe UI", 10), width=10, relief="solid", bd=1)
        self.license_entry.pack(side="left")
        tk.Button(self.license_inner, text="Submit", font=("Segoe UI", 10, "bold"),
                  bg="#2196F3", fg="white", bd=0, padx=10, pady=4, cursor="hand2",
                  command=self.submit_license).pack(side="left", padx=(8, 0))

        # Promo area
        promo = tk.Frame(self.main, bg="#eaf5ff", bd=1, relief="solid")
        promo.grid(row=3, column=0, columnspan=2, sticky="we", pady=(10, 0))
        self.promo1 = tk.Label(promo, text="Upgrade to Premium, increase your security",
                 font=("Segoe UI", 12, "bold"), bg="#eaf5ff", fg="#2d5be3")
        self.promo1.pack(padx=10, pady=(4, 2))
        self.promo2 = tk.Label(promo, text="Advanced ransomware protection, exploit prevention, and more.",
                 font=("Segoe UI", 10), bg="#eaf5ff")
        self.promo2.pack(padx=10, pady=(0, 8))

    def build_footer(self):   
        self.footer = tk.Frame(self.root, bg="#ff9800", height=45)
        self.footer.grid(row=1, column=0, columnspan=2, sticky="we")
        self.footer.grid_propagate(False)

        tk.Label(
            self.footer,
            text="Upgrade to Premium for Complete Protection",
            font=("Segoe UI", 10, "bold"),
            bg="#ff9800",
            fg="white"
        ).pack(side="left", padx=15)
        tk.Label(
            self.footer,
            text="Unlock ransomware protection, exploit prevention, and advanced web filtering.",
            font=("Segoe UI", 9),
            bg="#ff9800",
            fg="white"
        ).pack(side="left", padx=(5, 0))
        tk.Button(
            self.footer,
            text="Upgrade Now",
            font=("Segoe UI", 10, "bold"),
            bg="#f57c00",
            fg="white",
            activebackground="#e65100",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=5,
            cursor="hand2",
            relief="flat",
        ).pack(side="right", padx=20)

    def nav_click(self, item):
        messagebox.showinfo("Navigation", f"{item} ")

    def scan_now(self):
        messagebox.showinfo("Scan", "Scanning...")
        messagebox.showinfo("Scan", "Scan Completed. No threats found :)")

    def submit_license(self):
        key = self.license_entry.get().strip()
        if key=="abdou chikouri":
            messagebox.showinfo("License", f"License submitted: {key}")
            for k, v in self.feature_labels.items():
                if "Ransomware" in k or "Privacy" in k or "Malicious" in k:
                    v.config(text="Enabled", fg="green")
            self.protection_label.config(text="Protection: Excellent (Premium)")
            self.license_card.grid_forget()
            self.footer.grid_forget()
            self.promo1.config(text="Subcribed to Premuim!", fg="#108710")
            self.promo2.config(text="You now have full protection.", fg="#108710")
            
        else:
            messagebox.showwarning("License", "Please enter a valid license key!")

if __name__ == "__main__":
    root = tk.Tk()
    app = AtarBalsAntivirus(root)
    root.mainloop()
