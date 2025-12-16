import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import time

# --- City to TZ Database + Fallback offsets ---
CITY_ZONES = {
    "london":"Europe/London","paris":"Europe/Paris","berlin":"Europe/Berlin",
    "rome":"Europe/Rome","dubai":"Asia/Dubai","delhi":"Asia/Kolkata",
    "mumbai":"Asia/Kolkata","bengaluru":"Asia/Kolkata","tokyo":"Asia/Tokyo",
    "seoul":"Asia/Seoul","singapore":"Asia/Singapore","sydney":"Australia/Sydney",
    "cape town":"Africa/Johannesburg","moscow":"Europe/Moscow",
    "new york":"America/New_York","toronto":"America/Toronto",
    "los angeles":"America/Los_Angeles","rio":"America/Sao_Paulo",
    "hong kong":"Asia/Hong_Kong","istanbul":"Europe/Istanbul"
}
FALLBACK = {
    "Europe/London":0,"Europe/Paris":1,"Europe/Berlin":1,"Europe/Rome":1,
    "Asia/Dubai":4,"Asia/Kolkata":5.5,"Asia/Tokyo":9,"Asia/Seoul":9,
    "Asia/Singapore":8,"Australia/Sydney":11,"Africa/Johannesburg":2,
    "Europe/Moscow":3,"America/New_York":-5,"America/Toronto":-5,
    "America/Los_Angeles":-8,"America/Sao_Paulo":-3,"Asia/Hong_Kong":8,
    "Europe/Istanbul":3
}

# --- Small helper functions ---
def parse_date(s):
    for f in ["%d-%m-%Y","%Y-%m-%d","%d/%m/%Y"]:
        try: return datetime.strptime(s.strip(),f).date()
        except: pass
    raise ValueError("Use DD-MM-YYYY")

def parse_dt(s):
    for f in ["%d-%m-%Y %H:%M","%d-%m-%Y %H:%M:%S"]:
        try: return datetime.strptime(s.strip(),f)
        except: pass
    raise ValueError("Use DD-MM-YYYY HH:MM")

def age_calc(dob,a=None):
    if a is None: a=date.today()
    y=a.year-dob.year; m=a.month-dob.month; d=a.day-dob.day
    if d<0: m-=1; d+=(a.replace(day=1)-timedelta(days=1)).day
    if m<0: y-=1; m+=12
    return y,m,d

# --- Circular Timer Ring ---
class Ring(ttk.Frame):
    def __init__(self,p):
        super().__init__(p)
        self.c=tk.Canvas(self,width=160,height=160,bg="#FAFAFF",highlightthickness=0)
        self.c.pack()
        self.arc=self.c.create_arc(10,10,150,150,start=90,extent=0,style="arc",
                                   width=12,outline="#8B5CF6")
        self.txt=self.c.create_text(80,80,text="00:00",
                    font=("Segoe UI",13,"bold"),fill="#4B5563")
        self.total=0; self.rem=0; self.run=False
    def start(self,s):
        self.total=s; self.rem=s; self.run=True; self.tick()
    def tick(self):
        if not self.run: return
        m,sc=divmod(self.rem,60)
        self.c.itemconfig(self.txt,text=f"{m:02d}:{sc:02d}")
        self.c.itemconfig(self.arc,extent=-360*(1-self.rem/self.total))
        if self.rem==0:
            self.run=False; messagebox.showinfo("Timer","Time’s up!"); return
        self.rem-=1; self.after(1000,self.tick)
    def reset(self):
        self.run=False
        self.c.itemconfig(self.arc,extent=0)
        self.c.itemconfig(self.txt,text="00:00")

# --- MAIN APP ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Universal Date & Time Utility")
        self.geometry("760x520")
        self.configure(bg="#EDE9FE")

        style=ttk.Style()
        style.configure("Card.TFrame",background="#FFFFFF")
        style.configure("TLabel",background="#FFFFFF")

        nb=ttk.Notebook(self)
        nb.pack(fill="both",expand=True,padx=20,pady=20)

        # --- DAY TAB ---
        day=self.tab(nb,"Day Finder")
        self.d_e=self.entry(day,"Enter date (DD-MM-YYYY):")
        self.d_l=self.result(day)
        ttk.Button(day,text="Find Day",command=self.do_day).pack(pady=5)

        # --- AGE TAB ---
        age=self.tab(nb,"Age Calculator")
        self.a_e=self.entry(age,"Enter birthdate:")
        self.a_l=self.result(age)
        ttk.Button(age,text="Compute Age",command=self.do_age).pack()

        # --- COUNTDOWN TAB ---
        cd=self.tab(nb,"Countdown Timer")
        self.ev_name=self.entry(cd,"Event Name:")
        self.c_e=self.entry(cd,"Event Date (DD-MM-YYYY HH:MM):")
        self.c_l=self.result(cd)
        ttk.Button(cd,text="Show Remaining",command=self.do_cd).pack()

        # --- TIMER + STOPWATCH ---
        ti=self.tab(nb,"Timer & Stopwatch")
        self.ring=Ring(ti); self.ring.pack(pady=10)

        f=ttk.Frame(ti,style="Card.TFrame"); f.pack()
        ttk.Label(f,text="Min:").grid(row=0,column=0); self.tm=ttk.Entry(f,width=5); self.tm.grid(row=0,column=1)
        ttk.Label(f,text="Sec:").grid(row=0,column=2); self.ts=ttk.Entry(f,width=5); self.ts.grid(row=0,column=3)
        ttk.Button(f,text="Start",command=self.start_timer).grid(row=0,column=4,padx=5)
        ttk.Button(f,text="Reset",command=self.ring.reset).grid(row=0,column=5)

        sw=ttk.Frame(ti,style="Card.TFrame"); sw.pack(pady=10)
        self.sw_lbl=ttk.Label(sw,text="00:00:00",font=("Segoe UI",12,"bold"),
                              background="#FFFFFF")
        self.sw_lbl.pack()
        ttk.Button(sw,text="Start",command=self.sw_start).pack(side="left",padx=5)
        ttk.Button(sw,text="Stop",command=self.sw_stop).pack(side="left",padx=5)
        ttk.Button(sw,text="Reset",command=self.sw_reset).pack(side="left",padx=5)
        self.sw_run=False; self.start_t=0; self.elapsed=0

        # --- WORLD CLOCK ---
        wc=self.tab(nb,"World Clock")
        self.w_e=self.entry(wc,"Enter City (e.g. Tokyo):")
        self.w_l=self.result(wc)
        ttk.Button(wc,text="Show Time",command=self.do_wc).pack()

    # ---- UI helpers ----
    def tab(self,nb,title):
        f=ttk.Frame(nb,style="Card.TFrame")
        nb.add(f,text=title)
        ttk.Label(f,text=title,font=("Segoe UI",11,"bold")).pack(pady=8)
        return f
    def entry(self,p,label):
        ttk.Label(p,text=label).pack(pady=4)
        e=ttk.Entry(p); e.pack(pady=4)
        return e
    def result(self,p):
        l=ttk.Label(p,text="",font=("Segoe UI",12,"bold"))
        l.pack(pady=8)
        return l

    # ---- Feature Logic ----
    def do_day(self):
        try:
            d=parse_date(self.d_e.get())
            self.d_l.config(text=d.strftime("%A"))
        except Exception as e: messagebox.showerror("Error",str(e))

    def do_age(self):
        try:
            y,m,d=age_calc(parse_date(self.a_e.get()))
            self.a_l.config(text=f"{y}y {m}m {d}d")
        except Exception as e: messagebox.showerror("Error",str(e))

    def do_cd(self):
        try:
            name=self.ev_name.get().strip() or "Event"
            t=parse_dt(self.c_e.get())
            diff=t-datetime.now()
            if diff.total_seconds()<0:
                self.c_l.config(text=f"{name} already passed."); return
            ds=diff.days; h,s=divmod(diff.seconds,3600); m,s=divmod(s,60)
            self.c_l.config(text=f"Time left for {name}:\n{ds}d {h:02d}:{m:02d}:{s:02d}")
        except Exception as e: messagebox.showerror("Error",str(e))

    def start_timer(self):
        try:
            sec=int(self.tm.get())*60+int(self.ts.get())
            if sec<=0: raise ValueError
            self.ring.start(sec)
        except: messagebox.showerror("Error","Invalid time")

    # Stopwatch
    def sw_start(self):
        if not self.sw_run:
            self.sw_run=True
            self.start_t=time.time()-self.elapsed
            self.update_sw()
    def sw_stop(self):
        if self.sw_run:
            self.sw_run=False
            self.elapsed=time.time()-self.start_t
    def sw_reset(self):
        self.sw_run=False; self.elapsed=0
        self.sw_lbl.config(text="00:00:00")
    def update_sw(self):
        e=time.time()-self.start_t if self.sw_run else self.elapsed
        h=int(e//3600); m=int((e%3600)//60); s=int(e%60)
        self.sw_lbl.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        if self.sw_run: self.after(200,self.update_sw)

    # ---- City-Based World Clock ----
    def do_wc(self):
        city=self.w_e.get().strip().lower()
        if city not in CITY_ZONES:
            messagebox.showerror("Error","City not in database"); return
        tz=CITY_ZONES[city]
        try:
            from zoneinfo import ZoneInfo
            now=datetime.now(ZoneInfo(tz))
        except:
            now=datetime.utcnow()+timedelta(hours=FALLBACK.get(tz,0))
        self.w_l.config(text=now.strftime("%d-%m-%Y %H:%M:%S"))

App().mainloop()