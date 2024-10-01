import pandas as pd
import json

# Leggi il file JSON
with open('/results/result__KUGVD__1920x1080__600_x264__vmaf_v0.6.1.json') as f:
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

# Save as .csv in results/metrics.csv
df.to_csv('/results/result__KUGVD__1920x1080__600_x264__vmaf_v0.6.1.json.csv', index=False)

print("Csv ending")
