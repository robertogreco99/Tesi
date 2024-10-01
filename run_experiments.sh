#!/bin/bash

# Input video directory
INPUT_DIR="/inputs"
# Output results directory
OUTPUT_DIR="/results"
# Hash directory
HASH_DIR="/hash"

# VMAF model
MODEL_VERSION="vmaf_v0.6.1"
# Dataset
DATASET="KUGVD"
# Width
WIDTH=1920
# Height
HEIGHT=1080
# Bitrate
BITRATE=600
# Video codec
VIDEO_CODEC="x264"
# Pixel format
PIXEL_FORMAT=420
# BIT DEPTH
BIT_DEPTH=8

# Print of the variables
echo "MODEL_VERSION: $MODEL_VERSION"
echo "database: $DATASET"
echo "width: $WIDTH"
echo "height: $HEIGHT"
echo "bitrate: $BITRATE"
echo "video_codec: $VIDEO_CODEC"
echo "PIXEL FORMAT: $PIXEL_FORMAT"
echo "BITDEPTH: $BIT_DEPTH"

# Check of existing input directory
if [ ! -d "$INPUT_DIR" ]; then
    echo "Errore: la directory di input '$INPUT_DIR' non esiste."
    exit 1
fi

# Check of existing output directory
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Errore: la directory di output '$OUTPUT_DIR' non esiste."
    exit 1
fi

# Check of existing hash directory
if [ ! -d "$HASH_DIR" ]; then
    echo "Errore: la directory hash '$HASH_DIR' non esiste."
    exit 1
fi

# Function for decoding and VMAF evaluation
video_coding_vmafevaluation() {
    distorted=$1
    original=$2

    output_hash="$HASH_DIR/${distorted}_decoded.md5"

    echo "Input distorted file: $distorted"
    echo "Original YUV file: $original"

    # Output YUV file name decoded ( file decodificato)
    output_yuv="$OUTPUT_DIR/${distorted}_decoded.yuv"


     # Print the name of the output file
    echo "Output YUV: $output_yuv"

    # Decode the video
    ffmpeg -i "$INPUT_DIR/$distorted" -pix_fmt yuv420p -f rawvideo "$output_yuv"

   

    # MD5 hash of decoded YUV file
    echo "Hash MD5 for $output_yuv..."
    md5sum "$output_yuv" > "$output_hash"
    echo "Hash saved in $output_hash."

    # VMAF evaluation
    /vmaf-3.0.0/libvmaf/build/tools/vmaf \
       --reference "$INPUT_DIR/$original" \
        --distorted "$output_yuv" \
        --width "$WIDTH" \
        --height "$HEIGHT" \
        --pixel_format "$PIXEL_FORMAT" \
        --bitdepth "$BIT_DEPTH" \
        --model version="$MODEL_VERSION" \
        --feature psnr \
        --output "$OUTPUT_DIR/result__${DATASET}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}.json" \
        --json
}

# Check on input directory to see if there are YUV videos
for original_file in "$INPUT_DIR"/*.yuv; do
    if [ -f "$original_file" ]; then
        # Check for MP4 files
        for distorted_file in "$INPUT_DIR"/*.mp4; do
            if [ -f "$distorted_file" ]; then
                # Extract filenames
                distorted=$(basename "$distorted_file")
                original=$(basename "$original_file")
                video_coding_vmafevaluation "$distorted" "$original"
            else
                echo "Nessun file video MP4 trovato in '$INPUT_DIR'."
            fi
        done
    else
        echo "Nessun file YUV trovato in '$INPUT_DIR'."
    fi
done
