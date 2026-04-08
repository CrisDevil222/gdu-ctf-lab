# 🏴 GDU CTF Lab — Full Roadmap & Challenge Guide
> Nền tảng nội bộ dành cho sinh viên GDU, lộ trình từ con số 0 đến nâng cao.

---

## 📐 Kiến trúc tổng thể

```text
Internet
    │
  Nginx (port 80)
    │
  CTFd Platform (port 8000)  ← Hệ thống Scoreboard, Auth, Submit Flag
    │
  ┌─────────────────────────────────────────────────────────────────┐
  │                 Challenge Containers (Docker)                   │
  │  Web    Crypto   Forensics   RE      Pwn     Misc    OSINT      │
  │  500X   600X     700X, 133X  800X    900X    1000X   1100X      │
  └─────────────────────────────────────────────────────────────────┘
```

---

## 🗺️ ROADMAP — Lộ trình học tập tăng tiến

### Phase 1: Nhập môn & Làm Quen (Tuần 1–2)
> **Mục tiêu:** Hiểu luồng hoạt động của cờ (Flag), thao tác Netcat cơ bản, các kỹ thuật giấu thông tin đơn giản.

| # | Category | Challenge | Kiến thức đạt được |
|---|----------|-----------|--------------------|
| 1 | Misc | Morse Easy | Dịch mã Morse, kỹ năng dùng tools online |
| 2 | Crypto | Caesar Easy | Cơ bản về dịch vòng (Shift cipher), Brute-force |
| 3 | Forensics | Stego Easy | Kỹ thuật LSB Steganography, đọc mã HEX cơ bản |
| 4 | Web | SQLi Easy | Lỗ hổng SQL Injection căn bản ở khung Login |
| 5 | OSINT | Metadata Easy | Đọc thông tin Exif của file ảnh, tài liệu |
| 6 | Misc | Linux Quiz | Thao tác lệnh Command Line Linux qua Netcat |

### Phase 2: Web & Reversing Cơ Bản (Tuần 3–4)
> **Mục tiêu:** Khám phá cấu trúc mã hóa/dịch ngược căn bản; biết dùng Burp Suite để thao túng các Request web.

| # | Category | Challenge | Kiến thức đạt được |
|---|----------|-----------|--------------------|
| 7 | Web | Path Traversal | Khai thác lỗ hổng LFI/Path Traversal đọc file `/etc/passwd` |
| 8 | Web | XSS Easy | Khai thác Stored XSS, chèn script ăn trộm Cookie |
| 9 | RE | Strings Easy | Sử dụng lệnh `strings` để rà soát mã nguồn thô |
| 10| RE | XOR Easy | Thuật toán XOR đảo ngược trong Reversing |
| 11| Crypto | Dynastic | Mật mã học thay thế theo quy luật tùy chỉnh |
| 12| Web | IDOR Medium | Can thiệp tham số định danh (Access Control Bypass) |

### Phase 3: Forensics Nâng Cao & Khai thác Bộ Nhớ (Tuần 5–6)
> **Mục tiêu:** Phân tích mã độc, điều tra vết mạng (PCAP), bước đầu làm quen với lập trình khai thác bộ nhớ (Pwn).

| # | Category | Challenge | Kiến thức đạt được |
|---|----------|-----------|--------------------|
| 13| Web | SQLi Medium | Sử dụng phương pháp UNION-Based truy xuất toàn bộ DB |
| 14| Web | SSRF Medium | Tấn công nội bộ trích xuất Cloud Metadata bằng SSRF |
| 15| Forensics| Malware Analysis | Dịch ngược và điều tra tĩnh/động mã độc (Netcat Challenge) |
| 16| Forensics| SOC CTF Chall 3 | Phân tích PCAP, EVTX, EML truy vết Hacker (Netcat CTF) |
| 17| Pwn | BOF Easy | Stack Buffer Overflow, ghi đè Return Address |
| 18| Pwn | Ret2Win Easy | Khai thác lỗ hổng gọi hàm ẩn thông qua BOF |

### Phase 4: Trùm Cuối (Tuần 7–8)
> **Mục tiêu:** Tấn công chuỗi cấu trúc phức tạp (Exploit Chains). Vượt rào bảo mật.

| # | Category | Challenge | Kiến thức đạt được |
|---|----------|-----------|--------------------|
| 19| Web | SSTI Hard | Khai thác Jinja2 Server-Side Template Injection để đạt RCE |

---

## 🗂️ CHI TIẾT TỪNG MẢNG (HƯỚNG DẪN & WRITE-UP)

### 🌐 WEB EXPLOITATION

**1. Path Traversal (Easy) - Port 5005**
* Mô tả: Một trang web đọc file thông qua tham số `?file=...`.
* Điểm học: Cách sử dụng các dấu `../` liên tục để thoát khỏi thư mục hiện tại và đọc các file nhạy cảm của hệ thống Linux.
* Payload mẫu: `?file=../../../../../etc/passwd`

**2. SQL Injection (Easy) - Port 5001**
* Mô tả: Khung Login bị lỗi xác thực chuỗi nhập liệu.
* Nâng cao (Medium - Port 5006): Sử dụng `UNION SELECT` để truy vấn vượt ngoài số lượng cột có sẵn và lôi toàn bộ bảng `users` ra ánh sáng.

**3. SSRF (Medium) - Port 5007**
* Mô tả: Ứng dụng cung cấp chức năng check URL, người dùng nhập URL và máy chủ sẽ request giùm.
* Lỗ hổng: Nếu nhập các địa chỉ IP nội bộ như `http://169.254.169.254/latest/meta-data/`, ta có thể lừa Server lấy mã bảo vệ ngầm của server.

**4. SSTI (Hard) - Port 5004**
* Mô tả: Website render thư mời dùng Jinja2 Template.
* Lỗ hổng: Chèn mã code Python thông qua cú pháp ngoặc kép `{{ 7 * 7 }}` để kiểm tra.
* Payload lấy Flag (RCE):
  ```python
  {{config.__class__.__init__.__globals__['os'].environ['FLAG']}}
  ```

---

### 🔬 FORENSICS / INCIDENT RESPONSE (SOC)

**1. Steganography (Easy) - Port 7001**
* Mục tiêu: Tìm kiếm thông tin bị giấu đi một cách khéo léo sau các điểm ảnh (Pixels) của bức ảnh.
* Tools: Stegsolve, Zsteg, Exiftool.

**2. SOC Data Exfiltration (Port 1334)**
* Thử thách: Sinh viên phải đóng vai thành viên đội SOC, phân tích lưu lượng PCAP, file MFT, nhật ký Windows (EVTX) và truy tìm Email lừa đảo (EML).
* Cách chơi: Mở Terminal gõ `nc 35.247.183.253 1334` rồi trả lời đúng 100% các câu hỏi hệ thống đưa ra để ghép nối 4 mảnh của Flag gốc lại. Tính kỷ luật và sự chú ý đến từng khoảng trắng, cấu trúc chữ hoa/thường là chìa khóa.

**3. Malware Analysis (Port 1337)**
* Thử thách dịch ngược hoạt động của mã độc thông qua Netcat.

---

### 💣 PWN / BINARY EXPLOITATION

**1. Buffer Overflow (Easy) - Port 9001**
* Ứng dụng C bị lỗi nhập liệu quá dài. Máy tính phân vùng sai đè lên bộ nhớ thực thi.
* Sinh viên dùng script Python (`pwntools`) để chèn chuỗi ký tự 'A' tràn viền và thay thế địa chỉ trả về (Return address) trỏ thẳng vào hàm kích hoạt in Flag.

---

## 🛠️ Trạm Vũ Khí Sinh Viên Cần Chuẩn Bị Trang Bị

### Cho Mảng Web
- **Burp Suite Community:** Dùng để Intercept (bắt) và sửa đổi nội dung gói tin HTTP trước khi nó bay đến Server. (Bat chuộc phải dùng).
- **sqlmap:** Tool tự động tiêm mã độc SQL - `sqlmap -u "http://..." --dbs`
- Trình duyệt tích hợp tiện ích HackBar hoặc Cookie Editor.

### Cho Mảng Crypto / RE
- **CyberChef:** Con dao thụy sĩ đỉnh nhất vũ trụ để giải và chuyển đổi mọi thể loại mã hóa.
- **Ghidra / IDA Free:** Trình biên dịch ngược phần mềm từ ngôn ngữ máy về C++ hoặc ASM.

### Cho Mảng Forensics
- **Wireshark:** Bắt và soi các gói tin mạng, đặc biệt hiệu quả ở chức năng Follow TCP/HTTP Streams.
- **Autopsy:** Công cụ điều tra hệ thống đĩa cực mạnh.

---

> *Tất cả các mô phỏng lôc hổng trên nền tảng này đều được cung cấp riêng vì mục đích giáo dục và nghiên cứu học thuật của GDU. Tuyệt đối không áp dụng các công cụ và kĩ thuật này bào các hệ thống thực tế bên ngoài khi chưa có sự cho phép bằng văn bản.*
