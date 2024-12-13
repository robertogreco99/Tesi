# How to run

1. **Build Podman Image**  
   ```bash
   podman build -t <imageName>:<tag> <folder>   
    ```
- `imageName`:  Assigns a name and optionally a tag to the image being built
- `folder`: Specifies the directory containing the Dockerfile and all the required files for the build
  
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
    "DATASET_DIR": "/home/greco/home/docker/Dataset",
    "SIMULATIONS_DIR": "/home/greco/home/docker/Simulations",
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
    ],
    "USE_LIBVMAF": true,
    "USE_ESSIM": true,
    "ESSIM_PARAMETERS": {
        "Window_size": "8",
        "Window_stride": "4",
        "SSIM_Minkowski_pooling": "3",
        "Mode": "2"
    }
}
```

3. **Generate Podman Commands**  
   ```bash
   python3 run_simulation_create_commands.py Json/config.json
   ```
   Output = {output_dir}/{dataset}/commands_{dataset}.txt

3. **Run VMAF Simulations** 
   ```bash
   python3 run_vmaf_simulation.py Json/config.json
   ```
   Json results in {output_dir}/{dataset}/vmaf_results
   
   Output= /home/greco/home/docker/Result/{dataset}/analyzescriptcommands_{dataset}.txt

   Results:

    - If use_libvmaf is set to true: results will be saved in {output_dir}/{dataset}/vmaf_results.Otherwise, no results will be generated.

    - If use_essim is set to true: results will be saved in {output_dir}/{dataset}/essim_results.Otherwise, no results will be generated.

    General output:  /home/greco/home/docker/Result/{dataset}/analyzescriptcommands_{dataset}.txt.

4. **Generate Final CSV**  
   ```bash
    chmod +x run_create_csv.sh
    ./run_create_csv.sh
   ```
   Output= {output_dir}/{dataset}/combined_results_{dataset}.csv


5. **Generate Graphs**  
   ```bash
    chmod +x run_create_graphs.sh
    ./run_create_csv.sh
   ```
   Graph results in {output_dir}/{dataset}/graph_results
