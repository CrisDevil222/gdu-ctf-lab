FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
ENV FLAG=CTF{p4th_tr4v3rs4l_d1rect0ry_l34k}
CMD ["python", "app.py"]
