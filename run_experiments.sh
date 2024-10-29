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

    final_decoded_file="$distorted_decoded_yuv"

    #Output json 
    output_json="$OUTPUT_DIR/result__${DATASET}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}.json"
    #Width and height
    width_old="$WIDTH"
    height_old="$HEIGHT"

    # Resize if dimensions are not 1920x1080
    if [ "$WIDTH" -ne 1920 ] || [ "$HEIGHT" -ne 1080 ]; then
    echo "Resizing video to 1920x1080..."
    echo "distorted_decoded_yuv : $distorted_decoded_yuv"
    echo "WIDTH : $WIDTH"
    echo "HEIGHT : $HEIGHT"
    #ffmpeg -s "$WIDTH"x"$HEIGHT" -i "$distorted_decoded_yuv"  -vf scale=1920x1080:flags=lanczos:param0=3 -sws_flags lanczos+accurate_rnd+full_chroma_int -pix_fmt yuv420p  "$distorted_decoded_resized_yuv"
   
    ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv420p -r 30 -i "$distorted_decoded_yuv" \
   -vf scale=1920x1080:flags=lanczos:param0=3 \
   -sws_flags lanczos+accurate_rnd+full_chroma_int \
   -pix_fmt yuv420p -r 30 -f rawvideo "$distorted_decoded_resized_yuv"

    final_decoded_file="$distorted_decoded_yuv"
    #distorted_decoded_yuv="$distorted_decoded_resized_yuv"
    output_hash="$HASH_DIR/${distorted}_decoded_resized.md5"
    width_new=1920
    height_new=1080
    output_json="$OUTPUT_DIR/result__${DATASET}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
    
    else
    echo "No resizing needed. Dimensions are already 1920x1080."
    width_new="$width_old"
    height_new="$height_old"
    fi

    # MD5 hash of decoded YUV file
    #echo "Hash MD5 for $distorted_decoded_yuv..."
    echo "Hash MD5 for $final_decoded_file..."
    md5sum "$final_decoded_file" > "$output_hash"
    #md5sum "$distorted_decoded_yuv" > "$output_hash"
    echo "Hash saved in $output_hash."

    # Convert FEATURES string to an array
    # sep is ','; read from FEATURES and push into the feature_array the elmemnents
    IFS=',' read -r -a feature_array <<< "$FEATURES"

    # Prepare features argument for VMAF command
    feature_args=""
    for feature in "${feature_array[@]}"; do
        feature_args+="--feature $feature "
    done

   if [[ "${MODEL_VERSION}" == "vmaf_b_v0.6.3.json" ]]; then
     model_version="vmaf_b_v0.6.3"
     path="version=${model_version}"
     echo "Path : $path"
   elif [[ "${MODEL_VERSION}" == "vmaf_float_b_v0.6.3.json" ]]; then
     model_version="vmaf_float_b_v0.6.3"
     path="version=${model_version}"
     echo "Path : $path"
   else
    path="path=/vmaf-3.0.0/model/${MODEL_VERSION}"
    echo "Path : $path"
   fi

       # --model path=/vmaf-3.0.0/model/${MODEL_VERSION}\

    #--distorted "$distorted_decoded_yuv" \

    # VMAF evaluation
    /vmaf-3.0.0/libvmaf/build/tools/vmaf \
       --reference "$INPUT_REFERENCE_DIR/$original" \
        --distorted "$final_decoded_file" \
        --width "$width_new" \
        --height "$height_new" \
        --pixel_format "$PIXEL_FORMAT" \
        --bitdepth "$BIT_DEPTH" \
        --model "$path"\
        $feature_args \
        --output "$output_json" --json 
        #\
        #--output "$OUTPUT_DIR/result__${DATASET}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}.json" \
        #--json
        
    if [ -f "$distorted_decoded_yuv" ]; then
    rm "$distorted_decoded_yuv"
    echo "Decoded file removed: $distorted_decoded_yuv"
    fi

    if [ -f "$distorted_decoded_resized_yuv" ]; then
    rm "$distorted_decoded_resized_yuv"
    echo "Decoded resized file removed: $distorted_decoded_resized_yuv"
    fi

    #RUN PYTHON 
    #python3 analyze.py {dataset} {width} {height} {bitrate} {video_codec} {model_version}  /results {original_video}'
    echo "Dataset: $DATASET"
    echo "Width: $width_new"
    echo "Height: $height_new"
    echo "Bitrate: $BITRATE"
    echo "Video Codec: $VIDEO_CODEC"
    echo "Model Version: $MODEL_VERSION"
    echo "Output Directory: $OUTPUT_DIR"
    echo "Original Video: $ORIGINAL_VIDEO"
    echo "Old WIDTH : $width_old"
    echo "Old HEIGHT : $height_old"

    
    python3 analyze.py "$DATASET" "$width_new" "$height_new" "$BITRATE" "$VIDEO_CODEC" "$MODEL_VERSION" "$OUTPUT_DIR" "$ORIGINAL_VIDEO" "$width_old" "$height_old"


