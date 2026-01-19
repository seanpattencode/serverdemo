import sqlite3, time, threading, sys, os
conn = sqlite3.connect("times.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS logs(timestamp TEXT)")
if "install" in sys.argv: os.system(f"(crontab -l 2>/dev/null; echo '@reboot cd {os.getcwd()} && python3 {__file__} daemon') | crontab -"); print("Installed"); exit()
if "daemon" in sys.argv: exec("while True: conn.execute('INSERT INTO logs VALUES(?)', (time.strftime('%Y-%m-%d %H:%M:%S'),)); conn.commit(); time.sleep(1)")
print(f"TIME LOGGER | Entries: {conn.execute('SELECT COUNT(*) FROM logs').fetchone()[0]} | Last: {conn.execute('SELECT MAX(timestamp) FROM logs').fetchone()[0] or 'None'} | Type 'exit' to stop")
def log():
    while True: t=time.strftime("%Y-%m-%d %H:%M:%S"); conn.execute("INSERT INTO logs VALUES(?)",(t,)); conn.commit(); print(f"[{t}] Logged"); time.sleep(1)
threading.Thread(target=log, daemon=True).start()
while input() != "exit": pass
