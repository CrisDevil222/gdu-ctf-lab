#!/usr/bin/env python3
import socket
import threading
import time
import sys

FLAG = "CTF{DID_YOU_KNOW_ABOUT_THE_TRITHEMIUS_CIPHER?!_IT_IS_SIMILAR_TO_CAESAR_CIPHER}"

CIPHERTEXT = "DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL"

SOURCE_CODE = '''def to_identity_map(a):
    return ord(a) - 0x41

def from_identity_map(a):
    return chr(a % 26 + 0x41)

def encrypt(m):
    c = ''
    for i in range(len(m)):
        ch = m[i]
        if not ch.isalpha():
            ech = ch
        else:
            chi = to_identity_map(ch)
            ech = from_identity_map(chi + i)
        c += ech
    return c'''

STORY = """
Bạn thấy mình bị mắc kẹt trong một buồng khí kín, và đột nhiên,
không gian bị xé toạc bởi âm thanh méo mó phát ra từ một đoạn băng ghi âm.
Qua giọng nói rùng rợn ấy, bạn phát hiện rằng chỉ trong vòng 15 phút tới,
căn phòng này sẽ bị ngập tràn khí hydrogen cyanide — một loại khí chết người.

Bóng tối bao trùm, tay phải bị còng lại, cánh cửa thoát hiểm đã bị khóa.
Cả còng tay lẫn cánh cửa đều yêu cầu cùng một mã số để mở khóa.

Những ngón tay run rẩy chạm vào một chiếc đèn pin. Ánh sáng mờ nhạt
hé lộ những ký tự bí ẩn được khắc lên tường cùng bức vẽ ghê rợn
về một vị hoàng đế La Mã bằng máu...
"""

BANNER = r"""
╔══════════════════════════════════════════════════════════╗
║          GDU-CTF — Dynastic Cipher Challenge             ║
║                   [ CRYPTO ]  150 pts                    ║
╚══════════════════════════════════════════════════════════╝
"""

HINTS = [
    "Gợi ý 1: Nhìn vào source code — hàm encrypt() dịch mỗi ký tự theo VỊ TRÍ của nó (i).",
    "Gợi ý 2: Để giải mã, làm ngược lại: chi = to_identity_map(ch) - i, rồi from_identity_map(chi).",
    "Gợi ý 3: Script giải mã:\n  c = ciphertext\n  for i,ch in enumerate(c):\n      if ch.isalpha():\n          print(chr((ord(ch)-0x41-i)%26+0x41),end='')\n      else: print(ch,end='')",
]

def send(conn, msg):
    try:
        conn.sendall((msg + "\n").encode())
    except:
        pass

def recv_line(conn, prompt=""):
    try:
        if prompt:
            conn.sendall(prompt.encode())
        data = b""
        while True:
            chunk = conn.recv(1)
            if not chunk:
                return None
            if chunk == b"\n":
                return data.decode(errors='ignore').strip()
            data += chunk
    except:
        return None

def handle_client(conn, addr):
    print(f"[+] Connection: {addr}")
    try:
        send(conn, BANNER)
        time.sleep(0.3)
        send(conn, STORY)
        time.sleep(0.5)
        send(conn, "=" * 58)
        send(conn, "📜 Những ký tự trên tường:")
        send(conn, f"\n  {CIPHERTEXT}\n")
        send(conn, "=" * 58)
        send(conn, "\n📄 Source code tìm được gần đó:\n")
        send(conn, SOURCE_CODE)
        send(conn, "\n" + "=" * 58)
        send(conn, "Giải mã thông điệp, bọc trong CTF{} và submit!\n")

        hint_used = 0
        attempts = 0

        while True:
            send(conn, "\n[1] Submit flag")
            send(conn, "[2] Xem gợi ý")
            send(conn, "[3] Xem lại ciphertext")
            send(conn, "[0] Thoát")

            choice = recv_line(conn, "\nLựa chọn: ")
            if choice is None:
                break

            if choice == "1":
                attempts += 1
                flag = recv_line(conn, "Nhập flag: ")
                if flag is None:
                    break

                if flag.strip() == FLAG:
                    send(conn, "\n🎉 CHÍNH XÁC! Còng tay bật ra, cửa mở toang!")
                    send(conn, f"🚩 FLAG: {FLAG}")
                    send(conn, f"\n✅ Giải được sau {attempts} lần thử!")
                    break
                else:
                    send(conn, f"❌ Sai! Khí độc ngày càng đặc hơn... (lần {attempts})")
                    if attempts >= 3:
                        send(conn, "💀 Gợi ý: Đảm bảo bạn bọc trong CTF{} và viết HOA.")

            elif choice == "2":
                if hint_used < len(HINTS):
                    send(conn, f"\n{HINTS[hint_used]}")
                    hint_used += 1
                    if hint_used < len(HINTS):
                        send(conn, f"(Còn {len(HINTS)-hint_used} gợi ý)")
                    else:
                        send(conn, "(Đã dùng hết gợi ý!)")
                else:
                    send(conn, "Đã dùng hết gợi ý!")

            elif choice == "3":
                send(conn, f"\n  {CIPHERTEXT}\n")

            elif choice == "0":
                send(conn, "💀 Căn phòng ngập đầy khí độc... Game over!")
                break
            else:
                send(conn, "Lựa chọn không hợp lệ!")

    except Exception as e:
        print(f"[!] Error {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Closed: {addr}")

def main():
    HOST = '0.0.0.0'
    PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 6002

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(20)
    print(f"[*] Dynastic Cipher Server on {HOST}:{PORT}")

    while True:
        try:
            conn, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
        except KeyboardInterrupt:
            print("\n[*] Stopped.")
            break

    server.close()

if __name__ == '__main__':
    main()