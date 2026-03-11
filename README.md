# 🏴 CTF Lab Platform

Full CTF lab platform cho sinh viên — từ Easy đến Hard, gồm 6 mảng chính.

## 📁 Cấu trúc

```
ctf-lab/
├── docker-compose.yml          # Khởi động toàn bộ hệ thống
├── nginx/nginx.conf            # Reverse proxy
├── docs/ROADMAP.md             # Lộ trình học + hướng dẫn solve
└── challenges/
    ├── web/
    │   ├── sqli-easy/          # SQL Injection [Easy]    :5001
    │   ├── xss-easy/           # Stored XSS [Easy]       :5002
    │   ├── idor-medium/        # IDOR [Medium]            :5003
    │   └── ssti-hard/          # SSTI → RCE [Hard]       :5004
    ├── crypto/
    │   └── caesar-easy/        # Caesar/ROT13 [Easy]     :6001
    ├── forensics/
    │   └── stego-easy/         # LSB Steganography [Easy]:7001
    ├── reversing/              # (thêm sau)
    ├── pwn/                    # (thêm sau)
    └── misc/                   # (thêm sau)
```

## 🚀 Khởi động

```bash
docker-compose up -d
```

## 🌐 URLs

| Service | URL | Mô tả |
|---------|-----|-------|
| CTFd | http://localhost:8000 | Platform chính |
| SQLi | http://localhost:5001 | Web Easy |
| XSS | http://localhost:5002 | Web Easy |
| IDOR | http://localhost:5003 | Web Medium |
| SSTI | http://localhost:5004 | Web Hard |
| Caesar | http://localhost:6001 | Crypto Easy |
| Stego | http://localhost:7001 | Forensics Easy |

## 📖 Tài liệu

Xem `docs/ROADMAP.md` để biết lộ trình học và cách giải từng challenge.
