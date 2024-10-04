#lo script mi deve generare delle linee del tipo : 
#podman run --rm miovmaf -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m version=vmaf_4k_v0.6.1neg
#questo comando è da lanciare dentro il container

# 1. lo script che lancio con 
#python create_vmaf_cmdlines.py  input_orig_dir  OUTPUT_DIR HASH_DIR  MODEL VERSION DATASET WIDTH HEIGHT BITRATE  VIDEO_CODEC PIXEL_FORMAT BIT DEPTH
#fuori genera le linee--> lanciate dentro

# 2. quindi fa fuori è creo.py---> questo crea la linea , docker build e docker run con il run creato dentro

import os
import sys
import json

def create_vmaf_command(image_name,input_reference_dir, input_distorted_dir , output_dir, hash_dir, original_video, distorted_video,  model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth):
  
    print(f"Original Video: {original_video}")
    print(f"Distorted Video: {distorted_video}")
    
    command = f"docker run --rm -it \
    -v {input_reference_dir}:/reference \
    -v {input_distorted_dir}:/distorted \
    -v {output_dir}:/results \
    -v {hash_dir}:/hash \
    {image_name} \
    /bin/bash -c './run_experiments.sh /reference /distorted /results /hash {model_version} {dataset} {width} {height} {bitrate} {video_codec} {pixel_format} {bit_depth} {original_video} {distorted_video} && python3 analyze.py {dataset} {width} {height} {bitrate} {video_codec} {model_version}  /results'"

    print("-----------------------------------")


    return command

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python create_vmaf_cmdlines.py config file")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    # Read the JSON configuration file
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    # Get parameters from the config file
    image_name = config['IMAGE_NAME']
    input_reference_dir = config['INPUT_REF_DIR']
    input_distorted_dir = config['INPUT_DIST_DIR']
    output_dir = config['OUTPUT_DIR']
    hash_dir = config['HASH_DIR']
    original_video=config['ORIGINAL_VIDEO']
    model_version = config['MODEL_VERSION']
    dataset = config['DATASET']
    width = config['WIDTH']
    height = config['HEIGHT']
    bitrate = config['BITRATE']
    video_codec = config['VIDEO_CODEC']
    pixel_format = config['PIXEL_FORMAT']
    bit_depth = config['BIT_DEPTH']
    

# Ottiene il nome del file originale senza estensione (radice)
original_base = os.path.splitext(os.path.basename(original_video))[0]

# Scorre tutti i file nella directory distorted
for distorted_file in os.listdir(input_distorted_dir):
    # Mantiene il nome del file distorto completo per l'output
    distorted_full_name = distorted_file  
    distorted_base = os.path.splitext(distorted_full_name)[0]

    # Se il nome del file originale è contenuto nel nome del file distorto, genera il comando
    if original_base in distorted_base:
        command = create_vmaf_command(image_name, input_reference_dir, input_distorted_dir, output_dir, hash_dir, original_video, distorted_full_name, model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth)

        # Salva il comando nel file
        with open(os.path.join(output_dir, 'commands.txt'), 'a') as f:
            f.write(command + '\n')

print(f"Comandi VMAF generati e salvati in {output_dir}/commands.txt")
