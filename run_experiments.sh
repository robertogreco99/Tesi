#!/bin/bash

#if [ "$#" -ne 18 ]; then
#    echo "Error: Expected 18 arguments, but got $#."
#    exit 1
#fi



INPUT_REFERENCE_DIR="$1"   
INPUT_DISTORTED_DIR="$2"    
OUTPUT_DIR="$3"    
HASH_DIR="$4"  
MOS_DIR="$5"     
MODEL_VERSION="$6"  
DATASET="$7"        
WIDTH="$8"          
HEIGHT="$9"         
BITRATE="${10}"        
VIDEO_CODEC="${11}"    
PIXEL_FORMAT="${12}" 
BIT_DEPTH="${13}"
FPS="${14}"
DURATION="${15}"
ORIGINAL_VIDEO="${16}"
DISTORTED_VIDEO="${17}"    
FEATURES="${18}" 


echo "---------------------------"
echo "Input Reference Directory: $INPUT_REFERENCE_DIR"
echo "Input Distorted Directory: $INPUT_DISTORTED_DIR"
echo "Output Directory: $OUTPUT_DIR"
echo "Hash Directory: $HASH_DIR"
echo "MOS Directory: $MOS_DIR"
echo "Model Version: $MODEL_VERSION"
echo "Dataset: $DATASET"
echo "Width: $WIDTH"
echo "Height: $HEIGHT"
echo "Bitrate: $BITRATE"
echo "Video Codec: $VIDEO_CODEC"
echo "Pixel Format: $PIXEL_FORMAT"
echo "Bit Depth: $BIT_DEPTH"
echo "FPS : $FPS"
echo "Duration : $DURATION"
echo "Original Video : $ORIGINAL_VIDEO"
echo "Distorted Video : $DISTORTED_VIDEO"
echo "Features: $FEATURES"

# Check if directories exist
for dir in "$INPUT_REFERENCE_DIR" "$INPUT_DISTORTED_DIR" "$OUTPUT_DIR" "$HASH_DIR"; do
    if [ ! -d "$dir" ]; then
        echo "Error: Directory '$dir' does not exist."
        exit 1
    fi
done

FILE_COMMANDS="$OUTPUT_DIR/$DATASET/analyzescriptcommands_${DATASET}.txt"


if [ ! -f "$FILE_COMMANDS" ]; then
    touch "$FILE_COMMANDS"
fi

#Set filenames :

original="$ORIGINAL_VIDEO"
echo "Original YUV file: $original"
distorted="$DISTORTED_VIDEO"
echo "Input distorted file: $distorted"
#directory where to save hash file
output_hash="$HASH_DIR/${distorted}_decoded.md5"
# Output YUV : file name of decoded file
#disto1rted_decoded_yuv="$OUTPUT_DIR/${distorted}_decoded.yuv"
if [[ "$DATASET" == "ITS4S" ]] || [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
    # If dataset is AGHI, set decoded file extension to .y4m
    distorted_decoded="$OUTPUT_DIR/${distorted}_decoded.y4m"
else
    # Default extension is .yuv
    distorted_decoded="$OUTPUT_DIR/${distorted}_decoded.yuv"
fi

if [[ "$DATASET" == "ITS4S" ]]; then
    original_converted_to420p="$OUTPUT_DIR/${original}_420p.y4m"
    if [[ ! -f "$original_converted_to420p" ]]; then
        ffmpeg -i "$INPUT_REFERENCE_DIR/$original" -pix_fmt yuv420p "$original_converted_to420p" -loglevel quiet
        echo "OriginalConvertedtoy4m: $original_converted_to420p"
    fi
fi



# Print the name of the decoded file
echo "Decoded file: $distorted_decoded"
# Output Resized YUV : file name of decoded file resized
if [[ "$DATASET" == "ITS4S" ]] || [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
 distorted_decoded_resized="$OUTPUT_DIR/${distorted}_decoded_resized.y4m"
else
 distorted_decoded_resized="$OUTPUT_DIR/${distorted}_decoded_resized.yuv"
fi

##create the directory if absent
mkdir -p "$OUTPUT_DIR/${DATASET}/vmaf_results"
 #Output json 
output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}.json"

if [[ "$DATASET" == "ITS4S" ]]; then
    if [ ! -f "$distorted_decoded" ]; then
        ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv420p "$distorted_decoded" -loglevel quiet
    else
        echo "File already exists: $distorted_decoded"
    fi
elif [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
    if [ ! -f "$distorted_decoded" ]; then
        cp "$INPUT_DISTORTED_DIR/$distorted" "$distorted_decoded"
        #ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv422p "$distorted_decoded" -loglevel quiet
    else
        echo "File already exists: $distorted_decoded"
    fi
elif [[ "$DATASET" == "AVT-VQDB-UHD-1_1" ]]; then
    if [ ! -f "$distorted_decoded" ]; then
        if [[ "$original" == "bigbuck_bunny_8bit.yuv" ]]; then
            ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv422p -f rawvideo "$distorted_decoded" -loglevel quiet
        else
            ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv422p10le -f rawvideo "$distorted_decoded" -loglevel quiet
        fi
    else
        echo "File already exists: $distorted_decoded"
    fi
elif [[ "$DATASET" == "AVT-VQDB-UHD-1_2" || "$DATASET" == "AVT-VQDB-UHD-1_3" || "$DATASET" == "AVT-VQDB-UHD-1_4" ]]; then
    if [ ! -f "$distorted_decoded" ]; then
        ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv422p10le  "$distorted_decoded" -loglevel quiet
    else
        echo "File already exists: $distorted_decoded"
    fi
else
    # Use rawvideo format for other datasets
    if [ ! -f "$distorted_decoded" ]; then
        ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv420p -f rawvideo "$distorted_decoded" -loglevel quiet
    else
        echo "File already exists: $distorted_decoded"
    fi
fi

   
# Save Width and height in two variables : they are needed for naming
width_old="$WIDTH"
height_old="$HEIGHT"

echo "width_old : $width_old"
echo "height_old : $height_old"


if [[ "$DATASET" == "ITS4S" ]] || [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
    echo "DATASET : $DATASET"
    if [ "$WIDTH" -ne 1280 ] || [ "$HEIGHT" -ne 720 ]; then
        if [ ! -f "$distorted_decoded_resized" ]; then
            echo "Resized video does not exist"
            echo "Resizing video to 1280x720 for $DATASET"
            echo "distorted_decoded : $distorted_decoded"
            echo "WIDTH : $WIDTH"
            echo "HEIGHT : $HEIGHT"
            ffmpeg -i "$distorted_decoded" \
            -vf "scale=1280x720:flags=lanczos" \
            -sws_flags lanczos+accurate_rnd+full_chroma_int \
            -pix_fmt yuv420p "$distorted_decoded_resized"
        else 
          echo "Resized video already exists"
        fi
      final_decoded_file="$distorted_decoded_resized"
      output_hash="$HASH_DIR/${distorted}_decoded_resized.md5"
      width_new=1280
      height_new=720
      output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
    else
        echo "No resizing needed. Dimensions are already 1280x720."
        final_decoded_file="$distorted_decoded"
        width_new="$width_old"
        height_new="$height_old"
    fi
elif [[ "$DATASET" == "KUGVD" ]] || [[ "$DATASET" == "GamingVideoSet1" ]] || [[ "$DATASET" == "GamingVideoSet2" ]]; then    
    echo "DATASET : $DATASET"
    if [ "$WIDTH" -ne 1920 ] || [ "$HEIGHT" -ne 1080 ]; then
         if [ ! -f "$distorted_decoded_resized" ]; then
           echo "Resized video does not exist"
           echo "Resizing video to 1920x1080..."
           echo "distorted_decoded : $distorted_decoded"
           echo "WIDTH : $WIDTH"
           echo "HEIGHT : $HEIGHT"
   
           ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv420p -r 30 -i "$distorted_decoded" \
           -vf scale=1920x1080:flags=lanczos:param0=3 \
           -sws_flags lanczos+accurate_rnd+full_chroma_int \
           -pix_fmt yuv420p -r 30 -f rawvideo "$distorted_decoded_resized"
         else
           echo "Resized video already exists"
         fi
        final_decoded_file="$distorted_decoded_resized"
        output_hash="$HASH_DIR/${distorted}_decoded_resized.md5"
        width_new=1920
        height_new=1080
        output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
    else
        echo "No resizing needed. Dimensions are already 1920x1080."
        final_decoded_file="$distorted_decoded"
        width_new="$width_old"
        height_new="$height_old"
    fi
elif [[ "$DATASET" == "AVT-VQDB-UHD-1_1" ]] || [[ "$DATASET" == "AVT-VQDB-UHD-1_2" ]] || [[ "$DATASET" == "AVT-VQDB-UHD-1_3" ]] || [[ "$DATASET" == "AVT-VQDB-UHD-1_4" ]]; then
     echo "DATASET : $DATASET"
     if [ "$original" == "bigbuck_bunny_8bit.yuv" ]; then
        if [ "$WIDTH" -ne 4000 ] || [ "$HEIGHT" -ne 2250 ]; then
         if [ ! -f "$distorted_decoded_resized" ]; then
           echo "Resized video does not exist"
           echo "Resizing video to 4000x2250..."
           echo "distorted_decoded : $distorted_decoded"
           echo "WIDTH : $WIDTH"
           echo "HEIGHT : $HEIGHT"
           ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv422p -i "$distorted_decoded" \
           -vf scale=4000x2250:flags=lanczos:param0=3 \
           -sws_flags lanczos+accurate_rnd+full_chroma_int \
           -pix_fmt yuv422p -f rawvideo "$distorted_decoded_resized"
         else
           echo "Resized video already exists"
         fi
         final_decoded_file="$distorted_decoded_resized"
         output_hash="$HASH_DIR/${distorted}_decoded_resized.md5"
         width_new=4000
         height_new=2250
         output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
        else
           echo "No resizing needed. Dimensions are already 4000x2250."
           final_decoded_file="$distorted_decoded"
           width_new="$width_old"
           height_new="$height_old"
        fi
     else
        if [ "$WIDTH" -ne 3840 ] || [ "$HEIGHT" -ne 2160 ]; then
         if [ ! -f "$distorted_decoded_resized" ]; then
           echo "Resized video does not exist"
           echo "Resizing video to 3840x2160..."
           echo "distorted_decoded : $distorted_decoded"
           echo "WIDTH : $WIDTH"
           echo "HEIGHT : $HEIGHT"
           ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv422p10le  -i "$distorted_decoded" \
           -vf scale=3840x2160:flags=lanczos:param0=3 \
           -sws_flags lanczos+accurate_rnd+full_chroma_int \
           -pix_fmt yuv422p10le -f rawvideo "$distorted_decoded_resized"
         else
           echo "Resized video already exists"
         fi
         final_decoded_file="$distorted_decoded_resized"
         output_hash="$HASH_DIR/${distorted}_decoded_resized.md5"
         width_new=3840
         height_new=2160
         output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
        else
           echo "No resizing needed. Dimensions are already 3840x2160."
           final_decoded_file="$distorted_decoded"
           width_new="$width_old"
           height_new="$height_old"
        fi
     fi
fi

# Compute MD5 hash of decoded YUV file
echo "Hash MD5 for $final_decoded_file..."
md5sum "$final_decoded_file" > "$output_hash"
echo "Hash saved in $output_hash."

# Convert FEATURES string to an array
# sep is ','; read from FEATURES and push into the feature_array the elmemnents
IFS=',' read -r -a feature_array <<< "$FEATURES"

# Prepare features argument for VMAF command
feature_args=""
for feature in "${feature_array[@]}"; do
    feature_args+="--feature $feature "
done

# Set model path
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

echo "Final decoded file: $final_decoded_file"

# VMAF evaluation
if [[ "${MODEL_VERSION}" == "vmaf_v0.6.1.json" ]]; then
    if [[ "${DATASET}" == "ITS4S" ]]; then
        /vmaf-3.0.0/libvmaf/build/tools/vmaf \
        --reference "$original_converted_to420p" \
        --distorted "$final_decoded_file" \
        --model "$path" \
        $feature_args \
        --output "$output_json" --json \
        --threads "$(nproc)" 
    elif [[ "${DATASET}" == "AGH_NTIA_Dolby" ]]; then
        /vmaf-3.0.0/libvmaf/build/tools/vmaf \
        --reference "$INPUT_REFERENCE_DIR/$original" \
        --distorted "$final_decoded_file" \
        --model "$path" \
        $feature_args \
        --output "$output_json" --json \
        --threads "$(nproc)" 
    else
        /vmaf-3.0.0/libvmaf/build/tools/vmaf \
        --reference "$INPUT_REFERENCE_DIR/$original" \
        --distorted "$final_decoded_file" \
        --width "$width_new" \
        --height "$height_new" \
        --pixel_format "$PIXEL_FORMAT" \
        --bitdepth "$BIT_DEPTH" \
        --model "$path" \
        $feature_args \
        --output "$output_json" --json \
        --threads "$(nproc)" 
    fi     
else
    if [[ "${DATASET}" == "ITS4S" ]]; then
        /vmaf-3.0.0/libvmaf/build/tools/vmaf \
       --reference "$original_converted_to420p" \
       --distorted "$final_decoded_file" \
       --model "$path" \
       --output "$output_json" --json \
       --threads "$(nproc)" 
    elif [[ "${DATASET}" == "AGH_NTIA_Dolby" ]]; then
        /vmaf-3.0.0/libvmaf/build/tools/vmaf \
        --reference "$INPUT_REFERENCE_DIR/$original" \
        --distorted "$final_decoded_file" \
        --model "$path" \
        --output "$output_json" --json \
        --threads "$(nproc)" 
    else
       /vmaf-3.0.0/libvmaf/build/tools/vmaf \
       --reference "$INPUT_REFERENCE_DIR/$original" \
       --distorted "$final_decoded_file" \
       --width "$width_new" \
       --height "$height_new" \
       --pixel_format "$PIXEL_FORMAT" \
       --bitdepth "$BIT_DEPTH" \
       --model "$path" \
       --output "$output_json" --json \
       --threads "$(nproc)" 
    fi
fi

if [[ "$MODEL_VERSION" == "vmaf_4k_v0.6.1neg.json" ]]; then
    if [ -f "$distorted_decoded" ]; then
        rm "$distorted_decoded"
        echo "Decoded file removed: $distorted_decoded"
    fi

    if [ -f "$distorted_decoded_resized" ]; then
        rm "$distorted_decoded_resized"
        echo "Decoded resized file removed: $distorted_decoded_resized"
    fi

    if [ -f "$original_converted_to420p" ]; then
        rm "$original_converted_to420p"
        echo "Decoded resized file removed: $original_converted_to420p"
    fi
else
    echo "Model version is not 'vmaf_4k_v0.6.1neg.json', skipping file removal."
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
echo "MOS Directory: $MOS_DIR"
echo "Original Video: $ORIGINAL_VIDEO"
echo "Distorted Video : $DISTORTED_VIDEO"
echo "Old WIDTH : $width_old"
echo "Old HEIGHT : $height_old"
echo "FPS : $FPS"
echo "Duration : $DURATION"

    #python3 analyze.py "$DATASET" "$width_new" "$height_new" "$BITRATE" "$VIDEO_CODEC" "$MODEL_VERSION" "$OUTPUT_DIR" "$ORIGINAL_VIDEO" "$DISTORTED_VIDEO" "$width_old" "$height_old" "$FPS" "$DURATION" "$MOS_DIR"

echo "podman run --rm -it -v /home/greco/home/docker/Result:/results \
                          -v /home/greco/home/docker/Mos:/mos image \
                          python3 analyze.py \"$DATASET\" \"$width_new\" \"$height_new\" \"$BITRATE\" \"$VIDEO_CODEC\" \"$MODEL_VERSION\" \"$OUTPUT_DIR\" \"$ORIGINAL_VIDEO\" \"$DISTORTED_VIDEO\" \"$width_old\" \"$height_old\" \"$FPS\" \"$DURATION\" \"$MOS_DIR\"" >> "$FILE_COMMANDS"