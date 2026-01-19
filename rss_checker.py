import urllib.request, xml.etree.ElementTree as ET, sqlite3, re, html
from readability import Document
from googlenewsdecoder import new_decoderv1
def decode(url): return new_decoderv1(url).get('decoded_url', url) if 'news.google.com' in url else url
def fetch(url):
    try: req=urllib.request.Request(decode(url), headers={'User-Agent':'Mozilla/5.0'}); r=urllib.request.urlopen(req, timeout=10); return r.read().decode('utf-8','ignore'), r.geturl()
    except: return '', ''
conn = sqlite3.connect("feeds.db"); conn.execute("CREATE TABLE IF NOT EXISTS feeds(url TEXT UNIQUE)"); [conn.execute("INSERT OR IGNORE INTO feeds VALUES(?)", (u,)) for u in ["https://news.ycombinator.com/rss", "https://feeds.bbci.co.uk/news/rss.xml", "https://news.google.com/rss/search?q=AI", "https://news.google.com/rss/search?q=Demis+Hassabis", "https://feeds.arstechnica.com/arstechnica/technology-lab"]]; conn.commit()
feeds = conn.execute("SELECT url FROM feeds").fetchall()
print("RSS CHECKER\nSaved feeds:", *[f"  {i+1}. {f[0]}" for i,f in enumerate(feeds)], sep="\n")
if input("Start checking? (y/n): ").lower() == "y":
    for url in feeds:
        for i in ET.fromstring(urllib.request.urlopen(url[0]).read()).findall(".//item")[:3]: raw=i.findtext('{http://purl.org/rss/1.0/modules/content/}encoded') or i.findtext('description') or ''; txt=html.unescape(re.sub('<[^>]+>',' ',raw)).strip(); page,_=fetch(i.find('link').text) if len(txt)<200 else ('',''); txt=' '.join(re.sub('<[^>]+>',' ',Document(page).summary()).split()) if page else txt; print(f"{i.find('title').text}\n  {i.find('link').text}\n  {txt}\n")
