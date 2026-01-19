import urllib.request, xml.etree.ElementTree as ET, sqlite3
conn = sqlite3.connect("feeds.db"); conn.execute("CREATE TABLE IF NOT EXISTS feeds(url TEXT)"); [conn.execute("INSERT OR IGNORE INTO feeds VALUES(?)", (u,)) for u in ["https://news.ycombinator.com/rss", "https://feeds.bbci.co.uk/news/rss.xml"]]; conn.commit()
for url in conn.execute("SELECT url FROM feeds").fetchall():
    for i in ET.fromstring(urllib.request.urlopen(url[0]).read()).findall(".//item")[:3]: print(f"{i.find('title').text}\n  {i.find('link').text}\n")
