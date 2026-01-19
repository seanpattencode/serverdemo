#!/usr/bin/env python3
import urllib.request, xml.etree.ElementTree as ET, sqlite3, re, html, os; os.umask(0)
from readability import Document
from googlenewsdecoder import new_decoderv1
def decode(url): return new_decoderv1(url).get('decoded_url', url) if 'news.google.com' in url else url
def fetch(url):
    try: req=urllib.request.Request(decode(url), headers={'User-Agent':'Mozilla/5.0'}); r=urllib.request.urlopen(req, timeout=10); return r.read().decode('utf-8','ignore'), r.geturl()
    except: return '', ''
conn = sqlite3.connect("feeds.db"); conn.execute("CREATE TABLE IF NOT EXISTS feeds(url TEXT UNIQUE)"); exec("try: os.chmod('feeds.db', 0o666)\nexcept: pass")
while True:
    feeds = conn.execute("SELECT rowid,url FROM feeds").fetchall()
    print("\nRSS CHECKER\nFeeds:", *[f"  {i+1}. {f[1]}" for i,f in enumerate(feeds)] or ["  (none)"], "\n[r]un [a]dd [d]elete [q]uit", sep="\n")
    c = input("> ").lower()
    if c == 'a': conn.execute("INSERT OR IGNORE INTO feeds VALUES(?)", (input("URL: ").strip(),)); conn.commit()
    elif c == 'd': idx=int(input("ID: "))-1; conn.execute("DELETE FROM feeds WHERE rowid=?", (feeds[idx][0],)) if 0<=idx<len(feeds) else None; conn.commit()
    elif c == 'q': break
    elif c == 'r':
        for url in feeds:
            for i in ET.fromstring(urllib.request.urlopen(url[1]).read()).findall(".//item")[:3]: raw=i.findtext('{http://purl.org/rss/1.0/modules/content/}encoded') or i.findtext('description') or ''; txt=html.unescape(re.sub('<[^>]+>',' ',raw)).strip(); page,_=fetch(i.find('link').text) if len(txt)<200 else ('',''); txt=' '.join(re.sub('<[^>]+>',' ',Document(page).summary()).split()) if page else txt; print(f"{i.find('title').text}\n  {i.find('link').text}\n  {txt}\n")
