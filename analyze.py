import json
import pandas as pd
import matplotlib.pyplot as plt
import os

# Cartella con i risultati
result_folder = "./results"

# Funzione per analizzare i risultati VMAF
def analyze_vmaf(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    # Estrai i punteggi VMAF frame-by-frame
    vmaf_scores = [frame['metrics']['vmaf'] for frame in data['frames']]
    
    # Applica diversi metodi di temporal pooling
    mean_vmaf = sum(vmaf_scores) / len(vmaf_scores)
    median_vmaf = sorted(vmaf_scores)[len(vmaf_scores) // 2]
    
    return mean_vmaf, median_vmaf, vmaf_scores

# Lista per memorizzare i risultati
results = []

# Analizza tutti i file JSON nella cartella
for json_file in os.listdir(result_folder):
    if json_file.endswith(".json"):
        mean, median, vmaf_scores = analyze_vmaf(os.path.join(result_folder, json_file))
        results.append((json_file, mean, median))
        print(f"File: {json_file}, Mean VMAF: {mean}, Median VMAF: {median}")

# Converti i risultati in un DataFrame per una gestione migliore
df_results = pd.DataFrame(results, columns=["File", "Mean VMAF", "Median VMAF"])

# Visualizzazione dei risultati con matplotlib
plt.figure(figsize=(10, 6))
plt.bar(df_results["File"], df_results["Mean VMAF"], label="Mean VMAF", color="b", alpha=0.7)
plt.bar(df_results["File"], df_results["Median VMAF"], label="Median VMAF", color="r", alpha=0.5)
plt.xlabel("File")
plt.ylabel("VMAF Score")
plt.title("Mean and Median VMAF Scores for Each File")
plt.xticks(rotation=45, ha="right")
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig("vmaf_scores.png")
