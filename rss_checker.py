import urllib.request, xml.etree.ElementTree as ET, sqlite3
conn = sqlite3.connect("feeds.db"); conn.execute("CREATE TABLE IF NOT EXISTS feeds(url TEXT UNIQUE)"); [conn.execute("INSERT OR IGNORE INTO feeds VALUES(?)", (u,)) for u in ["https://news.ycombinator.com/rss", "https://feeds.bbci.co.uk/news/rss.xml"]]; conn.commit()
feeds = conn.execute("SELECT url FROM feeds").fetchall()
print("RSS CHECKER\nSaved feeds:", *[f"  {i+1}. {f[0]}" for i,f in enumerate(feeds)], sep="\n")
if input("Start checking? (y/n): ").lower() == "y":
    for url in feeds:
        for i in ET.fromstring(urllib.request.urlopen(url[0]).read()).findall(".//item")[:3]: print(f"{i.find('title').text}\n  {i.find('link').text}\n")
