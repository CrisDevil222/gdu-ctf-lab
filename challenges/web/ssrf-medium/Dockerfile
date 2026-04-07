FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
ENV FLAG=CTF{ssrf_r3qu3st_f0rg3ry_pwn3d}
CMD ["python", "app.py"]
