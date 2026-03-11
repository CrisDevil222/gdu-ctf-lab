FROM python:3.11-slim
WORKDIR /app
RUN pip install flask pillow
COPY app.py .
ENV FLAG=CTF{lsb_st3g0_r3d_ch4nn3l_s3cr3t}
CMD ["python", "app.py"]