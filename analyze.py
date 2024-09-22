import json
import pandas as pd
import matplotlib.pyplot as plt
import os

# Dove metto i risultati 
result_folder = "/results"

# Funzione per analizzare i risultati VMAF
def vmaf_analyze_results(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    # Estraggo  i punteggi VMAF frame-by-frame
    vmaf_scores = [frame['metrics']['vmaf'] for frame in data['frames']]
    
    # Applico i vari metodi di temporal pooling
    mean_vmaf = sum(vmaf_scores) / len(vmaf_scores)
    median_vmaf = sorted(vmaf_scores)[len(vmaf_scores) // 2]
    
    return mean_vmaf, median_vmaf, vmaf_scores

# Lista dove salvo i risultati
results = []

# Analizzo tutti i json nella cartella
for json_file in os.listdir(result_folder):
    if json_file.endswith(".json"):
        mean, median, vmaf_scores = vmaf_analyze_results(os.path.join(result_folder, json_file))
        results.append((json_file, mean, median))
        print(f"File: {json_file}, Mean VMAF: {mean}, Median VMAF: {median}")

# Converti i risultati in un DataFrame per una gestione migliore
df_results = pd.DataFrame(results, columns=["File", "Mean VMAF", "Median VMAF"])
