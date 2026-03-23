#!/usr/bin/env python3
import socket
import sys
import time

FLAG = "CTF{l1nux_m4st3r_c0mm4nd_g0d}"

QUESTIONS = [
    {
        "q": "Lệnh nào dùng để xem nội dung file trong Linux?",
        "choices": ["A. dir", "B. cat", "C. show", "D. read"],
        "answer": "B",
        "explain": "cat <file> hiển thị nội dung file ra stdout."
    },
    {
        "q": "Lệnh nào dùng để xem IP address của máy?",
        "choices": ["A. ipconfig", "B. ifconfig / ip a", "C. netstat", "D. ping"],
        "answer": "B",
        "explain": "ifconfig (cũ) hoặc ip a (mới) để xem network interfaces."
    },
    {
        "q": "Lệnh nào để thay đổi quyền file trong Linux?",
        "choices": ["A. chown", "B. chmod", "C. chgrp", "D. chperm"],
        "answer": "B",
        "explain": "chmod 755 file.sh để set quyền read/write/execute."
    },
    {
        "q": "Lệnh nào để xem process đang chạy?",
        "choices": ["A. top / ps", "B. list", "C. proc", "D. run"],
        "answer": "A",
        "explain": "ps aux hoặc top để xem danh sách process."
    },
    {
        "q": "Để chạy file script với quyền sudo, ta dùng lệnh nào?",
        "choices": ["A. sudo bash script.sh", "B. run script.sh", "C. exec script.sh", "D. start script.sh"],
        "answer": "A",
        "explain": "sudo bash script.sh hoặc sudo ./script.sh (cần chmod +x trước)."
    },
    {
        "q": "Lệnh nào để tìm file theo tên trong Linux?",
        "choices": ["A. search", "B. locate / find", "C. grep", "D. seek"],
        "answer": "B",
        "explain": "find / -name 'file.txt' hoặc locate file.txt."
    },
    {
        "q": "Lệnh nào để xem dung lượng ổ đĩa còn trống?",
        "choices": ["A. du", "B. ls -l", "C. df -h", "D. free"],
        "answer": "C",
        "explain": "df -h (disk free) hiển thị dung lượng theo đơn vị dễ đọc."
    },
    {
        "q": "Lệnh nào để giải nén file .tar.gz?",
        "choices": ["A. unzip file.tar.gz", "B. tar -xzf file.tar.gz", "C. extract file.tar.gz", "D. gunzip file.tar.gz"],
        "answer": "B",
        "explain": "tar -xzf: x=extract, z=gzip, f=filename."
    },
    {
        "q": "Để xem 10 dòng cuối của file log, ta dùng lệnh?",
        "choices": ["A. head -10 file", "B. tail -10 file", "C. last -10 file", "D. end -10 file"],
        "answer": "B",
        "explain": "tail -n 10 file hoặc tail -10 file. tail -f để theo dõi realtime."
    },
    {
        "q": "Lệnh nào để kết nối SSH đến server?",
        "choices": ["A. ssh user@ip", "B. connect user@ip", "C. telnet user@ip", "D. ftp user@ip"],
        "answer": "A",
        "explain": "ssh user@hostname -p port (mặc định port 22)."
    },
]

BANNER = r"""
╔══════════════════════════════════════════════════════╗
║         GDU-CTF — Linux Command Quiz                 ║
║         Trả lời đúng tất cả để nhận FLAG!            ║
╚══════════════════════════════════════════════════════╝
"""

def send(conn, msg):
    try:
        conn.sendall((msg + "\n").encode())
    except:
        pass

def recv(conn):
    try:
        data = b""
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                return None
            data += chunk
            if b"\n" in data:
                return data.decode(errors='ignore').strip().upper()
    except:
        return None

def handle_client(conn, addr):
    print(f"[+] New connection: {addr}")
    
    send(conn, BANNER)
    time.sleep(0.3)
    send(conn, f"Có {len(QUESTIONS)} câu hỏi về Linux.")
    send(conn, "Trả lời đúng → sang câu tiếp | Sai → reset từ câu 1\n")
    time.sleep(0.3)

    while True:
        current = 0
        send(conn, "=" * 54)
        send(conn, "  BẮT ĐẦU! Nhập A/B/C/D để trả lời.\n")

        while current < len(QUESTIONS):
            q = QUESTIONS[current]
            send(conn, f"\n[Câu {current+1}/{len(QUESTIONS)}] {q['q']}")
            for choice in q["choices"]:
                send(conn, f"  {choice}")
            send(conn, "Trả lời (A/B/C/D): ")

            answer = recv(conn)
            if answer is None:
                print(f"[-] Disconnected: {addr}")
                conn.close()
                return

            # Lấy chỉ ký tự đầu tiên
            answer = answer.strip().upper()
            if answer:
                answer = answer[0]

            if answer == q["answer"]:
                send(conn, f"\n✅ ĐÚNG! {q['explain']}")
                current += 1
                if current < len(QUESTIONS):
                    send(conn, f"➡ Tiếp tục câu {current+1}...")
                    time.sleep(0.5)
            else:
                send(conn, f"\n❌ SAI! Đáp án đúng là: {q['answer']}")
                send(conn, f"   {q['explain']}")
                send(conn, "\n💀 RESET! Quay lại câu 1...\n")
                time.sleep(1)
                break

        else:
            # Trả lời đúng hết
            send(conn, "\n" + "🎉" * 27)
            send(conn, "  CHÚC MỪNG! Bạn đã trả lời đúng tất cả câu hỏi!")
            send(conn, "🎉" * 27)
            send(conn, f"\n🚩 FLAG: {FLAG}\n")
            send(conn, "=" * 54)
            break

        # Hỏi có muốn chơi lại không
        send(conn, "\nBạn có muốn thử lại? (Y/N): ")
        ans = recv(conn)
        if ans is None or (ans and ans[0] == 'N'):
            send(conn, "Tạm biệt! Hãy thử lại sau nhé 👋\n")
            break

    conn.close()
    print(f"[-] Closed: {addr}")

def main():
    HOST = '0.0.0.0'
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 7777

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(10)
    print(f"[*] Linux Quiz Server listening on {HOST}:{PORT}")

    import threading
    while True:
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
        except KeyboardInterrupt:
            print("\n[*] Server stopped.")
            break

    server.close()

if __name__ == '__main__':
    main()