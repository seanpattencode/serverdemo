#!/usr/bin/env python3
import sqlite3,sys,time,os;P=os.path.dirname(os.path.abspath(__file__));db=sqlite3.connect(f"{P}/m.db");db.executescript("CREATE TABLE IF NOT EXISTS c(k PRIMARY KEY,v);CREATE TABLE IF NOT EXISTS l(t,m)")
def rem():r=db.execute("SELECT v FROM c WHERE k='t'").fetchone();s=max(0,float(r[0])-time.time())if r else 0;return f"{int(s//86400)}d {int(s%86400//3600)}h {int(s%3600//60)}m"
on=lambda:"active"in os.popen("systemctl --user is-active 'run-*.service' 2>/dev/null").read();svc=lambda a:os.system(f'systemd-run --user -- {sys.executable} {__file__} run'if a else"systemctl --user stop 'run-*.service' 2>/dev/null");cmd=sys.argv[1]if len(sys.argv)>1 else""
if cmd=="set":db.execute("REPLACE INTO c VALUES('t',?)",(time.time()+float(sys.argv[2]if len(sys.argv)>2 else input("Days: "))*86400,));db.commit();w=on();w and(svc(0),svc(1));print(f"Set: {rem()}")
elif cmd=="demo":[print(f"[Day {i+1}] {rem()}"+" sent"*(not os.system(f'{sys.executable} {P}/send_email.py msg "Refill (v2) Day {i+1}" "{rem()}"')))for i in range(7)]
elif cmd=="run":
 while 1:t=time.time();m=rem();sent=" sent"if time.strftime("%H:%M")=="11:11"and not db.execute("SELECT 1 FROM l WHERE m LIKE'%sent%'AND t>?",(t-43200,)).fetchone()and not os.system(f'{sys.executable} {P}/send_email.py msg "Refill (v2)" "{m}"')else"";db.execute("INSERT INTO l VALUES(?,?)",(t,m+sent));db.commit();print(f"[{time.strftime('%H:%M:%S')}] {m}{sent}",flush=1);time.sleep(1)
elif cmd in("start","stop"):svc(cmd=="start");print("Started"if cmd=="start"else"Stopped")
else:print(f"[{'ON'if on()else'OFF'}] {rem()}\nCommands: set [days]|start|stop|run|demo")
