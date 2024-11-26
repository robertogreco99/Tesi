import json
import os
import subprocess

dataset="KUGVD"
originalvideo_list_file = f"/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Simulations/{dataset}/{dataset}_reference_video_list.txt"
json_config_path = "/home/greco/home/docker/Json/config.json"  

def process_originalvideo_file(originalvideo_file):
    with open(json_config_path, 'r') as json_file:
        config_data = json.load(json_file)

    config_data["ORIGINAL_VIDEO"] = originalvideo_file

    with open(json_config_path, 'w') as json_file:
        json.dump(config_data, json_file, indent=4)

    subprocess.run(["python3", "create_commands.py", json_config_path])

with open(originalvideo_list_file, 'r') as file:
    originalvideo_files = file.readlines()

for originalvideo_file in originalvideo_files:
    originalvideo_file = originalvideo_file.strip() 
    if originalvideo_file:  
        process_originalvideo_file(originalvideo_file)
