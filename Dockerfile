# Parto dall'immagine base di Debian Bookworm
FROM python:3.12-bookworm

# Aggiornare i pacchetti e installare pacchetti necessari
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    build-essential \
    meson \
    nasm \
    yasm \
    git \
    python3-dev \
    gcc \ 
    libtool \
    libpng-dev \
    libjpeg-dev \
    zlib1g-dev \
    linux-headers-amd64 \  
    vim \
    nano \
    libx264-dev \
    libx265-dev \
    libvpx-dev \
    libvorbis-dev \
    libopus-dev \
    libaom-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

    # Librerie di python per fare le analisi e i grafici
RUN pip3 install matplotlib pandas

# Clono vmaf e installo libvmaf
RUN git clone https://github.com/Netflix/vmaf.git /vmaf \
    && cd /vmaf/libvmaf \
    && meson build --buildtype release \
    && ninja -C build \
    && ninja -C build install

# Clono il repository di ffmpeg per compilare con le opzioni giuste
RUN git clone https://git.ffmpeg.org/ffmpeg.git /ffmpeg \
    && cd /ffmpeg \
    && ./configure --enable-gpl  --enable-libvmaf --enable-libx264 --enable-libx265 --enable-libaom --enable-libvpx --enable-libvorbis --enable-libopus \
    && make -j$(nproc) \
    && make install


# Creo una directory per i video e  unai risultati
RUN mkdir -p /inputs /results

# Imposto al workdir
WORKDIR /app

# Copio gli script
COPY analyze.py .
COPY run_experiments.sh .

# Rendo script eseguibili
RUN chmod +x run_experiments.sh analyze.py

CMD ["/bin/sh"]