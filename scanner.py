#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=====================================================================
  AUTO WEB VULNERABILITY SCANNER - FULL AUTOMATIC (SCAN ALL)
=====================================================================
  Gunakan HANYA untuk menguji website milik sendiri atau yang
  sudah diberi izin tertulis. Penyalahgunaan adalah tanggung jawab
  pengguna. Ini alat untuk pentest yang sah / edukasi.
=====================================================================
  Fitur   : Recon, Port Scan, Subdomain, Crawler, SQLi, XSS, LFI,
            Command Injection, Open Redirect, Header Check, SSL,
            Directory Brute, CMS Check, Full Auto Scan,
            Laporan HTML/TXT/JSON, Mode CLI non-interaktif.
  Bahasa  : Python 3 murni (tanpa library eksternal)
  Cara pakai INTERAKTIF:
     python3 scanner.py
     -> banner + menu muncul
     -> pilih nomor menu
     -> masukkan target (contoh: target.com)
  Cara pakai CLI LANGSUNG (non-interaktif):
     python3 scanner.py -t target.com -m 1
     python3 scanner.py -t target.com --full-auto
=====================================================================
"""

import socket
import ssl
import sys
import os
import re
import json
import time
import argparse
import threading
import urllib.request
import urllib.parse
import urllib.error
from html.parser import HTMLParser
from datetime import datetime

# ===================== KONFIGURASI GLOBAL ==========================
USER_AGENT = "Mozilla/5.0 (compatible; AutoVulnScanner/1.0)"
TIMEOUT = 10
THREADS = 20
MAX_PAGES = 30          # batas halaman saat crawl
REPORT_DIR = "reports"
DIRLIST = [
    "admin", "administrator", "login", "wp-login.php", "dashboard",
    "backup", "backups", "db", "database", "sql", "config", "uploads",
    "upload", "files", "tmp", "temp", "test", "old", ".git", ".env",
    "phpmyadmin", "panel", "cp", "webmail", "server-status",
    "robots.txt", "sitemap.xml", ".htaccess", "wp-admin", "joomla",
    "api", "api/v1", "docs", "swagger", "info.php", "phpinfo.php"
]
SUBDOMAIN_WORDS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1",
    "ns2", "blog", "api", "dev", "staging", "test", "portal", "admin",
    "cpanel", "webdisk", "autodiscover", "autoconfig", "m", "shop",
    "vpn", "remote", "git", "gitlab", "jenkins", "jira", "status"
]
SQLI_PAYLOADS = [
    "'", "\"", "' OR '1'='1", "\" OR \"1\"=\"1", "' OR '1'='1'--",
    "1' ORDER BY 1--+", "1' AND SLEEP(3)--+", "1 UNION SELECT NULL-- -",
    "' AND 1=CONVERT(int,(SELECT @@version))--",
]
SQL_ERRORS = [
    "you have an error in your sql syntax", "warning: mysql",
    "unclosed quotation mark", "quoted string not properly terminated",
    "mysql_fetch", "ORA-00933", "postgresql", "sqlite3.",
    "odbc", "microsoft sql server", "native client", "syntax error",
]
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'-alert(1)-'",
    "<img src=x onerror=alert(1)>",
    "<svg/onload=alert(1)>",
    "\"><img src=x onerror=alert(1)>",
]
LFI_PAYLOADS = [
    "../../../etc/passwd", "../../../../etc/passwd",
    "....//....//etc/passwd", "..%2f..%2f..%2fetc%2fpasswd",
    "/etc/passwd", "php://filter/convert.base64-encode/resource=index.php",
]
CMD_PAYLOADS = [";id", "|id", "`id`", "$(id)", "&whoami"]
CMD_MARKERS = ["uid=", "gid=", "root", "groups="]
REDIR_PAYLOADS = [
    "//evil.com", "https://evil.com", "//cws.check", "//google.com",
]
SECURITY_HEADERS = [
    ("Strict-Transport-Security", "HSTS"),
    ("Content-Security-Policy", "CSP"),
    ("X-Frame-Options", "X-Frame-Options"),
    ("X-Content-Type-Options", "X-Content-Type-Options"),
    ("Referrer-Policy", "Referrer-Policy"),
    ("Permissions-Policy", "Permissions-Policy"),
    ("X-XSS-Protection", "X-XSS-Protection (legacy)"),
]
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445,
                993, 995, 1433, 1521, 2082, 2083, 2222, 3000, 3306,
                3389, 5432, 6379, 8000, 8080, 8443, 8888, 9090, 27017]

# Warna ANSI (aman dimatikan bila terminal tak mendukung)
USE_COLOR = os.environ.get("TERM") != "dumb" and sys.stdout.isatty()
C = {
    "R": "\033[91m", "Y": "\033[93m", "G": "\033[92m",
    "B": "\033[96m", "W": "\033[97m", "D": "\033[90m",
    "BOLD": "\033[1m", "END": "\033[0m",
}


def paint(text, color):
    return f"{C[color]}{text}{C['END']}" if USE_COLOR else text


# ===================== HASIL SCAN GLOBAL ============================
RESULT = {"target": None, "scan_time": None, "findings": [], "info": {}}

# ===================== UTILITAS DASAR ==============================
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


BANNER = r"""
  ___  _____  _    _    __    ___  ____  ___ 
 / __)(  _  )( \/\/ )  /__\  / __)( ___)/ __)
( (_-. )(_)(  )    (  /(__)\ \__ \ )__)( (__ 
 \___/(_____)(__/\__)(__)(__)(___/(____)\___)
"""


def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(paint(BANNER, "W"))
    print(paint("     W E B   V U L N E R A B I L I T Y   S C A N N E R", "B"))
    print(paint("  Full Automatic  |  Multi Menu  |  Authorized Use Only", "D"))
    print(paint("  " + "=" * 62, "D"))
    print("  Waktu : " + now())
    if RESULT["target"]:
        print(paint(f"  TARGET AKTIF : {RESULT['target']}", "G"))
    print()


def show_menu():
    print(paint("""
  ================== MENU UTAMA ===================
""", "W"))
    print(paint("""    1.  FULL AUTO SCAN   (jalankan semua modul otomatis)
    2.  Recon & Fingerprinting
    3.  Port Scanner
    4.  Subdomain Enumeration
    5.  Web Crawler (kumpulkan URL & form)
    6.  SQL Injection Scanner
    7.  XSS Scanner
    8.  LFI / Path Traversal Scanner
    9.  Command Injection Scanner
    10. Open Redirect Scanner
    11. Security Header Check
    12. SSL / TLS Check
    13. Directory & File Brute Force
    14. CMS / Platform Check
    15. Buat Laporan (HTML/TXT/JSON)
    16. Ganti Target""", "Y"))
    print(paint("""    0.  Keluar
  ==================================================""", "W"))


def ask_target(prompt="  [?] Masukkan target (contoh: target.com) : "):
    t = input(paint(prompt, "G")).strip()
    if not t:
        return ask_target(prompt)
    t = t.replace("http://", "").replace("https://", "").strip("/")
    if not re.match(r"^[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", t):
        print(paint("  [!] Format target tidak valid, coba lagi.", "R"))
        return ask_target(prompt)
    RESULT["target"] = t
    print(paint(f"  [+] Target diset: {t}", "G"))
    return t


def make_url(host, path="/", https=None):
    if https is None:
        https = True if port_open(host, 443, 2) else False
    scheme = "https" if https else "http"
    return f"{scheme}://{host}{path}"


def http_get(url, timeout=TIMEOUT, allow_redirect=True, data=None):
    if data:
        return http_post(url, data, timeout)
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "*/*",
        "Connection": "close",
    })

    class NoRedir(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None if not allow_redirect else \
                super().redirect_request(*a, **k)

    op = urllib.request.build_opener(NoRedir)
    try:
        resp = op.open(req, timeout=timeout)
        body = resp.read(500000).decode("utf-8", "replace")
        return {"code": resp.getcode(), "headers": dict(resp.headers),
                "body": body, "url": url}
    except urllib.error.HTTPError as e:
        return {"code": e.code, "headers": dict(e.headers),
                "body": e.read(500000).decode("utf-8", "replace"), "url": url}
    except Exception as e:
        return {"code": None, "error": str(e), "headers": {}, "body": "", "url": url}


def http_post(url, data, timeout=TIMEOUT):
    encoded = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=encoded, headers={
        "User-Agent": USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "close",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        return {"code": resp.getcode(),
                "body": resp.read(500000).decode("utf-8", "replace"),
                "headers": dict(resp.headers)}
    except urllib.error.HTTPError as e:
        return {"code": e.code,
                "body": e.read(500000).decode("utf-8", "replace"),
                "headers": dict(e.headers)}
    except Exception as e:
        return {"code": None, "body": "", "error": str(e), "headers": {}}


def port_open(host, port, timeout=2):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        r = s.connect_ex((host, port))
        s.close()
        return r == 0
    except Exception:
        return False


SEV_COLOR = {"CRITICAL": "R", "HIGH": "R", "MEDIUM": "Y", "LOW": "Y", "INFO": "B"}


def add_finding(severity, category, detail, url=""):
    f = {"severity": severity, "category": category, "detail": detail, "url": url}
    RESULT["findings"].append(f)
    print(f"    {paint('[' + severity + ']', SEV_COLOR.get(severity, 'W'))} "
          f"{paint(category, 'W')} | {detail[:70]}")


def info(msg):
    print(f"    {paint('[*]', 'B')} {msg}")


def ok(msg):
    print(f"    {paint('[+]', 'G')} {msg}")


def run_threads(fn, items, threads=THREADS):
    def worker(q):
        while q:
            try:
                item = q.pop(0)
            except IndexError:
                return
            try:
                fn(item)
            except Exception:
                pass
    queue = list(items)
    ts = [threading.Thread(target=worker, args=(queue,)) for _ in range(threads)]
    [t.start() for t in ts]
    [t.join() for t in ts]

# ===================== MODUL 1: RECON ==============================
def mod_recon(host):
    print(f"\n  {paint('[ MODUL 2 ] RECON PADA : ' + host, 'W')}")
    print(paint("  " + "-" * 62, "D"))
    try:
        ip = socket.gethostbyname(host)
        ok(f"IP Address      : {ip}")
        RESULT["info"]["ip"] = ip
    except Exception:
        info("Gagal resolve hostname.")
        return None
    try:
        name, _, _ = socket.gethostbyaddr(ip)
        info(f"Reverse DNS     : {name}")
    except Exception:
        pass
    for p in (80, 443):
        info(f"Port {p:<4}      : {'TERBUKA' if port_open(host, p) else 'tertutup'}")
    base = make_url(host)
    r = http_get(base)
    if r["code"]:
        info(f"Status Awal     : HTTP {r['code']}")
        server = r["headers"].get("Server") or r["headers"].get("server")
        if server:
            info(f"Server          : {server}")
            add_finding("INFO", "Recon", f"Server header: {server}", base)
        powered = r["headers"].get("X-Powered-By") or r["headers"].get("x-powered-by")
        if powered:
            info(f"X-Powered-By    : {powered}")
        techs = []
        for t, pat in [("WordPress", "wp-content"), ("Joomla", "/joomla"),
                       ("PHP", "\.php"), ("Cloudflare", "cloudflare"),
                       ("Nginx", "nginx"), ("Apache", "apache")]:
            if re.search(pat, r["body"], re.I) or (server and t.lower() in server.lower()):
                techs.append(t)
        if techs:
            ok(f"Teknologi       : {', '.join(sorted(set(techs)))}")
            RESULT["info"]["tech"] = sorted(set(techs))
    else:
        info("Target tidak merespons HTTP.")
    return base

# ===================== MODUL 2: PORT SCAN ===========================
def mod_portscan(host):
    print(f"\n  {paint('[ MODUL 3 ] PORT SCAN : ' + host, 'W')}")
    print(paint("  " + "-" * 62, "D"))
    open_ports = []

    def scan(port):
        if port_open(host, port, 1.5):
            open_ports.append(port)

    run_threads(scan, COMMON_PORTS, 50)
    if not open_ports:
        info("Tidak ada port umum yang terbuka.")
    else:
        for p in sorted(open_ports):
            ok(f"Port terbuka    : {p}")
        RESULT["info"]["open_ports"] = sorted(open_ports)
        risky = {21: "FTP", 23: "Telnet", 3306: "MySQL", 5432: "PostgreSQL",
                 6379: "Redis", 27017: "MongoDB", 3389: "RDP"}
        for p in sorted(open_ports):
            if p in risky:
                add_finding("MEDIUM", "Exposed Service",
                            f"Port {p} ({risky[p]}) terbuka untuk publik", f"{host}:{p}")

# ===================== MODUL 3: CRAWLER ============================
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.forms = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "form":
            self.forms.append({
                "action": a.get("action", ""),
                "method": (a.get("method") or "get").upper(),
                "fields": []})
        if tag == "input" and self.forms:
            if a.get("type") not in ("submit", "button", "reset", "file"):
                self.forms[-1]["fields"].append(a.get("name", ""))


def normalize(base, link):
    link = link.split("#")[0]
    if not link or link.startswith(("mailto:", "tel:", "javascript:")):
        return None
    full = urllib.parse.urljoin(base, link)
    if not full.startswith(("http://", "https://")):
        return None
    if urllib.parse.urlparse(full).netloc != urllib.parse.urlparse(base).netloc:
        return None
    return full


def mod_crawler(base):
    print(f"\n  {paint('[ MODUL 5 ] CRAWLER : ' + base, 'W')}")
    print(paint("  " + "-" * 62, "D"))
    visited, pages, forms = set(), [], []
    queue = [base]
    while queue and len(visited) < MAX_PAGES:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        r = http_get(url)
        if not r["code"] or not r["body"]:
            continue
        pages.append({"url": url, "body": r["body"], "code": r["code"]})
        parser = LinkParser()
        try:
            parser.feed(r["body"])
        except Exception:
            pass
        for f in parser.forms:
            f["url"] = urllib.parse.urljoin(url, f["action"] or url)
            forms.append(f)
        for l in parser.links:
            n = normalize(url, l)
            if n and n not in visited:
                queue.append(n)
    ok(f"Halaman ditemukan : {len(visited)}")
    ok(f"Form ditemukan    : {len(forms)}")
    RESULT["info"]["pages_crawled"] = len(visited)
    RESULT["info"]["forms"] = len(forms)
    return pages, forms


def collect_params(pages, base):
    """Kumpulkan semua URL ber-parameter dari halaman hasil crawl."""
    params = set()
    links = set()
    for p in pages:
        links.add(p["url"])
        parser = LinkParser()
        try:
            parser.feed(p["body"])
        except Exception:
            pass
        for l in parser.links:
            n = normalize(base, l)
            if n:
                links.add(n)
    for l in links:
        parsed = urllib.parse.urlparse(l)
        if parsed.query:
            params.add(l)
    return list(params)

# ===================== MODUL 4: SQL INJECTION =======================
def test_sqli_url(url):
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qsl(parsed.query)
    if not qs:
        return
    for i, (k, v) in enumerate(qs):
        baseline = http_get(url)
        base_body = baseline["body"].lower()
        for payload in SQLI_PAYLOADS:
            new = [(a, (payload if j == i else b)) for j, (a, b) in enumerate(qs)]
            test_url = parsed._replace(query=urllib.parse.urlencode(new)).geturl()
            r = http_get(test_url)
            body = r["body"].lower()
            err_hit = [e for e in SQL_ERRORS if e in body]
            if err_hit and err_hit[0] not in base_body:
                add_finding("CRITICAL", "SQL Injection (Error)",
                            f"Param '{k}' error DB: {err_hit[0]}", test_url)
                return
            if "sleep(3)" in payload.lower() and r["code"] == 200:
                t0 = time.time()
                http_get(test_url)
                if time.time() - t0 > 2.5:
                    add_finding("CRITICAL", "SQL Injection (Time-Based)",
                                f"Param '{k}' delay terdeteksi (SLEEP)", test_url)
                    return
            if payload in ("'", '"') and r["code"] == 500 and baseline["code"] != 500:
                add_finding("HIGH", "Kemungkinan SQLi",
                            f"Param '{k}' menyebabkan HTTP 500", test_url)
                return


def test_sqli_form(form):
    fields = [f for f in form["fields"] if f]
    if not fields:
        return
    data = {f: "test" for f in fields}
    for f in fields:
        for payload in SQLI_PAYLOADS:
            d = dict(data)
            d[f] = payload
            r = (http_post if form["method"] == "POST" else http_get)(form["url"], d)
            body = r.get("body", "").lower()
            err_hit = [e for e in SQL_ERRORS if e in body]
            if err_hit:
                add_finding("CRITICAL", "SQL Injection (Form)",
                            f"Field '{f}' error DB: {err_hit[0]}", form["url"])
                return
            if "sleep(3)" in payload.lower():
                t0 = time.time()
                (http_post if form["method"] == "POST" else http_get)(form["url"], d)
                if time.time() - t0 > 2.5:
                    add_finding("CRITICAL", "SQL Injection (Form, Time)",
                                f"Field '{f}' delay terdeteksi", form["url"])
                    return


def mod_sqli(pages, forms, base):
    print(f"\n  {paint('[ MODUL 6 ] SQL INJECTION', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    params = collect_params(pages, base)
    info(f"URL berparameter diuji : {len(params)}")
    info(f"Form diuji             : {len(forms)}")
    run_threads(test_sqli_url, params[:40], 6)
    for form in forms:
        test_sqli_form(form)

# ===================== MODUL 5: XSS =================================
def test_xss_url(url):
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qsl(parsed.query)
    if not qs:
        return
    for i, (k, v) in enumerate(qs):
        for payload in XSS_PAYLOADS:
            new = [(a, (payload if j == i else b)) for j, (a, b) in enumerate(qs)]
            test_url = parsed._replace(query=urllib.parse.urlencode(new)).geturl()
            r = http_get(test_url)
            if payload.lower() in r["body"].lower():
                add_finding("HIGH", "XSS (Reflected)",
                            f"Param '{k}' memantulkan payload", test_url)
                return


def test_xss_form(form):
    fields = [f for f in form["fields"] if f]
    if not fields:
        return
    for f in fields:
        for payload in XSS_PAYLOADS:
            d = {x: "test" for x in fields}
            d[f] = payload
            r = (http_post if form["method"] == "POST" else http_get)(form["url"], d)
            if payload.lower() in r.get("body", "").lower():
                add_finding("HIGH", "XSS (Form)",
                            f"Field '{f}' memantulkan payload", form["url"])
                return


def mod_xss(pages, forms, base):
    print(f"\n  {paint('[ MODUL 7 ] CROSS-SITE SCRIPTING (XSS)', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    params = collect_params(pages, base)
    info(f"URL berparameter diuji : {len(params)}")
    run_threads(test_xss_url, params[:40], 6)
    for form in forms:
        test_xss_form(form)

# ===================== MODUL 6: LFI / RFI ===========================
def mod_lfi(pages, base, forms=None):
    print(f"\n  {paint('[ MODUL 8 ] LFI / RFI / PATH TRAVERSAL', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    params = collect_params(pages, base)
    if forms:
        params += [f["url"] for f in forms]
    params = list(set(params))
    for url in params:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qsl(parsed.query)
        for i, (k, v) in enumerate(qs):
            for payload in LFI_PAYLOADS:
                new = [(a, (payload if j == i else b)) for j, (a, b) in enumerate(qs)]
                test_url = parsed._replace(query=urllib.parse.urlencode(new)).geturl()
                r = http_get(test_url)
                body = r["body"]
                if "root:" in body and ":/bin" in body:
                    add_finding("CRITICAL", "LFI",
                                f"Param '{k}' membaca /etc/passwd", test_url)
                    break
    info(f"Titik uji LFI: {len(params)} (hasil di atas jika ada)")

# ===================== MODUL 7: COMMAND INJECTION ===================
def mod_cmd(pages, base):
    print(f"\n  {paint('[ MODUL 9 ] COMMAND INJECTION', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    params = collect_params(pages, base)
    for url in params:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qsl(parsed.query)
        for i, (k, v) in enumerate(qs):
            for payload in CMD_PAYLOADS:
                new = [(a, (payload if j == i else b)) for j, (a, b) in enumerate(qs)]
                test_url = parsed._replace(query=urllib.parse.urlencode(new)).geturl()
                r = http_get(test_url)
                for marker in CMD_MARKERS:
                    if marker in r["body"]:
                        add_finding("CRITICAL", "Command Injection",
                                    f"Param '{k}' mengeksekusi perintah", test_url)
                        break
    info(f"Titik uji Command Injection: {len(params)}")

# ===================== MODUL 8: OPEN REDIRECT =======================
def mod_redirect(pages, base):
    print(f"\n  {paint('[ MODUL 10 ] OPEN REDIRECT', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    params = collect_params(pages, base)
    for url in params:
        parsed = urllib.parse.urlparse(url)
        qs = urllib.parse.parse_qsl(parsed.query)
        for i, (k, v) in enumerate(qs):
            if k.lower() not in ("url", "redirect", "next", "r", "dest",
                                 "destination", "goto", "return", "returnto", "link"):
                continue
            for payload in REDIR_PAYLOADS:
                new = [(a, (payload if j == i else b)) for j, (a, b) in enumerate(qs)]
                test_url = parsed._replace(query=urllib.parse.urlencode(new)).geturl()
                r = http_get(test_url, allow_redirect=False)
                loc = r["headers"].get("Location") or r["headers"].get("location") or ""
                if "evil.com" in loc or "evil.com" in r["body"]:
                    add_finding("MEDIUM", "Open Redirect",
                                f"Param '{k}' bisa dialihkan ke domain asing", test_url)
                    break
    info(f"Titik uji redirect: {len(params)}")

# ===================== MODUL 9: SECURITY HEADERS ====================
def mod_headers(base):
    print(f"\n  {paint('[ MODUL 11 ] SECURITY HEADERS', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    r = http_get(base)
    lower = {k.lower(): v for k, v in r["headers"].items()}
    for header, label in SECURITY_HEADERS:
        if header.lower() not in lower:
            add_finding("MEDIUM", "Header Hilang",
                        f"Header '{label}' tidak ditemukan", base)
    if "server" in lower and re.search(r"\d", lower.get("server", "")):
        add_finding("LOW", "Info Berlebih",
                    f"Versi server terpapar: {lower['server']}", base)
    ck = lower.get("set-cookie", "")
    if ck and "httponly" not in ck.lower():
        add_finding("LOW", "Cookie", "Cookie tanpa HttpOnly", base)
    if ck and "secure" not in ck.lower():
        add_finding("LOW", "Cookie", "Cookie tanpa flag Secure", base)
    info("Pemeriksaan header selesai.")

# ===================== MODUL 10: SSL/TLS ============================
def mod_ssl(host):
    print(f"\n  {paint('[ MODUL 12 ] SSL / TLS CHECK : ' + host, 'W')}")
    print(paint("  " + "-" * 62, "D"))
    if not port_open(host, 443, 3):
        info("Port 443 tertutup, SSL tidak aktif (HTTP saja).")
        add_finding("MEDIUM", "Tanpa HTTPS", "Server tidak melayani HTTPS", f"http://{host}")
        return
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as s:
                cert = s.getpeercert()
                cipher = s.cipher()
                info(f"Protokol TLS    : {s.version()}")
                info(f"Cipher          : {cipher[0]}")
                exp = cert.get("notAfter")
                info(f"Masa berlaku    : sampai {exp}")
                expire = ssl.cert_time_to_seconds(exp)
                days_left = (expire - time.time()) / 86400
                if days_left < 30:
                    add_finding("MEDIUM", "Sertifikat Segera Kedaluwarsa",
                                f"Sisa {int(days_left)} hari", f"https://{host}")
                sans = [v for k, v in cert.get("subjectAltName", [])]
                if not any(host.endswith(n.replace("*.", "")) for n in sans):
                    add_finding("MEDIUM", "Sertifikat Tidak Cocok",
                                f"Host tidak ada di SAN: {sans[:3]}", f"https://{host}")
    except ssl.SSLCertVerificationError as e:
        add_finding("HIGH", "Sertifikat Tidak Valid", str(e)[:90], f"https://{host}")
    except Exception as e:
        info(f"SSL check gagal: {e}")
    try:
        raw = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        raw.check_hostname = False
        raw.verify_mode = ssl.CERT_NONE
        with socket.create_connection((host, 443), timeout=10) as sock:
            with raw.wrap_socket(sock) as s:
                if s.version() in ("TLSv1", "TLSv1.1"):
                    add_finding("HIGH", "TLS Usang",
                                f"Server menerima {s.version()}", f"https://{host}")
    except Exception:
        pass

# ===================== MODUL 11: DIRECTORY BRUTE ====================
def mod_dirs(base):
    print(f"\n  {paint('[ MODUL 13 ] DIRECTORY & FILE BRUTE', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    found = []

    def check(path):
        r = http_get(base.rstrip("/") + "/" + path)
        if r["code"] in (200, 301, 302, 403):
            found.append((path, r["code"]))

    run_threads(check, DIRLIST, 20)
    for p, code in sorted(set(found)):
        info(f"{code}  /{p}")
        if p in (".env", ".git/HEAD") or (code == 200 and p in ("phpinfo.php", "info.php")):
            add_finding("HIGH", "File Sensitif Terpapar",
                        f"/{p} dapat diakses ({code})",
                        base.rstrip("/") + "/" + p)
    r = http_get(base.rstrip("/") + "/robots.txt")
    if r["code"] == 200 and "disallow" in r["body"].lower():
        info("robots.txt ditemukan (cek entri sensitif).")
        disallows = re.findall(r"Disallow:\s*(\S+)", r["body"], re.I)
        for d in disallows[:10]:
            info(f"  robots -> Disallow: {d}")

# ===================== MODUL 12: SUBDOMAIN ==========================
def mod_subdomain(host):
    print(f"\n  {paint('[ MODUL 4 ] SUBDOMAIN ENUMERATION', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    if host.count(".") < 1:
        info("Hostname tidak valid untuk subdomain.")
        return
    parts = host.split(".")
    root = ".".join(parts[-2:]) if len(parts) >= 2 else host
    found = []

    def check(word):
        sub = f"{word}.{root}"
        try:
            ip = socket.gethostbyname(sub)
            found.append((sub, ip))
        except Exception:
            pass

    run_threads(check, SUBDOMAIN_WORDS, 20)
    if not found:
        info("Tidak ada subdomain aktif ditemukan.")
    for sub, ip in sorted(found):
        ok(f"{sub:35} -> {ip}")
        if any(x in sub for x in ("dev", "test", "staging", "old", "backup")):
            add_finding("MEDIUM", "Subdomain Berisiko",
                        f"{sub} aktif (lingkungan non-produksi)", f"http://{sub}")
    RESULT["info"]["subdomains"] = [s for s, _ in found]

# ===================== MODUL 13: CMS & BACKUP =======================
def mod_cms(base):
    print(f"\n  {paint('[ MODUL 14 ] CMS / PLATFORM CHECK', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    checks = {
        "WordPress": ["/wp-login.php", "/wp-admin/"],
        "Joomla": ["/administrator/"],
        "Drupal": ["/user/login"],
        "PrestaShop": ["/admin-dev/"],
        "phpMyAdmin": ["/phpmyadmin/"],
        "Git repo": ["/.git/config"],
        ".env file": ["/.env"],
        "composer.json": ["/composer.json"],
    }
    for name, paths in checks.items():
        for p in paths:
            r = http_get(base.rstrip("/") + p, timeout=6)
            if r["code"] == 200:
                ok(f"{name:15} terdeteksi ({p})")
                if name in ("Git repo", ".env file"):
                    add_finding("HIGH", f"{name} Terpapar",
                                f"{p} dapat diakses publik", base + p)
                break
    wp = http_get(base.rstrip("/") + "/wp-content/", timeout=6)
    if wp["code"] == 403:
        add_finding("LOW", "WordPress", "Struktur wp-content terbuka (403 listing)")

# ===================== MODUL 14: REPORT ============================
def mod_report():
    print(f"\n  {paint('[ MODUL 15 ] MEMBUAT LAPORAN', 'W')}")
    print(paint("  " + "-" * 62, "D"))
    os.makedirs(REPORT_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    sev_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    RESULT["findings"].sort(key=lambda f: sev_order[f["severity"]])
    RESULT["scan_time"] = now()
    counts = {}
    for f in RESULT["findings"]:
        counts[f["severity"]] = counts.get(f["severity"], 0) + 1
    RESULT["info"]["counts"] = counts
    host = RESULT["target"] or "target"
    # JSON
    with open(f"{REPORT_DIR}/scan_{ts}.json", "w") as fp:
        json.dump(RESULT, fp, indent=2)
    # TXT
    with open(f"{REPORT_DIR}/scan_{ts}.txt", "w") as fp:
        fp.write("LAPORAN WEB VULNERABILITY SCAN\n")
        fp.write(f"Target   : {host}\nWaktu    : {now()}\n")
        fp.write(f"Ringkasan: {counts}\n" + "=" * 60 + "\n\n")
        for f in RESULT["findings"]:
            fp.write(f"[{f['severity']}] {f['category']}\n  {f['detail']}\n  URL: {f['url']}\n\n")
    # HTML
    rows = "".join(
        f"<tr><td class='{f['severity']}'>{f['severity']}</td>"
        f"<td>{f['category']}</td><td>{f['detail']}</td>"
        f"<td><code>{f['url']}</code></td></tr>"
        for f in RESULT["findings"])
    html = f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<title>Scan {host}</title><style>
body{{font-family:Arial;background:#0f172a;color:#e2e8f0;padding:30px}}
table{{width:100%;border-collapse:collapse}}
td,th{{border:1px solid #334;padding:8px;font-size:14px}}
.CRITICAL{{background:#7f1d1d}} .HIGH{{background:#9a3412}}
.MEDIUM{{background:#78350f}} .LOW{{background:#1e3a5f}}
h1{{color:#38bdf8}}</style></head><body>
<h1>Hasil Scan: {host}</h1><p>Waktu: {now()}</p>
<p><b>Temuan:</b> {counts}</p>
<table><tr><th>Severity</th><th>Kategori</th><th>Detail</th><th>URL</th></tr>
{rows}</table></body></html>"""
    with open(f"{REPORT_DIR}/report_{ts}.html", "w") as fp:
        fp.write(html)
    ok(f"Laporan tersimpan di folder '{REPORT_DIR}/':")
    ok(f"  - report_{ts}.html  (buka di browser)")
    ok(f"  - scan_{ts}.txt")
    ok(f"  - scan_{ts}.json")
    return f"{REPORT_DIR}/report_{ts}.html"

# ===================== MODUL 15: FULL AUTO SCAN =====================
def full_auto(host):
    print(f"\n  {paint('>>> FULL AUTOMATIC SCAN DIMULAI PADA ' + host + ' <<<', 'G')}")
    print(paint("  " + "=" * 62, "D"))
    RESULT["target"] = host
    base = mod_recon(host)
    if not base:
        print(paint("  Target tidak bisa dihubungi. Hentikan.", "R"))
        return
    mod_portscan(host)
    mod_ssl(host)
    pages, forms = mod_crawler(base)
    mod_headers(base)
    mod_sqli(pages, forms, base)
    mod_xss(pages, forms, base)
    mod_lfi(pages, base, forms)
    mod_cmd(pages, base)
    mod_redirect(pages, base)
    mod_dirs(base)
    mod_cms(base)
    mod_subdomain(host)
    mod_report()
    print(f"\n  {paint('>>> SCAN SELESAI. SEMUA LAPORAN DI FOLDER reports/ <<<', 'G')}\n")

# ===================== EKSEKUSI MENU =================================
def needs_crawler(n):
    return n in (5, 6, 7, 8, 9, 10)


def run_menu_choice(choice, host):
    """Jalankan modul sesuai nomor menu. Return host (mungkin berganti)."""
    if choice == 0:
        print(paint("\n  Terima kasih. Scan dengan bijak & bertanggung jawab!\n", "G"))
        sys.exit(0)
    if choice == 16:
        host = ask_target()
        return host
    if choice not in range(1, 16):
        print(paint("  Pilihan tidak valid.", "R"))
        return host
    if not host:
        host = ask_target()
    base = make_url(host)
    print(f"\n  {paint('TARGET : ' + host, 'Y')}")
    if choice == 1:
        full_auto(host)
    elif choice == 2:
        mod_recon(host)
    elif choice == 3:
        mod_portscan(host)
    elif choice == 4:
        mod_subdomain(host)
    elif choice == 5:
        mod_crawler(base)
    elif choice in (6, 7, 8, 9, 10):
        pages, forms = mod_crawler(base)
        if choice == 6:
            mod_sqli(pages, forms, base)
        elif choice == 7:
            mod_xss(pages, forms, base)
        elif choice == 8:
            mod_lfi(pages, base, forms)
        elif choice == 9:
            mod_cmd(pages, base)
        elif choice == 10:
            mod_redirect(pages, base)
    elif choice == 11:
        mod_headers(base)
    elif choice == 12:
        mod_ssl(host)
    elif choice == 13:
        mod_dirs(base)
    elif choice == 14:
        mod_cms(base)
    elif choice == 15:
        mod_report()
    return host


# ===================== MODE CLI NON-INTERAKTIF =======================
def run_cli(args):
    """Mode langsung: python3 scanner.py -t target.com -m 1 [--auto-report]"""
    global REPORT_DIR, MAX_PAGES, THREADS
    if args.report_dir:
        REPORT_DIR = args.report_dir
    if args.max_pages:
        MAX_PAGES = args.max_pages
    if args.threads:
        THREADS = args.threads
    host = args.target.replace("http://", "").replace("https://", "").strip("/")
    RESULT["target"] = host
    if args.full_auto or args.module in (0, 1):
        full_auto(host)
    else:
        run_menu_choice(args.module, host)
        if args.auto_report:
            mod_report()
    return 0

# ===================== MENU UTAMA ===================================
def main():
    parser = argparse.ArgumentParser(
        description="Auto Web Vulnerability Scanner - SCAN ALL (authorized use only)",
        epilog="Contoh: python3 scanner.py -t target.com --full-auto")
    parser.add_argument("-t", "--target", help="Target scan, contoh: target.com")
    parser.add_argument("-m", "--module", type=int, choices=range(0, 17), default=None,
                       help="Nomor menu (1-16). 1 = full auto. Tanpa -t = mode interaktif")
    parser.add_argument("--full-auto", action="store_true",
                       help="Jalankan semua modul otomatis")
    parser.add_argument("--auto-report", action="store_true",
                       help="Buat laporan otomatis setelah modul CLI selesai")
    parser.add_argument("--report-dir", default=None, help="Folder laporan (default: reports)")
    parser.add_argument("--max-pages", type=int, default=None, help="Batas halaman crawl")
    parser.add_argument("--threads", type=int, default=None, help="Jumlah thread")
    args = parser.parse_args()

    # ---------- MODE CLI NON-INTERAKTIF ----------
    if args.target or args.full_auto:
        return run_cli(args)

    # ---------- MODE INTERAKTIF (BANNER + MENU) ----------
    banner()
    print(paint("  LEGAL: Gunakan hanya pada aset yang Anda miliki/izin.", "R"))
    host = None
    while True:
        show_menu()
        raw = input(paint("  Pilih menu >> ", "G")).strip().lower()
        if raw in ("g", "16"):
            choice = 16
        elif raw in ("0", "q", "exit", "keluar"):
            choice = 0
        elif raw.isdigit() and 1 <= int(raw) <= 15:
            choice = int(raw)
        else:
            print(paint("  Pilihan tidak valid.", "R"))
            continue
        host = run_menu_choice(choice, host)
        if choice != 16:
            try:
                input(paint("\n  [Enter untuk kembali ke menu] ", "D"))
            except EOFError:
                break
        banner()


if __name__ == "__main__":
    try:
        sys.exit(main() or 0)
    except KeyboardInterrupt:
        print("\n\n  [!] Dihentikan oleh user. Bye!\n")
        sys.exit(0)
