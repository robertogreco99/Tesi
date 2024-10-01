#!/bin/bash

# Input video directory
INPUT_DIR="/inputs"
# Output results directory
OUTPUT_DIR="/results"
# Vmaf nodel
VMAF_MODEL="/vmaf-3.0.0/model/vmaf_v0.6.1.json"
# Hash directory
HASH_DIR="/hash"  

# Check of existing input directory
if [ ! -d "$INPUT_DIR" ]; then
    echo "Errore: la directory di input '$INPUT_DIR' non esiste."
    exit 1
fi

# Decode plus vmaf evaluation

# -i input file
# -pix_fmt yuv420p: output pixel format is YUV 4:2:0
# -f rawvideo output is rawvideo
##FIFA17_decoded.yuv: output yuv file name

video_coding_vmafevaluation(){
distorted=$1
original=$2

 
output_hash="$HASH_DIR/decoded_file.md5"

echo "Input distorted file: $distorted"
echo "Original YUV file: $original"

# Output YUV file name
output_yuv="$OUTPUT_DIR/FIFA17_30fps_30sec_v2_1920x1080_600_x264_mp4_decoded.yuv"


# Decode the video
ffmpeg -i "$distorted" -pix_fmt yuv420p -f rawvideo "$output_yuv"

# Print the name of the output file
echo "Output YUV: $output_yuv"

#  MD5 hash of decoded YUV file
echo "Hash MD5 per $output_yuv..."
md5sum "$output_yuv" > "$output_hash"
echo "Hash saved in $output_hash."



# VMAF evaluation
    /vmaf-3.0.0/libvmaf/build/tools/vmaf \
        --reference "$original" \
        --distorted "$output_yuv" \
        --width 1920 \
        --height 1080 \
        --pixel_format 420 \
        --bitdepth 8 \
        --model version=vmaf_v0.6.1 \
        --feature psnr \
        --output "$OUTPUT_DIR/result__KUGVD__1920x1080_600_x264__vmaf_v0.6.1.json" \
        --json
}

# Check on input directory to see if there are YUV videos
for original in "$INPUT_DIR"/*.yuv; do
    if [ -f "$original" ]; then
        for distorted in "$INPUT_DIR"/*.mp4; do
            if [ -f "$distorted" ]; then
                video_coding_vmafevaluation "$distorted" "$original"
            else
                echo "Nessun file video MP4 trovato in '$INPUT_DIR'."
            fi
        done
    else
        echo "Nessun file video YUV trovato in '$INPUT_DIR'."
    fi
done
