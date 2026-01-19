import sqlite3,os,sys,time;p=os.path.dirname(os.path.abspath(__file__));d=sqlite3.connect(f"{p}/hdb.db");d.execute("CREATE TABLE IF NOT EXISTS c(k,v)");d.execute("CREATE TABLE IF NOT EXISTS l(t,m)")
def cnt():t=d.execute("SELECT v FROM c WHERE k='t'").fetchone();r=max(0,float(t[0])-time.time())if t else 0;return f"{int(r//86400)}d {int(r%86400//3600)}h {int(r%3600//60)}m {int(r%60)}s"
if 'set'in sys.argv:d.execute("DELETE FROM c");d.execute("INSERT INTO c VALUES('t',?)",(time.time()+float(input("Days until refill: "))*86400,));d.commit();was_on=not os.popen("systemctl --user is-active 'run-*.service' 2>/dev/null").read().strip().find("active");os.system("systemctl --user stop 'run-*.service' 2>/dev/null");was_on and os.system(f'systemd-run --user -- {sys.executable} {os.path.abspath(__file__)} run >/dev/null 2>&1');exit(print(f"Set: {cnt()}{' (restarted)'if was_on else''}"))
if 'run'in sys.argv:
 while 1:m=cnt();d.execute("INSERT INTO l VALUES(?,?)",(time.time(),m));d.commit();a="sent"if time.strftime("%H:%M:%S")=="11:11:00"and not os.system(f'{sys.executable} {p}/send_email.py msg "Nootropic Refill" "{m}"')else"";print(m,a);time.sleep(1)
if 'start'in sys.argv:os.system(f'systemd-run --user -- {sys.executable} {os.path.abspath(__file__)} run');exit(print("Started"))
if 'stop'in sys.argv:os.system("systemctl --user stop 'run-*.service'");exit(print("Stopped"))
if 'log'in sys.argv:[print(time.strftime("%H:%M:%S",time.localtime(r[0])),r[1])for r in d.execute("SELECT*FROM l ORDER BY t DESC LIMIT 10")];exit()
if 'status'in sys.argv:exit(print("Refill in: "+cnt()))
run="ON"if not os.popen("systemctl --user is-active 'run-*.service' 2>/dev/null").read().strip().find("active")else"OFF";last=d.execute("SELECT t,m FROM l WHERE m LIKE '%sent%' ORDER BY t DESC LIMIT 1").fetchone();print(f"[{run}] {cnt()} | Last sent: {time.strftime('%Y-%m-%d %H:%M',time.localtime(last[0]))+' '+last[1].split()[0]if last else'never'}\nUsage: set|start|stop|log|status")
