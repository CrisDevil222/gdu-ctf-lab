FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
ENV FLAG=CTF{xss_st0r3d_c00k13_st3al3r}
CMD ["python", "app.py"]