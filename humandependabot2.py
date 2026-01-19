smtplib,sqlite3,EmailMessage,sys,time,os=__import__('smtplib'),__import__('sqlite3'),__import__('email.message',fromlist=['EmailMessage']).EmailMessage,__import__('sys'),__import__('time'),__import__('os')
db=sqlite3.connect("m.db");db.execute("PRAGMA journal_mode=WAL");db.execute("CREATE TABLE IF NOT EXISTS l(t)");med=sys.argv[2] if len(sys.argv)>2 else "11:11"
if 'setup' in sys.argv: open('/etc/systemd/system/med.service','w').write(f"[Unit]\n[Service]\nExecStart={sys.executable} {os.path.abspath(__file__)} run {med}\nRestart=always\n[Install]\nWantedBy=multi-user.target");os.system("systemctl enable --now med")
if 'demo' in sys.argv: [os.system(f"python3 send_email.py msg 'Demo Day {i+1}' 'Take meds' && echo 'Day {i+1}'>>demo.log") for i in range(7)]
if 'run' in sys.argv:
 while True:
  time.sleep(1); n=time.strftime("%H:%M:%S"); print(n); db.execute("INSERT INTO l VALUES(?)",(n,)); db.commit()
  if n==med+":00": os.system(f"python3 send_email.py msg 'MEDICATION TIME' 'It is {med}'")
