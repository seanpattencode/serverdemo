import sqlite3,sys,time,os;db=sqlite3.connect("m.db");db.execute("CREATE TABLE IF NOT EXISTS c(k,v)");db.execute("CREATE TABLE IF NOT EXISTS l(t,m)")
def rem():r=db.execute("SELECT v FROM c WHERE k='t'").fetchone();s=max(0,float(r[0])-time.time())if r else 0;return f"{int(s//86400)}d {int(s%86400//3600)}h {int(s%3600//60)}m"
if 'set'in sys.argv:db.execute("DELETE FROM c");db.execute("INSERT INTO c VALUES('t',?)",(time.time()+float(sys.argv[2])*86400,));db.commit();print(f"Set: {rem()}")
if 'demo'in sys.argv:[os.system(f"python3 send_email.py msg 'Demo Day {i+1}' '{rem()}'")for i in range(7)]
if 'run'in sys.argv:
 while 1:t=time.time();m=rem();last=db.execute("SELECT m FROM l ORDER BY t DESC LIMIT 1").fetchone();sent=" sent"if time.strftime("%H:%M")=="11:11"and(not last or"sent"not in last[0])and not os.system(f"python3 send_email.py msg 'Refill (v2)' '{m}'")else"";db.execute("INSERT INTO l VALUES(?,?)",(t,m+sent));db.commit();print(f"[{time.strftime('%H:%M:%S')}] {m}{sent}",flush=1);time.sleep(1)
if not sys.argv[1:]or'status'in sys.argv:print(f"{rem()}\nCommands: set <days>|run|demo|status")
