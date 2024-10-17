import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
from scipy.stats import gmean
import os  


if len(sys.argv) != 9:
    print("Error , format is : python analyze.py <dataset> <width> <height> <bitrate> <video_codec> <model_version> <output_directory> <original_video>")
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


graph_directory = os.path.join(
    output_directory,
    dataset,
    original_video,
    f"{dataset}__{width}x{height}__{bitrate}_{video_codec}__{model_version}"
)
os.makedirs(graph_directory, exist_ok=True)


# Create the json  path name
json_filename = f'/results/result__{dataset}__{width}x{height}__{bitrate}__{video_codec}__{model_version}.json'
# Read the 
with open(json_filename) as f:
    data = json.load(f)

# Take data from pooled frames
frames_list = data["frames"]
frames_rows = []

for frame in frames_list:
    frame_num = frame["frameNum"]
    metrics = frame["metrics"]
    row = {"frameNum": frame_num}
    row.update(metrics)
    frames_rows.append(row)

# A new dataframe
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

        # Lp norm
        p = 2
        norm_lp = np.power(np.mean(np.power(dframes[column_name], p)), 1.0 / p)
        print(f"Norm L_{p} of {column_name} values is: {norm_lp}")
        
        return mean_value, harmonic_mean_value, geometric_mean_value, total_variation, norm_lp
    else:
        print(f"Metric '{column_name}' not found in the DataFrame.")
        return None

# List of metrics to evaluate
metrics_to_evaluate = [
    "cambi",
    "float_ssim",
    "psnr_y",
    "psnr_cb",
    "psnr_cr",
    "float_ms_ssim",
    "ciede2000",
    "psnr_hvs_y",
    "psnr_hvs_cb",
    "psnr_hvs_cr",
    "psnr_hvs",
    "vmaf"
]

metrics_results = {}
for metric in metrics_to_evaluate:
    results = calculate_metrics(metric)
    if results:
        metrics_results[metric] = results

# Create scatter plots for each metric
def create_scatter_plot(x, y, x_label, y_label, title, output_img):
    plt.scatter(x, y, color='blue')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.savefig(output_img)
    plt.close()
    print(f"Plot saved as {output_img}")

# Scatter plots for metrics
for metric, values in metrics_results.items():
    mean_value, harmonic_mean_value, geometric_mean_value, total_variation, norm_lp = values
    create_scatter_plot(mean_value, harmonic_mean_value, 'Mean', 'Harmonic Mean',
                     f'{metric} Mean vs {metric} Harmonic Mean',
                     os.path.join(graph_directory, f'{metric}_mean_vs_harmonic_mean.png'))

    create_scatter_plot(mean_value, geometric_mean_value, 'Mean', 'Geometric Mean',
                     f'{metric} Mean vs {metric} Geometric Mean',
                     os.path.join(graph_directory, f'{metric}_mean_vs_geometric_mean.png'))

    create_scatter_plot(mean_value, total_variation, 'Mean', 'Total Variation',
                     f'{metric} Mean vs {metric} Total Variation',
                     os.path.join(graph_directory, f'{metric}_mean_vs_total_variation.png'))

    create_scatter_plot(mean_value, norm_lp, 'Mean', f'Norm L_{2}',
                     f'{metric} Mean vs Norm L_{2}',
                     os.path.join(graph_directory, f'{metric}_mean_vs_lp_norm.png'))    

# Save the metrics to CSV
rows = []
for metric, values in metrics_results.items():
    mean_value, harmonic_mean_value, geometric_mean_value, total_variation, norm_lp = values
    rows.append({
        "Metric": metric,  
        "Mean": mean_value,
        "Harmonic Mean": harmonic_mean_value,
        "Geometric Mean": geometric_mean_value,
        "Total Variation": total_variation,
        "Norm L_2": norm_lp
    })

# Create a DataFrame and save it as CSV
df_metrics = pd.DataFrame(rows)
csv_filename = f'/results/result__{dataset}__{width}x{height}__{bitrate}_{video_codec}__{model_version}.json.csv'
df_metrics.to_csv(csv_filename, index=False)

print("Csv ending")
