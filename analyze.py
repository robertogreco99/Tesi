import pandas as pd
import json

# Parametri per il nome del file
# Modello VMAF
model_version = "vmaf_v0.6.1"
# Dataset
dataset = "KUGVD"
# Dimensioni
width = 1920
height = 1080
# Bitrate
bitrate = 600
# Codec video
video_codec = "x264"
# Formato pixel
pixel_format = 420
# Profondità del bit
bit_depth = 8

# Costruisci il nome del file JSON usando i parametri
json_filename = f'/results/result__{dataset}__{width}x{height}__{bitrate}__{video_codec}__{model_version}.json'
# Leggi il file JSON
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
