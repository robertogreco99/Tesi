import json
import os
import sys
import subprocess

schema_file_path = 'Json/configschema.json'

def process_originalvideo_file(originalvideo_file):           
    with open(json_config_path, 'r') as json_file:
        config_data = json.load(json_file)
            
    config_data["ORIGINAL_VIDEO"] = originalvideo_file
    
    with open(json_config_path, 'w') as json_file:
        json.dump(config_data, json_file, indent=4)
            #run the create commands.py script
    subprocess.run(["python3", "create_commands.py", json_config_path])
    # Remove if the file created by previous executions exists.
        
if __name__ == '__main__':
    # Check for the correct number of arguments
    if len(sys.argv) != 2:
        print("The script needs two arguments. You need to call it like: python3 run_analyze_script_simulation.py Json/config.json")
        sys.exit(1)
    
    # Get the config file from the command-line argument
    config_file = sys.argv[1]

    # Load the config file
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)

    # Load the schema file
    try:
        with open(schema_file_path) as schema_file:
            schema = json.load(schema_file)
    except FileNotFoundError:
        print(f"Error: Schema file '{schema_file_path}' not found.")
        sys.exit(1)

    output_dir = config['OUTPUT_DIR']
    dataset = config['DATASET']
    simulations_dir=config['SIMULATIONS_DIR']
    json_dir=config['JSON_DIR']
    #text file that contains the list of reference videos       
    originalvideo_list_file = f"{simulations_dir}/{dataset}/{dataset}_reference_video_list.txt"
    #where to found the config file
    json_config_path = f"{json_dir}/config.json"  
    #where to find the text file from previous run 
    commands_file_path = f"{output_dir}/{dataset}/commands_{dataset}.txt"

    if os.path.exists(commands_file_path):
        os.remove(commands_file_path)
        print(f"Deleted existing file: {commands_file_path}")
        
    # read the file list      
    with open(originalvideo_list_file, 'r') as file:
        originalvideo_files = file.readlines()
    # change the "ORIGINAL_VIDEO" field in the config file for every video in the list
    for originalvideo_file in originalvideo_files:
        originalvideo_file = originalvideo_file.strip() 
        if originalvideo_file:  
            process_originalvideo_file(originalvideo_file)
    
    
    
    
    
    
"""
#dataset to set
dataset="KUGVD"
#text file that contains the list of reference videos
originalvideo_list_file = f"/home/greco/home/docker/Simulations/{dataset}/{dataset}_reference_video_list.txt"
#where to found the config file
json_config_path = "/home/greco/home/docker/Json/config.json"  
#where to find the text file from previous run 
commands_file_path = f"/home/greco/home/docker/Result/{dataset}/commands_{dataset}.txt"

def process_originalvideo_file(originalvideo_file):           
    with open(json_config_path, 'r') as json_file:
        config_data = json.load(json_file)

    config_data["ORIGINAL_VIDEO"] = originalvideo_file
    
    with open(json_config_path, 'w') as json_file:
        json.dump(config_data, json_file, indent=4)
    #run the create commands.py script
    subprocess.run(["python3", "create_commands.py", json_config_path])
# Remove if the file created by previous executions exists.
if os.path.exists(commands_file_path):
        os.remove(commands_file_path)
        print(f"Deleted existing file: {commands_file_path}")
# read the file list      
with open(originalvideo_list_file, 'r') as file:
    originalvideo_files = file.readlines()
# change the "ORIGINAL_VIDEO" field in the config file for every video in the list
for originalvideo_file in originalvideo_files:
    originalvideo_file = originalvideo_file.strip() 
    if originalvideo_file:  
        process_originalvideo_file(originalvideo_file)
"""