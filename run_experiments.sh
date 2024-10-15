#!/bin/bash

INPUT_REFERENCE_DIR="$1"   
INPUT_DISTORTED_DIR="$2"    
OUTPUT_DIR="$3"    
HASH_DIR="$4"       
MODEL_VERSION="$5"  
DATASET="$6"        
WIDTH="$7"          
HEIGHT="$8"         
BITRATE="$9"        
VIDEO_CODEC="${10}"    
PIXEL_FORMAT="${11}" 
BIT_DEPTH="${12}"
ORIGINAL_VIDEO="${13}"
DISTORTED_VIDEO="${14}"    
FEATURES="${15}" 


echo "---------------------------"
echo "Input Reference Directory: $INPUT_REFERENCE_DIR"
echo "Input Distorted Directory: $INPUT_DISTORTED_DIR"
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
echo "Original Video : $ORIGINAL_VIDEO"
echo "Distorted Video : $DISTORTED_VIDEO"
echo "Features: $FEATURES"

if [ "$#" -ne 15 ]; then
    echo "Error: Expected 15 arguments, but got $#."
    exit 1
fi



# Check of existing input directory
if [ ! -d "$INPUT_REFERENCE_DIR" ]; then
    echo "Error: input directory '$INPUT_REFERENCE_DIR' ( for reference videos ) does not exists  "
    exit 1
fi
# Check of existing input directory
if [ ! -d "$INPUT_DISTORTED_DIR" ]; then
    echo "Error: input directory '$INPUT_DISTORTED_DIR' (for distorted videos) does not exists "
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


original="$ORIGINAL_VIDEO"
distorted="$DISTORTED_VIDEO"


    #directory where to save hash file
    output_hash="$HASH_DIR/${distorted}_decoded.md5"
    # Output YUV : file name of decoded file
    distorted_decoded_yuv="$OUTPUT_DIR/${distorted}_decoded.yuv"
    # Output Resized YUV : file name of decoded file resized
    distorted_decoded_resized_yuv="$OUTPUT_DIR/${distorted}_decoded_resized.yuv"


    echo "Input distorted file: $distorted"
    echo "Original YUV file: $original"

    # Print the name of the decoded file
    echo "Decoded file: $distorted_decoded_yuv"

    # Decode the video
    ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv420p -f rawvideo "$distorted_decoded_yuv" -loglevel quiet

    # Resize if dimensions are not 1920x1080
    #if [ "$WIDTH" -ne 1920 ] || [ "$HEIGHT" -ne 1080 ]; then
    #echo "Resizing video to 1920x1080..."
    #echo "distorted_decoded_yuv : $distorted_decoded_yuv"
    #echo "WIDTH : $WIDTH"
    #echo "HEIGHT : $HEIGHT"
    #distorted_decoded_yuv="$distorted_decoded_resized_yuv"
    #output_hash="$HASH_DIR/${distorted}_decoded_resized.md5"
    #else
    #echo "No resizing needed. Dimensions are already 1920x1080."
    #fi

    # MD5 hash of decoded YUV file
    echo "Hash MD5 for $distorted_decoded_yuv..."
    md5sum "$distorted_decoded_yuv" > "$output_hash"
    echo "Hash saved in $output_hash."

    # Convert FEATURES string to an array
    IFS=',' read -r -a feature_array <<< "$FEATURES"

    # Prepare features argument for VMAF command
    feature_args=""
    for feature in "${feature_array[@]}"; do
        feature_args+="--feature $feature "
    done

    # VMAF evaluation
    /vmaf-3.0.0/libvmaf/build/tools/vmaf \
       --reference "$INPUT_REFERENCE_DIR/$original" \
        --distorted "$distorted_decoded_yuv" \
        --width "$WIDTH" \
        --height "$HEIGHT" \
        --pixel_format "$PIXEL_FORMAT" \
        --bitdepth "$BIT_DEPTH" \
        --model path=/vmaf-3.0.0/model/${MODEL_VERSION}\
        $feature_args \
        --output "$OUTPUT_DIR/result__${DATASET}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}.json" \
        --json
    



