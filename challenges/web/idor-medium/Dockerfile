FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
ENV FLAG=CTF{1d0r_n0_auth_ch3ck_byp4ss}
CMD ["python", "app.py"]