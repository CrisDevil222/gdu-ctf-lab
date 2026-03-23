#!/usr/bin/env python3
import socket
import threading
import sys

FLAG = "CTF{DID_YOU_KNOW_ABOUT_THE_TRITHEMIUS_CIPHER?!_IT_IS_SIMILAR_TO_CAESAR_CIPHER}"

BANNER = r"""
╔══════════════════════════════════════════════╗
║     GDU-CTF — Dynastic Cipher Challenge      ║
║              [ CRYPTO ]  150 pts             ║
╚══════════════════════════════════════════════╝
"""

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
        send(conn, "Giải mã ciphertext trong đề bài trên CTFd rồi submit flag tại đây.\n")

        attempts = 0
        while True:
            flag = recv_line(conn, "Flag: ")
            if flag is None:
                break

            attempts += 1
            if flag.strip() == FLAG:
                send(conn, f"\n🎉 CORRECT! Well done!")
                send(conn, f"🚩 {FLAG}")
                send(conn, f"✅ Solved in {attempts} attempt(s)!\n")
                break
            else:
                send(conn, f"❌ Wrong flag! Try again. (attempt {attempts})\n")

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
    print(f"[*] Dynastic server on {HOST}:{PORT}")

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