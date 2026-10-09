<div align="center">

# 🔥 Auto Web Vulnerability Scanner

### Full Automatic Web Pentest Tool — 15 Modul dalam 1 Script Python

**Python 3 • Tanpa Library Eksternal • Multi-threading • Multi Platform**

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Windows%20%7C%20Linux-success)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Ethical](https://img.shields.io/badge/Use-Authorized%20Only-red)]()

</div>

---

> ⚠️ **PERINGATAN LEGAL**
>
> Tool ini dibuat untuk **pentest yang sah**, edukasi keamanan, dan pengujian website **milik sendiri** atau yang sudah memberi **izin tertulis** (bug bounty, kontrak pentest).
> Melakukan scan tanpa izin **melanggar UU ITE** dan bisa berujung pidana. Gunakan dengan bijak — Developer tidak bertanggung jawab atas penyalahgunaan.

---

## 📋 Daftar Isi

- [✨ Fitur](#-fitur)
- [📥 Instalasi](#-instalasi)
  - [📱 Termux (Android)](#-termux-android)
  - [🪟 Windows](#-windows)
  - [🐧 Linux](#-linux)
- [🚀 Cara Penggunaan](#-cara-penggunaan)
- [🧰 Panduan Setiap Fitur](#-panduan-setiap-fitur)
- [📊 Laporan Hasil Scan](#-laporan-hasil-scan)
- [☁️ Deploy ke GitHub](#️-deploy-ke-github)
- [🤝 Kontribusi](#-kontribusi)

---

## ✨ Fitur

| # | Modul | Deskripsi |
|---|-------|-----------|
| 1 | **Full Auto Scan** | Jalankan SEMUA modul sekaligus secara otomatis |
| 2 | **Recon & Fingerprinting** | IP, reverse DNS, server header, deteksi teknologi |
| 3 | **Port Scanner** | Scan 30+ port umum, deteksi service berisiko |
| 4 | **Subdomain Enumeration** | Cari subdomain aktif (dev/staging/test) |
| 5 | **Web Crawler** | Kumpulkan otomatis semua halaman, link & form |
| 6 | **SQL Injection** | Error-based & Time-based (SLEEP), via param & form |
| 7 | **XSS Scanner** | 6 payload — reflected & form-based |
| 8 | **LFI / Path Traversal** | Termasuk bypass & `php://filter` |
| 9 | **Command Injection** | Deteksi eksekusi perintah (`id`, `whoami`) |
| 10 | **Open Redirect** | Deteksi parameter redirect yang bisa dibajak |
| 11 | **Security Header Check** | HSTS, CSP, X-Frame-Options, cookie flags |
| 12 | **SSL/TLS Check** | Protokol usang, sertifikat kedaluwarsa/mismatch |
| 13 | **Directory Brute Force** | Cari `/admin`, `/.env`, `/.git`, dll |
| 14 | **CMS Check** | WordPress, Joomla, Drupal, phpMyAdmin |
| 15 | **Laporan Otomatis** | HTML + TXT + JSON di folder `reports/` |

**Keunggulan:**
- ✅ 100% Python murni — **tidak perlu `pip install` apa pun**
- ✅ Multi-threading → scan lebih cepat
- ✅ Auto-detect HTTP/HTTPS target
- ✅ Menu interaktif — pilih modul satu-satu atau full auto
- ✅ Laporan siap dibuka di browser

---

## 📥 Instalasi

### 📱 Termux (Android)

```bash
# 1. Update & install Python
pkg update && pkg upgrade -y
pkg install python git -y

# 2. Clone repository
git clone https://github.com/username/web-vuln-scanner.git
cd web-vuln-scanner

# 3. Jalankan
python3 scanner.py
```

> 💡 Kalau mau scan lama di background, install `termux-api` dan pastikan Termux tidak di-kill oleh baterai (Nonaktifkan *Battery Optimization* untuk Termux di Pengaturan Android).

### 🪟 Windows

**Cara 1 — Installer Python:**

1. Download Python dari [python.org/downloads](https://www.python.org/downloads/)
2. Saat install, **centang ✅ "Add Python to PATH"**
3. Buka **Command Prompt (cmd)** atau **PowerShell**, lalu:

```cmd
:: Clone repository
git clone https://github.com/username/web-vuln-scanner.git
cd web-vuln-scanner

:: Jalankan
python scanner.py
```

**Cara 2 — Tanpa Git (download ZIP):**

1. Klik tombol hijau **`<> Code`** di repo ini → **Download ZIP**
2. Extract ZIP
3. Buka cmd di folder hasil extract (ketik `cmd` di address bar File Explorer)
4. Jalankan: `python scanner.py`

> 💡 Jika error `python tidak dikenali`, coba `py scanner.py` atau install ulang Python dengan PATH tercentang.

### 🐧 Linux

```bash
# Debian / Ubuntu / Kali
sudo apt update && sudo apt install python3 git -y
git clone https://github.com/username/web-vuln-scanner.git
cd web-vuln-scanner
python3 scanner.py
```

```bash
# Arch / Manjaro
sudo pacman -S python git --noconfirm
git clone https://github.com/username/web-vuln-scanner.git
cd web-vuln-scanner
python3 scanner.py
```

```bash
# Fedora
sudo dnf install python3 git -y
git clone https://github.com/username/web-vuln-scanner.git
cd web-vuln-scanner
python3 scanner.py
```

> 🐧 Di **Kali Linux**, tool ini cocok jadi pendamping Nmap/Nikto — cepat dipakai karena tanpa dependensi.

---

## 🚀 Cara Penggunaan

```bash
python3 scanner.py
```

```
  ================== MENU UTAMA ===================
    1.  FULL AUTO SCAN   (jalankan semua modul otomatis)
    2.  Recon & Fingerprinting
    3.  Port Scanner
    ...
    16. Ganti Target
    0.  Keluar
  ==================================================
```

1. Jalankan script → masukkan **target**, contoh: `target.com` (tanpa `http://`)
2. Tool otomatis mendeteksi HTTP/HTTPS
3. Pilih menu — atau tekan `1` untuk **Full Auto Scan**
4. Tekan `g` kapan saja untuk ganti target
5. Hasil scan tersimpan di folder `reports/`

---

## 🧰 Panduan Setiap Fitur

### 1️⃣ Full Auto Scan
Menu paling cepat: jalanin **semua modul berurutan** (Recon → Port → SSL → Crawler → semua scanner → Laporan). Cocok untuk audit menyeluruh satu target.

### 2️⃣ Recon & Fingerprinting
Mengumpulkan info dasar: IP address, reverse DNS, port 80/443, header `Server` & `X-Powered-By`, plus deteksi teknologi (WordPress, PHP, Cloudflare, Nginx, Apache).

### 3️⃣ Port Scanner
Menguji 30+ port umum (21, 22, 80, 443, 3306, 6379, dst) dengan 50 thread. Service berbahaya yang terbuka untuk publik (MySQL, Redis, MongoDB, RDP) langsung di-flag **MEDIUM**.

### 4️⃣ Subdomain Enumeration
Mencoba ±30 subdomain umum (`dev.`, `staging.`, `api.`, `cpanel.`, dll). Subdomain lingkungan non-produksi yang aktif di-flag sebagai risiko.

### 5️⃣ Web Crawler
Menjelajahi website sampai 30 halaman, mengumpulkan semua link & form (GET/POST). Hasilnya jadi bahan untuk modul scanner lain.

### 6️⃣ SQL Injection
Menguji setiap parameter URL dan field form dengan 9 payload:
- **Error-based** — cari pesan error MySQL/Oracle/PostgreSQL/SQLite
- **Time-based** — payload `SLEEP()` dan ukur delay respons
- Deteksi HTTP 500 akibat quote (indikasi SQLi)

### 7️⃣ XSS Scanner
Menyuntik 6 payload (`<script>`, `<img onerror>`, `<svg onload>`, dst) ke parameter & form. Kalau payload terpantulkan mentah di response → **Reflected XSS** (HIGH).

### 8️⃣ LFI / Path Traversal
Menguji payload `../../etc/passwd` (plus varian encoding `..%2f` dan `php://filter`). Kalau isi `/etc/passwd` muncul → **CRITICAL**.

### 9️⃣ Command Injection
Menguji `;id`, `|id`, `` `id` ``, `$(id)`, `&whoami` di parameter. Kalau output `uid=` / `groups=` muncul → **CRITICAL**.

### 🔟 Open Redirect
Fokus ke parameter `url`, `redirect`, `next`, `goto`, dll. Kalau server mengalihkan ke domain asing (`evil.com`) → **MEDIUM**.

### 1️⃣1️⃣ Security Header Check
Memeriksa keberadaan header keamanan: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` + flag cookie `HttpOnly`/`Secure`.

### 1️⃣2️⃣ SSL/TLS Check
Verifikasi sertifikat: masa berlaku (< 30 hari = warning), kecocokan hostname vs SAN, sertifikat invalid, dan protokol TLS usang (TLSv1 / TLSv1.1).

### 1️⃣3️⃣ Directory & File Brute Force
Menguji ±35 path umum (`/admin`, `/.env`, `/.git`, `/phpmyadmin`, `/backup`, dll). File sensitif yang bisa diakses publik di-flag **HIGH**. Juga membaca `robots.txt` untuk entri `Disallow`.

### 1️⃣4️⃣ CMS / Platform Check
Deteksi CMS & file sensitif: WordPress (`/wp-login.php`), Joomla, Drupal, PrestaShop, phpMyAdmin, repo `.git`, file `.env`, `composer.json`.

### 1️⃣5️⃣ Laporan
Membuat 3 file laporan di folder `reports/` (lihat bagian berikutnya).

---

## 📊 Laporan Hasil Scan

Setelah scan, folder `reports/` berisi:

| File | Isi |
|------|-----|
| `report_YYYYMMDD_HHMMSS.html` | Laporan visual, tinggal buka di browser 🌐 |
| `scan_YYYYMMDD_HHMMSS.txt` | Ringkasan teks untuk arsip |
| `scan_YYYYMMDD_HHMMSS.json` | Data mentah — mudah di-parse oleh tool lain |

Setiap temuan punya **severity**: `CRITICAL` → `HIGH` → `MEDIUM` → `LOW` → `INFO`, diurutkan dari yang paling berbahaya.

---


## 🤝 Kontribusi

1. Fork repo ini
2. Buat branch fitur: `git checkout -b fitur-baru`
3. Commit: `git commit -m "add: fitur baru"`
4. Push: `git push origin fitur-baru`
5. Buka **Pull Request** 🚀

---

## 📄 License

MIT License — bebas dipakai dan dimodifikasi untuk keperluan yang **legal dan beretika**.

---

<div align="center">

**⭐ Kasih bintang kalau tool ini bermanfaat! ⭐**

</div>
