# 🏴 GDU CTF Lab Platform

Nền tảng thực hành CTF nội bộ toàn diện được thiết kế đặc biệt cho sinh viên, đi từ các khái niệm Cơ bản (Easy) đến Nâng cao (Hard), bao phủ 6 mảng chính của An toàn thông tin.

## 📁 Cấu trúc chung

```text
gdu-ctf-lab/
├── docker-compose.yml          # Tệp cấu hình khởi động toàn bộ hạ tầng
├── Landing/                    # Trang chủ điều hướng (GDU Library/Dashboard)
├── nginx/                      # Cấu hình Reverse Proxy chuyển tiếp traffic
├── deploy.sh                   # Script triển khai tự động lên Cloud VM
├── ROADMAP.md                  # Lộ trình học + Hướng dẫn giải chi tiết
└── challenges/                 # Chứa mã nguồn của từng thử thách
    ├── web/                    # Lỗ hổng ứng dụng Web (SQLi, XSS, SSRF, SSTI...)
    ├── crypto/                 # Mật mã học (Caesar, Dynastic...)
    ├── forensics/              # Điều tra số (PCAP, Malware, SOC, Stego...)
    ├── re/                     # Dịch ngược phần mềm (Strings, XOR...)
    ├── pwn/                    # Khai thác lỗ hổng phần mềm (Buffer Overflow...)
    ├── misc/                   # Kịch bản khác (Linux Quiz, Morse...)
    └── osint/                  # Thu thập tình báo nguồn mở
```

## 🚀 Hướng dẫn Khởi động

Để triển khai toàn bộ hệ thống (gồm 25+ dịch vụ) trên cùng một máy, bạn chỉ cần chạy lệnh sau trên môi trường có cài đặt sẵn Docker và Docker Compose:

```bash
# Chọn thư mục
cd gdu-ctf-lab

# Xây dựng và khởi động chạy ngầm tất cả các dịch vụ
docker compose up -d --build
```

Để dừng hệ thống:
```bash
docker compose down
```

## 🌐 Bảng định tuyến Cổng (Ports Map)

| Category | Challenge / Service | Port |
|----------|---------------------|------|
| **Core** | Nginx Reverse Proxy | `80` |
| **Core** | CTFd Platform       | `8000` |
| **Core** | Landing Page        | `5000` |
| **Web**  | SQL Injection (Easy)| `5001` |
| **Web**  | XSS Stored (Easy)   | `5002` |
| **Web**  | IDOR (Medium)       | `5003` |
| **Web**  | SSTI Jinja2 (Hard)  | `5004` |
| **Web**  | Path Traversal (Easy)| `5005` |
| **Web**  | SQLi UNION (Medium) | `5006` |
| **Web**  | SSRF (Medium)       | `5007` |
| **Crypto**| Caesar Cipher (Easy)| `6001` |
| **Crypto**| Dynastic (Medium)   | `6002` |
| **Forensics**| Steganography (Easy)| `7001` |
| **Forensics**| Malware Analysis | `1337` (Netcat)|
| **Forensics**| SOC Data Exfil   | `1334` (Netcat)|
| **RE**   | Strings (Easy)      | `8001` |
| **RE**   | XOR (Easy)          | `8002` |
| **Pwn**  | Buffer Overflow (Easy) | `9001` |
| **Pwn**  | Ret2Win (Easy)      | `9002` |
| **Misc** | Morse Code (Easy)   | `10001` |
| **Misc** | Linux Quiz          | `7777` (Netcat)|
| **OSINT**| Metadata (Easy)     | `11001` |

## 📖 Tài liệu học tập

Vui lòng tham khảo tệp `ROADMAP.md` để xem lộ trình học tập, thông tin chi tiết từng mảng và lời giải (write-ups) mẫu cho các bài tập. Thay vì giải bừa, hãy đi theo lộ trình để xây dựng nền tảng vững chắc nhất!
