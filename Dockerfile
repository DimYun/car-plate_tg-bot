FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    python3-pip \
    make \
    wget \
    ffmpeg \
    libsm6 \
    libxext6 \
    libjpeg-dev \
    libpng-dev

WORKDIR /plate_bot

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD make run_app
