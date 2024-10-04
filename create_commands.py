import os
import sys
import json
from jsonschema import validate, ValidationError


def create_vmaf_command(image_name,input_reference_dir, input_distorted_dir , output_dir, hash_dir, original_video, distorted_video,  model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth, features_list):
  
    #print(f"Original Video: {original_video}")
    #print(f"Distorted Video: {distorted_video}")

    #print(f"Properties: {width}x{height}, Bitrate: {bitrate} kbps, Pixel Format: {pixel_format}, Codec: {video_codec}, Bit Depth: {bit_depth}")
    

    features = ','.join(features_list)  
    
    command = f"docker run --rm -it \
    -v {input_reference_dir}:/reference \
    -v {input_distorted_dir}:/distorted \
    -v {output_dir}:/results \
    -v {hash_dir}:/hash \
    {image_name} \
    /bin/bash -c './run_experiments.sh /reference /distorted /results /hash {model_version} {dataset} {width} {height} {bitrate} {video_codec} {pixel_format} {bit_depth} {original_video} {distorted_video} {features} && python3 analyze.py {dataset} {width} {height} {bitrate} {video_codec} {model_version}  /results'"

    #print("-----------------------------------")


    return command

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python create_vmaf_cmdlines.py config file")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    # Carica lo schema da un file


    # Read the JSON configuration file
with open(config_file, 'r') as f:
        config = json.load(f)
with open('Json/configschema.json') as schema_file:
    schema = json.load(schema_file)
    
    # Get parameters from the config file
    image_name = config['IMAGE_NAME']
    input_reference_dir = config['INPUT_REF_DIR']
    input_distorted_dir = config['INPUT_DIST_DIR']
    output_dir = config['OUTPUT_DIR']
    hash_dir = config['HASH_DIR']
    original_video=config['ORIGINAL_VIDEO']
    model_version = config['MODEL_VERSION']
    dataset = config['DATASET']
    features_list= config['FEATURES']

    
    dataset_file = f"{dataset}.json"  
   
    dataset_file = os.path.join("Dataset", f"{dataset}.json")
   
try:
    validate(instance=config, schema=schema)
    print("JSON is valid")
except ValidationError as e:
    print("JSON is not valid", e.message)
    sys.exit(1) 
    
    
   

with open(dataset_file, 'r') as f:
    video_metadata = json.load(f)
    
    

# Ottiene il nome del file originale senza estensione (radice)
original_base = os.path.splitext(os.path.basename(original_video))[0]

# Scorre tutti i file nella directory distorted
for distorted_file in os.listdir(input_distorted_dir):
    # Mantiene il nome del file distorto completo per l'output
    distorted_full_name = distorted_file  
    distorted_base = os.path.splitext(distorted_full_name)[0]

    # Se il nome del file originale è contenuto nel nome del file distorto, genera il comando
    if original_base in distorted_base:
        # Estrai i metadati associati al file distorto
        # Trova il video distorto con file_name pari a distorted_full_name  
        metadata = next((video for video in video_metadata["distorted_videos"] if video["file_name"] == distorted_full_name), None)

        #  Se il video esiste, estrai i suoi metadati
        if metadata:
            width = metadata["width"]
            height = metadata["height"]
            bitrate = metadata["bitrate"]
            video_codec = metadata["video_codec"]
            pixel_format=metadata["pixel_format"]
            bit_depth = metadata["bitdepth"]
        else:
            print(f"{distorted_full_name} was not found.")
            
       

        command = create_vmaf_command(image_name, input_reference_dir, input_distorted_dir, output_dir, hash_dir, original_video, distorted_full_name, model_version, dataset, width, height, bitrate, video_codec, pixel_format, bit_depth,features_list)

        # Save the command
        with open(os.path.join(output_dir, 'commands.txt'), 'a') as f:
            f.write(command + '\n')

print(f" VMAF comands saved in {output_dir}/commands.txt")
