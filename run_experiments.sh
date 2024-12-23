#!/bin/bash

#if [ "$#" -ne 18 ]; then
#    echo "Error: Expected 18 arguments, but got $#."
#    exit 1
#fi


# parameters
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
OUTPUT_DIR_SERVER="${18}"     
HASH_DIR_SERVER="${19}"  
MOS_DIR_SERVER="${20}"
ESSIM_PARAMS_STRING="${21}"
USE_LIBVMAF="${22}"
USE_ESSIM="${23}"
FEATURES="${24}"


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
echo "Output Directory server: $OUTPUT_DIR_SERVER"
echo "Hash Directory sercer: $HASH_DIR_SERVER"
echo "MOS Directory: $MOS_DIR_SERVER"
echo "Features: $FEATURES"
echo "USE_LIBVMAF : $USE_LIBVMAF"
echo "USE_ESSIM" : "$USE_ESSIM"
echo "ESSIM_PARAMS_STRING : $ESSIM_PARAMS_STRING"

# Check if directories exist
for dir in "$INPUT_REFERENCE_DIR" "$INPUT_DISTORTED_DIR" "$OUTPUT_DIR" "$HASH_DIR" "$MOS_DIR"; do
    if [ ! -d "$dir" ]; then
        echo "Error: Directory '$dir' does not exist."
        exit 1
    fi
done
# File where to save the Python commands for analyzing the JSON output from VMAF.
FILE_COMMANDS="$OUTPUT_DIR/$DATASET/analyzescriptcommands_${DATASET}.txt"

# Create if it does not exist
if [ ! -f "$FILE_COMMANDS" ]; then
    touch "$FILE_COMMANDS"
fi

#Set filenames :
original="$ORIGINAL_VIDEO"
echo "Original YUV file: $original"
distorted="$DISTORTED_VIDEO"
echo "Input distorted file: $distorted"
# create the hash directory for the dataset
mkdir -p "$HASH_DIR/${DATASET}"
#output hash name
output_hash="$HASH_DIR/${DATASET}/${distorted}_decoded.md5"
if [[ "$DATASET" == "ITS4S" ]] || [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
    # If dataset is AGH_NTIA_Dolby or ITS4S, set decoded file extension to .y4m
    distorted_decoded="$OUTPUT_DIR/${distorted}_decoded.y4m"
else
    # Default extension is .yuv
    distorted_decoded="$OUTPUT_DIR/${distorted}_decoded.yuv"
fi
#"ITS4S has the original video in 4:2:2 and the distorted video in 4:2:0: convert the reference video to 4:2:0."
if [[ "$DATASET" == "ITS4S" ]]; then
    original_converted_to420p="$OUTPUT_DIR/${original}_420p.y4m"
    if [[ ! -f "$original_converted_to420p" ]]; then
        ffmpeg -i "$INPUT_REFERENCE_DIR/$original" -pix_fmt yuv420p "$original_converted_to420p" -loglevel quiet
        echo "OriginalConvertedtoy4m: $original_converted_to420p"
    fi
fi
#AVT-VQDB-UHD-1_1 has one original video with 8-bit depth, and the others have 10-bit depth.
#Convert the reference video to YUV422p with 8-bit depth."
if [[ "$DATASET" == "AVT-VQDB-UHD-1_1" ]]; then
    if [[ "$original" != "bigbuck_bunny_8bit.yuv" ]]; then
        reference_converted_to_8_bit="$OUTPUT_DIR/${original}_8bit.yuv"
        if [[ ! -f "$reference_converted_to_8_bit" ]]; then
            #ffmpeg -s 3840x2160 -i "$INPUT_REFERENCE_DIR/$original" -pix_fmt yuv422p "$reference_converted_to_8_bit"
            ffmpeg -s 3840x2160 -pix_fmt yuv422p10le -i "$INPUT_REFERENCE_DIR/$original" -pix_fmt yuv422p -y "$reference_converted_to_8_bit"
            if [[ $? -eq 0 ]]; then  
                echo "Original Converted to 8bit: $reference_converted_to_8_bit"
            else
                echo "Error in converting original to 8bit: $reference_converted_to_8_bit"
            fi
        fi
    fi
fi

#AVT-VQDB-UHD-1_4 has some videos with a different frame rate than the reference. Convert the reference video to 30fps or 15fps

if [[ "$DATASET" == "AVT-VQDB-UHD-1_4" ]]; then
    if [[ "$FPS" == 59.94 ]] || [[ "$FPS" == 60.0 ]] ; then
        final_original_file_avt_1_4="$INPUT_REFERENCE_DIR/$original"
    else
        if [[ "$FPS" == 30.0 ]]; then
            reference_converted_to_30fps="$OUTPUT_DIR/${original}_30fps.yuv"
            if [[ ! -f "$reference_converted_to_30fps" ]]; then
                ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv422p10le -i "$INPUT_REFERENCE_DIR/$original" -vf "select=not(mod(n\,2))" -vsync 0 -strict -1 -pix_fmt yuv422p10le "$reference_converted_to_30fps"
                final_original_file_avt_1_4="$reference_converted_to_30fps"
            else
                echo "30fps original file already exists: $reference_converted_to_30fps"
            fi
        elif [[ "$FPS" == 15.0 ]]; then
            reference_converted_to_15fps="$OUTPUT_DIR/${original}_15fps.yuv"
            if [[ ! -f "$reference_converted_to_15fps" ]]; then
                ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv422p10le -i "$INPUT_REFERENCE_DIR/$original" -vf "select=not(mod(n\,4))" -vsync 0 -strict -1 -pix_fmt yuv422p10le "$reference_converted_to_15fps"
                final_original_file_avt_1_4="$reference_converted_to_15fps"
            else
                echo "15fps original file already exists: $reference_converted_to_15fps"
            fi
        fi
    fi
fi




# Print the name of the decoded file
echo "Decoded file: $distorted_decoded"
# Output Resized YUV : file name of decoded file resized.
if [[ "$DATASET" == "ITS4S" ]] || [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
 distorted_decoded_resized="$OUTPUT_DIR/${distorted}_decoded_resized.y4m"
else
 distorted_decoded_resized="$OUTPUT_DIR/${distorted}_decoded_resized.yuv"
fi

##create the vmaf results directory if absent
mkdir -p "$OUTPUT_DIR/${DATASET}/vmaf_results"

#Default Output json 
output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}.json"

#Default Output Essim
output_essim="$OUTPUT_DIR/${DATASET}/essim_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}__${ESSIM_PARAMS_STRING}.csv"

#Decoding: (decode only if the decoded file does not exist)
#   - ITS4S: Decode the distorted video. The result is YUV420p in a .y4m file.
#   -  AGH_NTIA_Dolby: The distorted video is already in .y4m format. Simply copy the file.
#   -  TODO: AVT-VQDB-UHD-1_1: Decode the distorted video. The result is YUV422p in a .yuv file.
#   -  AVT-VQDB-UHD-1_2, AVT-VQDB-UHD-1_3, AVT-VQDB-UHD-1_4: Decode the distorted video. The result is YUV422p with 10-bit depth in a .yuv file.
#   -  KUGVD, GamingVideoSet1, VideoGamingSet2: Decode the distorted video. The result is YUV420p in a .yuv file.

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
            #decoded --> bitdepth = 8
            ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv422p -f rawvideo "$distorted_decoded" -loglevel quiet
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
    if [ ! -f "$distorted_decoded" ]; then
        ffmpeg -i "$INPUT_DISTORTED_DIR/$distorted" -pix_fmt yuv420p -f rawvideo "$distorted_decoded" -loglevel quiet
    else
        echo "File already exists: $distorted_decoded"
    fi
fi

   
# Save Width and height in two variables : they are needed for naming in The csv
width_old="$WIDTH"
height_old="$HEIGHT"

echo "width_old : $width_old"
echo "height_old : $height_old"

# Resizing ( resize the decoded file if it does not exist and the dimensions are different from the original one)
# The code set also where to save the hash file of the distorted file and the JSON output from VMAF.
# The resized video will be used for vmaf evaluation
# Target dimensions :
# - ITS4S : 1280x720
# - AGH_NTIA_Dolby : 1280x720
# - KUGVD: 1920x1080
# - GamingVideoSet1 : 1920x1080
# - GamingVideoSet2 : 1920x1080
# - AVT-VQDB-UHD-1_1 : bigbuck_bunny_8bit.yuv related files : 4000x2250. Others: 3840x2160
# - AVT-VQDB-UHD-1_2 | AVT-VQDB-UHD-1_3 | AVT-VQDB-UHD-1_4 :  3840x2160

# TODO : FPS ?

if [[ "$DATASET" == "ITS4S" ]]; then
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
      output_hash="$HASH_DIR/${DATASET}/${distorted}_decoded_resized.md5"
      width_new=1280
      height_new=720
      output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
      output_essim="$OUTPUT_DIR/${DATASET}/essim_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}__${ESSIM_PARAMS_STRING}_resized_${width_new}x${height_new}.csv"
    else
        echo "No resizing needed. Dimensions are already 1280x720."
        final_decoded_file="$distorted_decoded"
        width_new="$width_old"
        height_new="$height_old"
    fi
elif [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
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
            -pix_fmt yuv422p "$distorted_decoded_resized"
        else 
          echo "Resized video already exists"
        fi
      final_decoded_file="$distorted_decoded_resized"
      output_hash="$HASH_DIR/${DATASET}/${distorted}_decoded_resized.md5"
      width_new=1280
      height_new=720
      output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
      output_essim="$OUTPUT_DIR/${DATASET}/essim_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}__${ESSIM_PARAMS_STRING}_resized_${width_new}x${height_new}.csv"
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
        output_hash="$HASH_DIR/${DATASET}/${distorted}_decoded_resized.md5"
        width_new=1920
        height_new=1080
        output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
        output_essim="$OUTPUT_DIR/${DATASET}/essim_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}__${ESSIM_PARAMS_STRING}_resized_${width_new}x${height_new}.csv"
    else
        echo "No resizing needed. Dimensions are already 1920x1080."
        final_decoded_file="$distorted_decoded"
        width_new="$width_old"
        height_new="$height_old"
    fi
elif [[ "$DATASET" == "AVT-VQDB-UHD-1_1" ]]; then
     echo "DATASET : $DATASET"
     if [ "$original" == "bigbuck_bunny_8bit.yuv" ]; then
        if [ "$WIDTH" -ne 4000 ] || [ "$HEIGHT" -ne 2250 ]; then
         if [ ! -f "$distorted_decoded_resized" ]; then
           echo "Resized video does not exist"
           echo "Resizing video to 4000x2250..."
           echo "distorted_decoded : $distorted_decoded"
           echo "WIDTH : $WIDTH"
           echo "HEIGHT : $HEIGHT"
           ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv422p  -i "$distorted_decoded" \
           -vf scale=4000x2250:flags=lanczos:param0=3 \
           -sws_flags lanczos+accurate_rnd+full_chroma_int \
           -pix_fmt yuv422p -f rawvideo "$distorted_decoded_resized"
         else
           echo "Resized video already exists"
         fi
         final_decoded_file="$distorted_decoded_resized"
         output_hash="$HASH_DIR/${DATASET}/${distorted}_decoded_resized.md5"
         width_new=4000
         height_new=2250
         output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
         output_essim="$OUTPUT_DIR/${DATASET}/essim_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}__${ESSIM_PARAMS_STRING}_resized_${width_new}x${height_new}.csv"
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
           ffmpeg -s "$WIDTH"x"$HEIGHT" -pix_fmt yuv422p  -i "$distorted_decoded" \
           -vf scale=3840x2160:flags=lanczos:param0=3 \
           -sws_flags lanczos+accurate_rnd+full_chroma_int \
           -pix_fmt yuv422p -f rawvideo "$distorted_decoded_resized"
         else
           echo "Resized video already exists"
         fi
         final_decoded_file="$distorted_decoded_resized"
         output_hash="$HASH_DIR/${DATASET}/${distorted}_decoded_resized.md5"
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
elif [[ "$DATASET" == "AVT-VQDB-UHD-1_2" ]] || [[ "$DATASET" == "AVT-VQDB-UHD-1_3" ]] || [[ "$DATASET" == "AVT-VQDB-UHD-1_4" ]]; then
     echo "DATASET : $DATASET"
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
        output_hash="$HASH_DIR/${DATASET}/${distorted}_decoded_resized.md5"
        width_new=3840
        height_new=2160
        output_json="$OUTPUT_DIR/${DATASET}/vmaf_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}_resized_${width_new}x${height_new}.json"
        output_essim="$OUTPUT_DIR/${DATASET}/essim_results/result__${DATASET}__${original}__${WIDTH}x${HEIGHT}__${BITRATE}__${VIDEO_CODEC}__${MODEL_VERSION}__${ESSIM_PARAMS_STRING}_resized_${width_new}x${height_new}.csv"
     else
        echo "No resizing needed. Dimensions are already 3840x2160."
        final_decoded_file="$distorted_decoded"
        width_new="$width_old"
        height_new="$height_old"
     fi
fi

# "Compute the MD5 hash of the decoded (or decoded and resized, if resizing is necessary) file, but only if it doesn't already exist."
if [ ! -f "$output_hash" ]; then
    echo "Hash MD5 for $final_decoded_file..."
    md5sum "$final_decoded_file" > "$output_hash"
    echo "Hash saved in $output_hash."
else
    echo "Hash already exists in $output_hash."
fi


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

# vmaf :
# parameters :
# - referencevideo :  path to reference .y4m or .yuv. 
# Special cases : ITS4S --> convert the original to 420p
# AVT-VQDB-UHD-1_1 -> convert the reference video to yuv 422 with bitdepth=8  if the original video is different fromb igbuck_bunny_8bit.yuv
# AVT-VQDB-UHD-1_4 has some videos with a different frame rate than the reference. Convert the reference video to 30fps or 15fps.
# - distortedvideo : decoded or decoded resized distorted video video 
# - model : "$path"
# - $feature_args  : only used when the model is vmaf_v0.6.1.json
# - output : write output file as JSON
# - threads : number of threads to use


# Check if USE_LIBVMAF is true
if [[ "$USE_LIBVMAF" == "True" ]]; then
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
        elif [[ "${DATASET}" == "AVT-VQDB-UHD-1_1" ]]; then
            if [[ "$original" == "bigbuck_bunny_8bit.yuv" ]]; then
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
            else
                /vmaf-3.0.0/libvmaf/build/tools/vmaf \
                --reference "$reference_converted_to_8_bit" \
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
        elif [[ "${DATASET}" == "AVT-VQDB-UHD-1_4" ]]; then
            /vmaf-3.0.0/libvmaf/build/tools/vmaf \
            --reference "$final_original_file_avt_1_4" \
            --distorted "$final_decoded_file" \
            --width "$width_new" \
            --height "$height_new" \
            --pixel_format "$PIXEL_FORMAT" \
            --bitdepth "$BIT_DEPTH" \
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
        elif [[ "${DATASET}" == "AVT-VQDB-UHD-1_1" ]]; then
            if [[ "$original" == "bigbuck_bunny_8bit.yuv" ]]; then
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
            else
                /vmaf-3.0.0/libvmaf/build/tools/vmaf \
                --reference "$reference_converted_to_8_bit" \
                --distorted "$final_decoded_file" \
                --width "$width_new" \
                --height "$height_new" \
                --pixel_format "$PIXEL_FORMAT" \
                --bitdepth "$BIT_DEPTH" \
                --model "$path" \
                --output "$output_json" --json \
                --threads "$(nproc)"
            fi
        elif [[ "${DATASET}" == "AVT-VQDB-UHD-1_4" ]]; then
            /vmaf-3.0.0/libvmaf/build/tools/vmaf \
            --reference "$final_original_file_avt_1_4" \
            --distorted "$final_decoded_file" \
            --width "$width_new" \
            --height "$height_new" \
            --pixel_format "$PIXEL_FORMAT" \
            --bitdepth "$BIT_DEPTH" \
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
fi

mkdir -p "$OUTPUT_DIR/${DATASET}/essim_results"


#Function to interpret the model string:



if [[ "$USE_ESSIM" == "True" ]]; then
    # Function to parse the model string and extract parameters
    parse_model() {
        local model_str="$1"
        wsize=$(echo "$model_str" | sed -n 's/.*ws\([0-9]*\).*/\1/p')
        wstride=$(echo "$model_str" | sed -n 's/.*wt\([0-9]*\).*/\1/p')
        mink=$(echo "$model_str" | sed -n 's/.*mk\([0-9]*\).*/\1/p')
        mode=$(echo "$model_str" | sed -n 's/.*md\([0-9]*\).*/\1/p')
    }

    # Extracting parameters from the template string
    parse_model "$ESSIM_PARAMS_STRING"

    # Set directories and file paths for essim
    final_original_file_essim="$INPUT_REFERENCE_DIR/$original"
    final_decoded_file_essim="$final_decoded_file" 
   
    if [[ "$DATASET" == "AVT-VQDB-UHD-1_1" ]]; then
        if [[ "$original" == "bigbuck_bunny_8bit.yuv" ]]; then
            final_original_file_essim="$INPUT_REFERENCE_DIR/$original"
        else
            final_original_file_essim="$reference_converted_to_8_bit"
        fi
    fi

    if [[ "$DATASET" == "AVT-VQDB-UHD-1_4" ]]; then
        final_original_file_essim="$final_original_file_avt_1_4"
    fi

    # Convert video file based on dataset type
    if [[ "$DATASET" == "ITS4S" ]]; then
        final_original_file_essim="$OUTPUT_DIR/${original%.*}.yuv"     
        final_decoded_file_essim="${final_decoded_file%.*}.yuv"
        if [ ! -f "$final_original_file_essim" ]; then
            ffmpeg -i "$original_converted_to420p" -f rawvideo -pix_fmt yuv420p "$final_original_file_essim"
        else 
            echo "File already exists: $final_original_file_essim"
        fi
        if [ ! -f "$final_decoded_file_essim" ]; then
            ffmpeg -i "$final_decoded_file" -f rawvideo -pix_fmt yuv420p "$final_decoded_file_essim"
        else 
            echo "File already exists: $final_decoded_file_essim"
        fi
    elif [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
        final_original_file_essim="$OUTPUT_DIR/${original%.*}.yuv"     
        final_decoded_file_essim="${final_decoded_file%.*}.yuv"
        if [ ! -f "$final_original_file_essim" ]; then
            ffmpeg -i "$INPUT_REFERENCE_DIR/$original" -f rawvideo -pix_fmt yuv422p "$final_original_file_essim"
        else  
            echo "File already exists: $final_original_file_essim"
        fi
        if [ ! -f "$final_decoded_file_essim" ]; then
            ffmpeg -i "$final_decoded_file" -f rawvideo -pix_fmt yuv422p "$final_decoded_file_essim"
        else 
            echo "File already exists: $final_decoded_file_essim"
        fi
    fi

    # Run eSSIM
    /essim/build/bin/essim \
        -r "$final_original_file_essim" \
        -d "$final_decoded_file_essim" \
        -w "$width_new" \
        -h "$height_new" \
        -bd "$BIT_DEPTH" \
        -wsize "$wsize" \
        -wstride "$wstride" \
        -mink "$mink" \
        -mode "$mode" \
        -o "$output_essim"
fi



# remove file after the vmaf evaluations
# TODO: when i can delete the files?
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
        echo "Original converted to 420p removed: $original_converted_to420p"
    fi
    if [ -f "$reference_converted_to_8_bit" ]; then
        rm "$reference_converted_to_8_bit"
        echo "Reference converted to 8-bit removed: $reference_converted_to_8_bit"
    fi
    if [ -f "$reference_converted_to_30fps" ]; then
        rm "$reference_converted_to_30fps"
        echo "Reference converted to 30fps removed: $reference_converted_to_30fps"
    fi
    if [ -f "$reference_converted_to_15fps" ]; then
        rm "$reference_converted_to_15fps"
        echo "Reference converted to 15fps removed: $reference_converted_to_15fps"
    fi
    echo "Final_original_file_essim : $final_original_file_essim"
    echo "Final_decoded_file_essimm : $final_decoded_file_essim"

    if [[ "$DATASET" == "ITS4S" ]] || [[ "$DATASET" == "AGH_NTIA_Dolby" ]]; then
        if [ -f "$final_original_file_essim" ]; then
            rm "$final_original_file_essim"
            echo "Final_original_file_essimm removed: $final_original_file_essim"
        fi
        if [ -f "$final_decoded_file_essim" ]; then
            rm "$final_decoded_file_essim"
            echo "Final_decoded_file_essim removed: $final_decoded_file_essim"
        fi
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
echo "Output Directory server: $OUTPUT_DIR_SERVER"
echo "Hash Directory sercer: $HASH_DIR_SERVER"
echo "MOS Directory: $MOS_DIR_SERVER"
echo "Essim String : $ESSIM_PARAMS_STRING"
echo "USE_LIBVMAF : $USE_LIBVMAF"
echo "USE_ESSIM : $USE_ESSIM"

#python3 analyze.py "$DATASET" "$width_new" "$height_new" "$BITRATE" "$VIDEO_CODEC" "$MODEL_VERSION" "$OUTPUT_DIR" "$ORIGINAL_VIDEO" "$DISTORTED_VIDEO" "$width_old" "$height_old" "$FPS" "$DURATION" "$MOS_DIR"

# echo "python3 analyze.py \"$DATASET\" \"$width_new\" \"$height_new\" \"$BITRATE\" \"$VIDEO_CODEC\" \"$MODEL_VERSION\" \"$OUTPUT_DIR_SERVER\" \"$ORIGINAL_VIDEO\" \"$DISTORTED_VIDEO\" \"$width_old\" \"$height_old\" \"$FPS\" \"$DURATION\" \"$MOS_DIR_SERVER\" " >> "$FILE_COMMANDS"
echo "python3 analyze.py \"$DATASET\" \"$width_new\" \"$height_new\" \"$BITRATE\" \"$VIDEO_CODEC\" \"$MODEL_VERSION\" \"$OUTPUT_DIR_SERVER\" \"$ORIGINAL_VIDEO\" \"$DISTORTED_VIDEO\" \"$width_old\" \"$height_old\" \"$FPS\" \"$DURATION\" \"$MOS_DIR_SERVER\" \"$ESSIM_PARAMS_STRING\" \"$USE_LIBVMAF\" \"$USE_ESSIM\"" >> "$FILE_COMMANDS"
