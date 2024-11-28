# How to run

1. **Build Podman Image**  
   ```bash
   podman build -t <imageName> <folder>
   ```
2. Set up the JSON Configuration File
Create or edit the JSON file in /home/greco/home/docker.
Example template:
```json
{
    "IMAGE_NAME": "image",
    "INPUT_REF_DIR": "",
    "INPUT_DIST_DIR": "",
    "OUTPUT_DIR": "/home/greco/home/docker/Result",
    "HASH_DIR": "/home/greco/home/docker/Hash",
    "MOS_DIR": "/home/greco/home/docker/Mos",
    "ORIGINAL_VIDEO": "",
    "MODEL_VERSION": "VMAF_ALL",
    "DATASET": "",
    "FEATURES": [
        "cambi",
        "float_ssim",
        "psnr",
        "float_ms_ssim",
        "ciede",
        "psnr_hvs"
    ]
}
```

3. **Generate Podman Commands**  
   Edit the variable dataset="" in run_simulation_create_commands.py
   ```bash
   python3 run_simulation_create_commands.py
   ```
   Output = /home/greco/home/docker/Result/{dataset}/commands_{dataset}.txt

3. **Run VMAF Simulations** 
   Edit the variable dataset="" in run_vmaf_simulation.py 
   ```bash
   python3 run_vmaf_simulation.py
   ```
   Json results in /home/greco/home/docker/Result/{dataset}/vmaf_results
   
   Output= /home/greco/home/docker/Result/{dataset}/analyzescriptcommands_{dataset}.txt

4. **Generate Final CSV**  
   Edit the variable dataset="" in run_analyze_script_simulation.py
   ```bash
    python3 run_analyze_script_simulation.py
   ```
   Output= /home/greco/home/docker/Result/{dataset}/combined_results_{dataset}.csv


5. **Generate Graphs**  
   Edit the variable dataset="" in graph_simulations_run.py
   ```bash
   python3 graph_simulations_run.py
   ```
   Graph results in /home/greco/home/docker/Result/{dataset}/graph_results
