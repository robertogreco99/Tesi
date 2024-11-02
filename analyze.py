import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
from scipy.stats import gmean
import os  

# Initialize an empty list to hold all metrics results
all_metrics_results = []

if len(sys.argv) != 15:
    print("Error, format is : python3 analyze.py <dataset> <width> <height> <bitrate> <video_codec> <model_version> <output_directory> <original_video> <distorted_video> <width_old> <height_old> <fps> <duration> <mos_dir>")
    sys.exit(1)

# Parameters
dataset = sys.argv[1]        
width = int(sys.argv[2])     
height = int(sys.argv[3])    
bitrate = int(sys.argv[4])   
video_codec = sys.argv[5]   
model_version = sys.argv[6] 
output_directory = sys.argv[7] 
original_video = sys.argv[8]  
distorted_video = sys.argv[9]
width_old = sys.argv[10]
height_old = sys.argv[11]
fps=sys.argv[12]
duration=sys.argv[13]
mos_dir=sys.argv[14]

print(f"width_old: {width_old}, height_old: {height_old}")

# Directory for graph results
if width_old != '1920' or height_old != '1080':
    graph_directory = os.path.join(
        output_directory,
        dataset,
        original_video,
        f"{dataset}__{width_old}x{height_old}__{bitrate}_{video_codec}__{model_version}_resized_{width}x{height}"
    )
else:
    graph_directory = os.path.join(
        output_directory,
        dataset,
        original_video,
        f"{dataset}__{width_old}x{height_old}__{bitrate}_{video_codec}__{model_version}"
    )

os.makedirs(graph_directory, exist_ok=True)

# Create the JSON path name
if width_old != '1920' or height_old != '1080':
    json_filename = f'/results/result__{dataset}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}_resized_{width}x{height}.json'
else:
    json_filename = f'/results/result__{dataset}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}.json'

# Print json filename
print(f"Json file path: {json_filename}")

# Read the JSON file
with open(json_filename) as f:
    data = json.load(f)

# Take data from the frames
frames_list = data["frames"]
frames_rows = []

for frame in frames_list:
    frame_num = frame["frameNum"]
    metrics = frame["metrics"]
    row = {"frameNum": frame_num}
    row.update(metrics)
    frames_rows.append(row)

# Create a DataFrame for current file's metrics
dframes = pd.DataFrame(frames_rows)
print(dframes)

# Function to calculate metrics
def calculate_metrics(column_name):
    if column_name in dframes.columns:
        mean_value = dframes[column_name].mean()
        harmonic_mean_value = 1.0 / np.mean(1.0 / (dframes[column_name] + 1.0)) - 1.0
        geometric_mean_value = gmean(dframes[column_name])
        
        percentiles = {
            '1%': np.percentile(dframes[column_name], 1),
            '5%': np.percentile(dframes[column_name], 5),
            '10%': np.percentile(dframes[column_name], 10),
            '20%': np.percentile(dframes[column_name], 20),
        }
        
        # Print values
        print(f"{column_name} Mean: {mean_value}")
        print(f"Harmonic mean {column_name}: {harmonic_mean_value}")
        print(f"Geometric mean {column_name}: {geometric_mean_value}")
        print(f"{column_name} Percentiles:")
        for p, value in percentiles.items():
            print(f"{p}: {value}")
        
        # Total variation
        abs_diff_scores = np.absolute(np.diff(dframes[column_name]))
        total_variation = np.mean(abs_diff_scores)
        print(f"Total variation {column_name}: {total_variation}")

        # Norms
        norm_lp_1 = np.power(np.mean(np.power(np.array(dframes[column_name]), 1)), 1.0 / 1)  # Norm L_1
        print(f"Norm L_1 of {column_name} values is: {norm_lp_1}")

        norm_lp_2 = np.power(np.mean(np.power(np.array(dframes[column_name]), 2)), 1.0 / 2)  # Norm L_2
        print(f"Norm L_2 of {column_name} values is: {norm_lp_2}")

        norm_lp_3 = np.power(np.mean(np.power(np.array(dframes[column_name]), 3)), 1.0 / 3)  # Norm L_3
        print(f"Norm L_3 of {column_name} values is: {norm_lp_3}")

        return mean_value, harmonic_mean_value, geometric_mean_value, total_variation, norm_lp_1, norm_lp_2, norm_lp_3
    else:
        print(f"Metric '{column_name}' not found in the DataFrame.")
        return (None, None, None, None, None, None, None)

# List of metrics to evaluate
metrics_to_evaluate = [
    "vmaf",
    "cambi",
    "float_ssim",
    "psnr_y",
    "psnr_cb",
    "psnr_cr",
    "float_ms_ssim",
    "ciede2000",
    "psnr_hvs_y",
    "psnr_hvs_cb",
    "vmaf_bagging",      
    "vmaf_stddev",       
    "vmaf_ci_p95_lo",    
    "vmaf_ci_p95_hi" 
]
vmaf_models=[
                "vmaf_v0.6.1.json", 
                "vmaf_v0.6.1neg.json", 
                "vmaf_float_v0.6.1.json", 
                "vmaf_float_v0.6.1neg.json", 
                "vmaf_float_b_v0.6.3.json", 
                "vmaf_b_v0.6.3.json", 
                "vmaf_float_4k_v0.6.1.json", 
                "vmaf_4k_v0.6.1.json", 
                "vmaf_4k_v0.6.1neg.json"
            ]

metrics_results = {}
for metric in metrics_to_evaluate:
    results = calculate_metrics(metric)
    if results:
        metrics_results[metric] = results

print("METRICS RESULTS")
print(metrics_results)

all_metrics_results.append({
    "Dataset": dataset,
    "Original file name": original_video,
    "Width original": width_old,
    "Height original": height_old,
    "Width": width,
    "Height": height,
    "Bitrate": bitrate,
    "Video Codec": video_codec,
    "FPS" : fps,
    "Duration" : duration,
    "Model Version": model_version,
})

print(dataset)
 # Read the database  mos file name 
mos_dataset = f"/mos/Scores{dataset}.json"
print(mos_dataset)

# Read the JSON file
with open(mos_dataset) as f:
    data_mos = json.load(f)

mos = None
os_values = [None] * 17

distorted_file_name_no_extension = distorted_video.rsplit(".", 1)[0]  


for score in data_mos["scores"]:
    if score["PVS"]["PVS_ID"] == distorted_file_name_no_extension:
        print(score["PVS"]["PVS_ID"])  
        print(distorted_file_name_no_extension)
        
        mos = score["MOS"]  
        for i in range(1,18):  
            mos_value = score["OS"][str(i)]
            if mos_value is not None:  
                os_values[i-1] = mos_value
            else:
                os_values[i-1] = None  
        break  
else:
    print("No mos found")

print(mos)
print(os_values)
all_metrics_results[-1].update({
                    f"MOS": {mos},
                })
for i in range(1, 18):
    all_metrics_results[-1][f"OS_{i}"] = os_values[i-1]



for metric, values in metrics_results.items():
    if metric == "vmaf":
        mean_value, harmonic_mean_value, geometric_mean_value, total_variation, norm_lp_1, norm_lp_2, norm_lp_3 = values
        
        # Create columns for every vmaf model
        for model in vmaf_models:
            if model == model_version:
                all_metrics_results[-1].update({
                    f"{metric}_{model}_mean": mean_value,
                    f"{metric}_{model}_harmonic_mean": harmonic_mean_value,
                    f"{metric}_{model}_geometric_mean": geometric_mean_value,
                    f"{metric}_{model}_total_variation": total_variation,
                    f"{metric}_{model}_norm_lp_1": norm_lp_1,
                    f"{metric}_{model}_norm_lp_2": norm_lp_2,
                    f"{metric}_{model}_norm_lp_3": norm_lp_3,
                })
            else:
                # The value is None if the model is not the current
                all_metrics_results[-1].update({
                    f"{metric}_{model}_mean": None,
                    f"{metric}_{model}_harmonic_mean": None,
                    f"{metric}_{model}_geometric_mean": None,
                    f"{metric}_{model}_total_variation": None,
                    f"{metric}_{model}_norm_lp_1": None,
                    f"{metric}_{model}_norm_lp_2": None,
                    f"{metric}_{model}_norm_lp_3": None,
                })
    else:
        mean_value, harmonic_mean_value, geometric_mean_value, total_variation, norm_lp_1, norm_lp_2, norm_lp_3 = values
        
        # Create columns for other metrics
        all_metrics_results[-1].update({
            f"{metric}_mean": mean_value,
            f"{metric}_harmonic_mean": harmonic_mean_value,
            f"{metric}_geometric_mean": geometric_mean_value,
            f"{metric}_total_variation": total_variation,
            f"{metric}_norm_lp_1": norm_lp_1,
            f"{metric}_norm_lp_2": norm_lp_2,
            f"{metric}_norm_lp_3": norm_lp_3,
        })


df_all_metrics = pd.DataFrame(all_metrics_results)
csv_filename = f'/results/combined_results.csv'

# Append to CSV 
if os.path.isfile(csv_filename):
    df_all_metrics.to_csv(csv_filename, mode='a', header=False, index=False)
else:
    df_all_metrics.to_csv(csv_filename, mode='w', header=True, index=False)

print("Combined CSV updated.")
