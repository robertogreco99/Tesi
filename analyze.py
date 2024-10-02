import pandas as pd
import json

# Parameters : 
#VMAF model
model_version = "vmaf_v0.6.1"
# Dataset
dataset = "KUGVD"
# Dimensions 
width = 1920
height = 1080
# Bitrate
bitrate = 600
# Codec video
video_codec = "x264"
# Pixel format
pixel_format = 420
# Bit depth
bit_depth = 8

# Create the json filename
json_filename = f'/results/result__{dataset}__{width}x{height}__{bitrate}__{video_codec}__{model_version}.json'
# Read json filename
with open(json_filename) as f:
    data = json.load(f)

# Take data from pooled metrics
metrics = data["pooled_metrics"]
rows = []

# A row for every metric
for metric, values in metrics.items():
    rows.append({
        "Metric": metric,  
        "Min": values["min"],
        "Max": values["max"],
        "Mean": values["mean"],
        "Harmonic Mean": values["harmonic_mean"]
    })

#  A new dataframe
df = pd.DataFrame(rows)

csv_filename = f'/results/result__{dataset}__{width}x{height}__{bitrate}_{video_codec}__{model_version}.json.csv'

# Save as .csv in results/filename.csv
df.to_csv(csv_filename, index=False)

print("Csv ending")
