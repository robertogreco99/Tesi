#!/bin/bash

# Input video directory
INPUT_DIR="/inputs"
# Output results directory
OUTPUT_DIR="/results"
# Vmaf nodel
VMAF_MODEL="/vmaf-3.0.0/model/vmaf_v0.6.1.json"

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
input_file=$1
video_name=$(basename "$input_file" .mp4)
# Output YUV file name

output_yuv="$OUTPUT_DIR/${video_name}_decoded.yuv"
    
# Decode the video to YUV format
ffmpeg -i "$input_file" -pix_fmt yuv420p -f rawvideo "$output_yuv"
    
}

# Check on input directory to see if there are videos
for video_file in "$INPUT_DIR"/*.mp4; do
    if [ -f "$video_file" ]; then
        video_coding_vmafevaluation "$video_file"
    else
        echo "Nessun file video trovato in '$INPUT_DIR'."
    fi
done

