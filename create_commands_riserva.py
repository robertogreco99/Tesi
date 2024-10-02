#lo script mi deve generare delle linee del tipo : 
#podman run --rm miovmaf -r original.y4m -d distorted.y4m -o result_NAME.json --json -q -m version=vmaf_4k_v0.6.1neg
#questo comando è da lanciare dentro il container

# 1. lo script che lancio con 
#python create_vmaf_cmdlines.py  INPUT_DIR  OUTPUT_DIR HASH_DIR  MODEL VERSION DATASET WIDTH HEIGHT BITRATE  VIDEO_CODEC PIXEL_FORMAT BIT DEPTH
#fuori genera le linee--> lanciate dentro

# 2. quindi fa fuori è creo.py---> questo crea la linea , docker build e docker run con il run creato dentro

import os
import sys

def create_vmaf_command(image_name,input_dir, output_dir, hash_dir, model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth):
    # Directory
    original_file = os.path.join(input_dir, 'original.yuv')
    distorted_file = os.path.join(output_dir, 'distorted.yuv')
    
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
    if len(sys.argv) != 13:
        print("Usage: python create_commands.py IMAGE_NAME INPUT_DIR OUTPUT_DIR HASH_DIR MODEL_VERSION DATASET WIDTH HEIGHT BITRATE VIDEO_CODEC PIXEL_FORMAT BIT_DEPTH")
        sys.exit(1)
    
    # need to check error in the params
    image_name,input_dir, output_dir, hash_dir, model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth = sys.argv[1:]
    
    command = create_vmaf_command(image_name,input_dir, output_dir, hash_dir, model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth)

      
    
    # Print command line
    #print(command)
    
    # Save line command
    with open(os.path.join(output_dir, 'commands.txt'), 'a') as f:
        f.write(command + '\n')
