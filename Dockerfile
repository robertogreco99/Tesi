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
    gcc\ 
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
    libaom-dev 
   

# Python libraries for analysis and graphs
RUN pip3 install matplotlib pandas

# Download the zip of VMAF (version 3.0.0) and install libvmaf
RUN curl -L https://github.com/Netflix/vmaf/archive/refs/tags/v3.0.0.zip -o vmaf.zip \
    && unzip vmaf.zip \
    && cd vmaf-3.0.0/libvmaf \
    && meson build --buildtype release \
    && ninja -C build \
    && ninja -C build install

    


# Download the zip of FFmpeg version 7.0.2 and compile with the correct options
RUN curl -L https://github.com/FFmpeg/FFmpeg/archive/refs/tags/n7.0.2.zip -o ffmpeg.zip \
    && unzip ffmpeg.zip \
    && cd FFmpeg-n7.0.2 \
    && ./configure --enable-gpl  --enable-libvmaf --enable-libx264 --enable-libx265 --enable-libaom --enable-libvpx --enable-libvorbis --enable-libopus \
    && make -j$(nproc) \
    && make install \
    && ldconfig  
    



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