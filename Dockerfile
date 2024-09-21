# Usa l'immagine base di Alpine
FROM python:3.9-alpine

# Aggiorna gli indici dei pacchetti e installa dipendenze di base e FFmpeg
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

# Installa le librerie Python per l'analisi e la grafica
RUN pip3 install matplotlib pandas

# Clona il repository VMAF e compila la libreria
RUN git clone https://github.com/Netflix/vmaf.git /vmaf \
    && cd /vmaf/libvmaf \
    && meson build --buildtype release \
    && ninja -C build \
    && ninja -C build install

# Clona il repository di FFmpeg
RUN git clone https://git.ffmpeg.org/ffmpeg.git /ffmpeg \
    && cd /ffmpeg \
    && ./configure --enable-gpl  --enable-libvmaf --enable-libx264 --enable-libx265 --enable-libaom --enable-libvpx --enable-libvorbis --enable-libopus \
    && make -j4 \
    && make install


# Crea una directory per i video e i risultati
RUN mkdir -p /inputs /results

# Imposta la directory di lavoro
WORKDIR /app

# Copia i file necessari
COPY analyze.py .
COPY run_experiments.sh .

# Aggiungi permessi di esecuzione agli script
RUN chmod +x run_experiments.sh analyze.py

# Esegui lo script 
RUN ./run_experiments.sh

# Avvia una shell Bash
CMD ["/bin/sh"]
