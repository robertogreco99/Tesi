#lo script mi deve generare delle linee del tipo : 
#podman run --rm miovmaf -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m version=vmaf_4k_v0.6.1neg
#questo comando è da lanciare dentro il container

# 1. lo script che lancio con 
#python create_vmaf_cmdlines.py  INPUT_DIR  OUTPUT_DIR HASH_DIR  MODEL VERSION DATASET WIDTH HEIGHT BITRATE  VIDEO_CODEC PIXEL_FORMAT BIT DEPTH
#fuori genera le linee--> lanciate dentro

# 2. quindi fa fuori è creo.py---> questo crea la linea , docker build e docker run con il run creato dentro

import os
import sys
import json

def create_vmaf_command(image_name,input_dir, output_dir, hash_dir, model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth):
    # Directory
      
    #output_file = os.path.join(output_dir, f'result_{hash_dir}_{dataset}_{model_version}.json')
    #print(output_file)

    # Create the command base
    #command = f"docker run --rm -it -v {input_dir}:/inputs -v{output_dir}:/results -v {hash_dir}:/hash {image_name} " 
    #print(command)
    #command = f"docker run --rm -it \
    #-v {input_dir}:/inputs \
    #-v {output_dir}:/results \
    #-v {hash_dir}:/hash \
    #{image_name} \
    #/bin/bash -c './run_experiments.sh {input_dir} {output_dir} {hash_dir} {model_version} {dataset} {width} {height} {bitrate} {video_codec} {pixel_format} {bit_depth}; exec /bin/bash'"

    command = f"docker run --rm -it \
    -v {input_dir}:/inputs \
    -v {output_dir}:/results \
    -v {hash_dir}:/hash \
    {image_name} \
    /bin/bash -c './run_experiments.sh {input_dir} {output_dir} {hash_dir} {model_version} {dataset} {width} {height} {bitrate} {video_codec} {pixel_format} {bit_depth} && python3 analyze.py {dataset} {width} {height} {bitrate} {video_codec} {model_version} {output_dir}'"


   

    #-o {output_file} --json -q -m version={model_version}"
    #command = f"podman run -it --rm -v /home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Input:/inputs 
    # -v /home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result:/results 
    # -v /home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Hash:/hash 
    # image -r {original_file} -d {distorted_file} -o {output_file} --json -q -m version={model_version}"

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
    input_dir = config['INPUT_DIR']
    output_dir = config['OUTPUT_DIR']
    hash_dir = config['HASH_DIR']
    model_version = config['MODEL_VERSION']
    dataset = config['DATASET']
    width = config['WIDTH']
    height = config['HEIGHT']
    bitrate = config['BITRATE']
    video_codec = config['VIDEO_CODEC']
    pixel_format = config['PIXEL_FORMAT']
    bit_depth = config['BIT_DEPTH']
    
    command = create_vmaf_command(image_name, input_dir, output_dir, hash_dir, model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth)

    # Save the command to a file
    with open(os.path.join(output_dir, 'commands.txt'), 'a') as f:
        f.write(command + '\n')
