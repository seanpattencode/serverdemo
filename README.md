./venv/bin/python rss_checker.py

## Multi-user Setup

Owner must run first to create db with correct permissions:
```
chmod 777 /path/to/serverdemo
./venv/bin/python rss_checker.py
```

Other users can then run normally. Only the owner can change db permissions - this is a Linux limitation, not a bug.
