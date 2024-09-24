# Parto dall'immagine base di alpine
FROM python:3.9-alpine

# Pacchetti necessari
RUN apk add --no-cache \
    bash \
    build-base \
    meson \
    nasm \
    yasm \
    git \
    python3-dev \
    libgcc \
    libtool \
    libpng-dev \
    jpeg-dev \
    zlib-dev \
    linux-headers \ 
    vim  \
    nano \
    x264-dev \
    x265-dev \
    libvpx-dev \
    libvorbis-dev \
    opus-dev \
    aom-dev

# Librerie pyhton per l'analisi grafica
RUN pip3 install matplotlib pandas

# Clono vmaf e installo libvmaf
RUN git clone https://github.com/Netflix/vmaf.git /vmaf \
    && cd /vmaf/libvmaf \
    && meson build --buildtype release \
    && ninja -C build \
    && ninja -C build install

# Clona il repository di FFmpeg e lo compilo con le dipendenze necessarie
RUN git clone https://git.ffmpeg.org/ffmpeg.git /ffmpeg \
    && cd /ffmpeg \
    && ./configure --enable-gpl  --enable-libvmaf --enable-libx264 --enable-libx265 --enable-libaom --enable-libvpx --enable-libvorbis --enable-libopus \
    && make -j$(nproc) \
    && make install


# Creo una directory per i video e  unai risultati
RUN mkdir -p /inputs /results

# Imposto la workdir
WORKDIR /app

# Copio gli script
COPY analyze.py .
COPY run_experiments.sh .

# Rendo script eseguibili
RUN chmod +x run_experiments.sh analyze.py

# Creazione di uno script per eseguire entrambi gli script
RUN echo -e '#!/bin/sh\n./run_experiments.sh\npython3 analyze.py' > run_both.sh && chmod +x run_both.sh

# Comando per eseguire lo script run_both.sh all'avvio del contenitore
CMD ["./run_both.sh"]