FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
ENV FLAG=CTF{un10n_b4s3d_sqli_m4st3r}
CMD ["python", "app.py"]
