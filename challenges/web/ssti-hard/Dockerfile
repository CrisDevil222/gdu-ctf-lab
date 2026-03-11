FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
ENV FLAG=CTF{ssti_jinja2_rce_m4st3r}
CMD ["python", "app.py"]