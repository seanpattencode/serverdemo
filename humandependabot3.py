#!/usr/bin/env python3
import sqlite3,sys,time,os,subprocess
P=os.path.dirname(os.path.abspath(__file__));db=sqlite3.connect(f"{P}/hdb3.db");db.executescript("CREATE TABLE IF NOT EXISTS c(k PRIMARY KEY,v);CREATE TABLE IF NOT EXISTS l(t,m)")
def rem():r=db.execute("SELECT v FROM c WHERE k='t'").fetchone();s=max(0,float(r[0])-time.time())if r else 0;return f"{int(s//86400)}d {int(s%86400//3600)}h {int(s%3600//60)}m"
def weather():
 try:r=subprocess.run(['claude','-p','--allowedTools','WebSearch'],input='NYC weather in 10 words or less',capture_output=True,text=True,timeout=30);return r.stdout.strip()if r.returncode==0 else"weather unavailable"
 except:return"weather unavailable"
U=os.path.expanduser("~/.config/systemd/user");SVC="hdb3";on=lambda:os.popen(f"systemctl --user is-active {SVC}.service 2>/dev/null").read().strip()=="active"
auto=lambda:os.popen(f"systemctl --user is-enabled {SVC}.timer 2>/dev/null").read().strip()=="enabled"
def install():
 os.makedirs(U,exist_ok=True);open(f"{U}/{SVC}.service","w").write(f"[Service]\nExecStart={sys.executable} {__file__} run\nRestart=on-failure\n");open(f"{U}/{SVC}.timer","w").write(f"[Timer]\nOnBootSec=1min\nOnCalendar=*:0/5\nPersistent=true\n[Install]\nWantedBy=timers.target\n")
 os.system(f"systemctl --user daemon-reload && systemctl --user enable --now {SVC}.service {SVC}.timer");print("Installed")
cmd=sys.argv[1]if len(sys.argv)>1 else""
if cmd=="set":db.execute("REPLACE INTO c VALUES('t',?)",(time.time()+float(sys.argv[2]if len(sys.argv)>2 else input("Days: "))*86400,));db.commit();on()and os.system(f"systemctl --user restart {SVC}.service");print(f"Set: {rem()}")
elif cmd=="run":
 while 1:t=time.time();m=rem();w=weather()if time.strftime("%H:%M")=="08:00"else"";sent=" sent"if time.strftime("%H:%M")=="08:00"and not db.execute("SELECT 1 FROM l WHERE m LIKE'%sent%'AND t>?",(t-43200,)).fetchone()and not os.system(f'{sys.executable} {P}/send_email.py msg "Refill (v3)" "{m} | NYC: {w}"')else"";db.execute("INSERT INTO l VALUES(?,?)",(t,m+sent));db.commit();print(f"[{time.strftime('%H:%M:%S')}] {m}{' | '+w if w else''}{sent}",flush=1);time.sleep(1)
elif cmd=="install":install()
elif cmd=="uninstall":os.system(f"systemctl --user disable --now {SVC}.service {SVC}.timer 2>/dev/null");print("Uninstalled")
elif cmd in("start","stop"):os.system(f"systemctl --user {cmd} {SVC}.service");print("Started"if cmd=="start"else"Stopped")
else:print(f"[{'ON'if on()else'OFF'}] [Auto:{'Y'if auto()else'N'}] {rem()}\nset|start|stop|install|uninstall")
