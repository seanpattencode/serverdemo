#!/usr/bin/env python3
import subprocess,sys

DEFAULTS = {
    "net.core.rmem_max": "212992",
    "net.core.wmem_max": "212992",
    "net.ipv4.tcp_rmem": "4096 131072 6291456",
    "net.ipv4.tcp_wmem": "4096 16384 4194304",
}

OPTIMIZED = {
    "net.core.rmem_max": "16777216",
    "net.core.wmem_max": "16777216",
    "net.ipv4.tcp_rmem": "4096 87380 16777216",
    "net.ipv4.tcp_wmem": "4096 65536 16777216",
}

def get(k): return " ".join(subprocess.getoutput(f"sysctl -n {k}").split())
def set(k,v): subprocess.run(["sudo","sysctl","-w",f"{k}={v}"],check=True)

def status():
    print("Current TCP buffer settings:")
    for k in DEFAULTS:
        v = get(k)
        opt = "OK" if v.strip() == OPTIMIZED[k] else "LOW"
        print(f"  {k} = {v} [{opt}]")

def apply():
    print("Applying optimized settings...")
    for k,v in OPTIMIZED.items(): set(k,v)
    print("Done. Reconnect SSH to use new settings.")

def revert():
    print("Reverting to defaults...")
    for k,v in DEFAULTS.items(): set(k,v)
    print("Done.")

def permanent():
    print("Writing to /etc/sysctl.d/99-tcp-tuning.conf...")
    conf = "\n".join(f"{k}={v}" for k,v in OPTIMIZED.items())
    subprocess.run(["sudo","tee","/etc/sysctl.d/99-tcp-tuning.conf"], input=conf.encode(), check=True, stdout=subprocess.DEVNULL)
    print("Done. Settings will persist after reboot.")

def remove():
    print("Removing permanent config...")
    subprocess.run(["sudo","rm","-f","/etc/sysctl.d/99-tcp-tuning.conf"], check=True)
    print("Done.")

if __name__ == "__main__":
    cmds = {"status":status, "apply":apply, "revert":revert, "permanent":permanent, "remove":remove}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        status()
        print(f"\nUsage: python3 {sys.argv[0]} <{'/'.join(cmds.keys())}>")
    else:
        cmds[sys.argv[1]]()
