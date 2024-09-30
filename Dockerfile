# Base image 
FROM python:3.12-bookworm

# Update packages and install necessary packets
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

# Python libraries for analysis and graphs
RUN pip3 install matplotlib pandas

# Clone vmaf and install libvmaf
RUN git clone https://github.com/Netflix/vmaf.git /vmaf \
    && cd /vmaf/libvmaf \
    && meson build --buildtype release \
    && ninja -C build \
    && ninja -C build install

# Clone the ffmpeg repository to compile with the correct options
RUN git clone https://git.ffmpeg.org/ffmpeg.git /ffmpeg \
    && cd /ffmpeg \
    && ./configure --enable-gpl  --enable-libvmaf --enable-libx264 --enable-libx265 --enable-libaom --enable-libvpx --enable-libvorbis --enable-libopus \
    && make -j$(nproc) \
    && make install


# Create a directory for videos and results
RUN mkdir -p /inputs /results

# Set the working directory
WORKDIR /app

# Copy scripts
COPY analyze.py .
COPY run_experiments.sh .

# Make scripts executable
RUN chmod +x run_experiments.sh analyze.py

CMD ["/bin/sh"]