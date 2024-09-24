import json
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

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


#  Creo il data frame
df_results = pd.DataFrame(results, columns=["File", "Mean VMAF", "Median VMAF"])
print(df_results)

# lista di indici da 0 alla dimensione del data frame
index = np.arange(len(df_results))
width = 0.3

plt.figure(figsize=(12, 6)) 

plt.title("Confronto di input vs Media e Mediana")
plt.bar(index, df_results['Mean VMAF'],width = width ,label='Mean VMAF', color='b')
plt.bar(index+width, df_results['Median VMAF'],width = width, label='Median VMAF', color='r')
plt.xticks(index+width/2, df_results['File'])
plt.legend()

# Salvo il grafico
plt.savefig('/results/vmaf_scores.png', format='png')