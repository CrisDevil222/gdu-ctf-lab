# Sử dụng Python bản nhẹ
FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file server vào container
COPY server.py .

# Mở cổng 1334 cho Netcat
EXPOSE 1334

# Chạy server (tham số -u giúp log in ra màn hình ngay lập tức)
CMD ["python3", "-u", "server.py"]