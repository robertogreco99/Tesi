#!/bin/bash

# Input video directory
#INPUT_DIR="/inputs"
# Output results directory
#OUTPUT_DIR="/results"
# Hash directory
#HASH_DIR="/hash"

# VMAF model
#MODEL_VERSION="vmaf_v0.6.1"
# Dataset
#DATASET="KUGVD"
# Width
#WIDTH=1920
# Height
#HEIGHT=1080
# Bitrate
#BITRATE=600
# Video codec
#VIDEO_CODEC="x264"
# Pixel format
#PIXEL_FORMAT=420
# BIT DEPTH
#BIT_DEPTH=8

INPUT_DIR="$1"     
OUTPUT_DIR="$2"    
HASH_DIR="$3"       
MODEL_VERSION="$4"  
DATASET="$5"        
WIDTH="$6"          
HEIGHT="$7"         
BITRATE="$8"        
VIDEO_CODEC="$9"    
PIXEL_FORMAT="${10}" 
BIT_DEPTH="${11}"    


echo "Eseguendo con i seguenti parametri:"
echo "Input Directory: $INPUT_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo "Hash Directory: $HASH_DIR"
echo "Model Version: $MODEL_VERSION"
echo "Dataset: $DATASET"
echo "Width: $WIDTH"
echo "Height: $HEIGHT"
echo "Bitrate: $BITRATE"
echo "Video Codec: $VIDEO_CODEC"
echo "Pixel Format: $PIXEL_FORMAT"
echo "Bit Depth: $BIT_DEPTH"


# Check of existing input directory
if [ ! -d "$INPUT_DIR" ]; then
    echo "Error: input directory '$INPUT_DIR' does not exists "
    exit 1
fi

# Check of existing output directory
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Error: output directory '$OUTPUT_DIR' does not exists"
    exit 1
fi

# Check of existing hash directory
if [ ! -d "$HASH_DIR" ]; then
    echo "Error : hash directory '$HASH_DIR' does not exists"
    exit 1
fi

# Function for decoding and VMAF evaluation
video_coding_vmafevaluation() {
    distorted=$1 #distorted video
    original=$2 # orginal video

    #directory where to save hash file
    output_hash="$HASH_DIR/${distorted}_decoded.md5"

    echo "Input distorted file: $distorted"
    echo "Original YUV file: $original"

    # Output YUV : file name of decoded file
    distorted_decoded_yuv="$OUTPUT_DIR/${distorted}_decoded.yuv"


    # Print the name of the decoded file
    echo "Decoded file: $distorted_decoded_yuv"

    # Decode the video
    ffmpeg -i "$INPUT_DIR/$distorted" -pix_fmt yuv420p -f rawvideo "$distorted_decoded_yuv"

   

    # MD5 hash of decoded YUV file
    echo "Hash MD5 for $distorted_decoded_yuv..."
    md5sum "$distorted_decoded_yuv" > "$output_hash"
    echo "Hash saved in $output_hash."

    # VMAF evaluation
    /vmaf-3.0.0/libvmaf/build/tools/vmaf \
       --reference "$INPUT_DIR/$original" \
        --distorted "$distorted_decoded_yuv" \
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
                echo "No mp4 file founded '$INPUT_DIR'."
            fi
        done
    else
        echo " No yuv file founded in '$INPUT_DIR'."
    fi
done
