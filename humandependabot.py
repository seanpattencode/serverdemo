#!/usr/bin/env python3
import sqlite3,os,sys,time;from datetime import datetime as D;P=os.path.dirname(os.path.abspath(__file__));DB=sqlite3.connect(f"{P}/hdb.db");DB.executescript("CREATE TABLE IF NOT EXISTS c(k PRIMARY KEY,v);CREATE TABLE IF NOT EXISTS l(t,m)")
T0,SPD=time.time(),float(os.environ.get("SPD",1));now=lambda:T0+(time.time()-T0)*SPD;rem=lambda:(lambda s:f"{int(s//86400)}d {int(s%86400//3600)}h {int(s%3600//60)}m")(max(0,(lambda r:float(r[0])-now()if r else 0)(DB.execute("SELECT v FROM c WHERE k='t'").fetchone())))
on=lambda:"active"in os.popen("systemctl --user is-active 'run-*.service' 2>/dev/null").read();svc=lambda a:os.system(f'systemd-run --user -- {sys.executable} {__file__} run'if a else"systemctl --user stop 'run-*.service' 2>/dev/null");cmd=sys.argv[1]if len(sys.argv)>1 else""
if cmd=="set":DB.execute("REPLACE INTO c VALUES('t',?)",(time.time()+float(sys.argv[2]if len(sys.argv)>2 else input("Days: "))*86400,));DB.commit();w=on();w and(svc(0),svc(1));print(f"Set: {rem()}")
elif cmd=="run":
 while 1:t=now();r=time.time();m=rem();h=D.fromtimestamp(t);sent=" sent"if h.hour==11 and(SPD==1 and h.minute==11 or SPD>1)and not DB.execute("SELECT 1 FROM l WHERE m LIKE'%sent%'AND t>?",(r-43200,)).fetchone()and(SPD>1 or not os.system(f'{sys.executable} {P}/send_email.py msg "Refill (v1)" "{m}"'))else"";DB.execute("INSERT INTO l VALUES(?,?)",(r,m+sent));DB.commit();print(f"[{h:%m-%d %H:%M:%S}] {m}{sent}",flush=1);time.sleep(1/SPD)
elif cmd in("start","stop"):svc(cmd=="start");print("Started"if cmd=="start"else"Stopped")
elif cmd=="log":[print(f"{D.fromtimestamp(t):%m-%d %H:%M:%S} {m}")for t,m in DB.execute("SELECT*FROM l ORDER BY t DESC LIMIT 20")]
else:print(f"[{'ON'if on()else'OFF'}] {rem()}\nCommands: set [days]|start|stop|log  (SPD=N to speed up time N×)")
