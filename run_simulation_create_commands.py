import json
import os
import subprocess

yuv_list_file = "/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Simulation/KUGDV/KUGDV_reference_video_list.txt"  
json_config_path = "/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Json/config.json"  

def process_yuv_file(yuv_file):
    with open(json_config_path, 'r') as json_file:
        config_data = json.load(json_file)

    config_data["ORIGINAL_VIDEO"] = yuv_file

    with open(json_config_path, 'w') as json_file:
        json.dump(config_data, json_file, indent=4)

    subprocess.run(["python3", "create_commands.py", json_config_path])

with open(yuv_list_file, 'r') as file:
    yuv_files = file.readlines()

for yuv_file in yuv_files:
    yuv_file = yuv_file.strip() 
    if yuv_file:  
        process_yuv_file(yuv_file)
