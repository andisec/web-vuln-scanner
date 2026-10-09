# 🤝 Panduan Kontribusi

Terima kasih sudah mau berkontribusi ke **Auto Web Vulnerability Scanner**!

## Cara Kontribusi

1. **Fork** repository ini
2. Clone hasil fork kamu:
   `git clone https://github.com/username/web-vuln-scanner.git`
3. Buat branch baru:
   `git checkout -b fitur/nama-fitur`
4. Lakukan perubahan & commit:
   `git commit -m "feat: tambahkan fitur XXX"`
5. Push ke fork kamu:
   `git push origin fitur/nama-fitur`
6. Buka **Pull Request** ke branch `main` repo ini

## Aturan Pull Request

- ✅ Kode harus **100% Python stdlib** (tanpa `pip install`)
- ✅ Lint harus lolos: `flake8 scanner.py --max-line-length=120`
- ✅ CI (GitHub Actions) harus **hijau** sebelum di-review
- ✅ Satu PR = satu fitur/fix (jangan campur banyak hal)
- ✅ Tambahkan komentar yang jelas pada modul baru

## Format Commit (Conventional Commits)

| Prefix | Arti |
|--------|------|
| `feat:` | Fitur baru |
| `fix:` | Perbaikan bug |
| `docs:` | Perubahan dokumentasi |
| `refactor:` | Perbaikan kode tanpa perubahan fungsi |
| `perf:` | Perbaikan performa |

## Ide Pengembangan yang Ditunggu

- [ ] Deteksi CSRF
- [ ] Brute force login form
- [ ] XPath injection
- [ ] SSRF scanner
- [ ] Deteksi CORS misconfiguration
- [ ] Export laporan ke PDF
- [ ] Mode CLI non-interaktif (`--target --full-auto`)

## Kode Etik

Gunakan tool & kontribusi hanya untuk keperluan keamanan yang **legal dan beretika**.
