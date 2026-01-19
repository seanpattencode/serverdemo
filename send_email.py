smtplib,sqlite3,EmailMessage=__import__('smtplib'),__import__('sqlite3'),__import__('email.message',fromlist=['EmailMessage']).EmailMessage
db=sqlite3.connect("email.db");db.execute("CREATE TABLE IF NOT EXISTS c(f,t,p)");r=db.execute("SELECT*FROM c").fetchone()or(db.execute("INSERT INTO c VALUES(?,?,?)",[input(x+": ")for x in["from","to","pass"]]),db.commit(),db.execute("SELECT*FROM c").fetchone())[2]
msg=EmailMessage();msg["From"],msg["To"],msg["Subject"]=r[0],r[1],input("subject: ");msg.set_content(input("body: "))
s=smtplib.SMTP_SSL("smtp.gmail.com",465);s.login(r[0],r[2]);s.sendmail(r[0],r[1],msg.as_string());print(f"Sent '{msg['Subject']}' from {r[0]} to {r[1]}")
