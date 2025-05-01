FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=on
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update -y && apt install python3 -y && apt install pip -y && \
pip3 install requests --break-system-packages && \
pip3 install yt-dlp --break-system-packages && \
pip3 install flask --break-system-packages


WORKDIR /root
COPY main.py .

ENTRYPOINT ["python3", "main.py"]
EXPOSE 15000