import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
from scipy.stats import gmean
import os  

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
fps = sys.argv[12]
duration = sys.argv[13]
mos_dir = sys.argv[14]
mos = -1
ci = -1
computed_mos = -1

print(f"width_old: {width_old}, height_old: {height_old}")

# Verifica se il CSV esiste
csv_filename = f'/results/combined_results_{dataset}.csv'

# Se il CSV non esiste, crealo con 7 righe
if not os.path.isfile(csv_filename):
    print("Il CSV non esiste, lo creo...")
    # Definisci le righe da aggiungere, inclusa la colonna temporal_pooling
    temporal_pooling_values = ['mean', 'harmonic_mean', 'geometric_mean', 'total_variation', 'norm_lp1', 'norm_lp2', 'norm_lp']
    new_rows = [
        {
            "Dataset": dataset,
            "Original file name": original_video,
            "Distorted file name": distorted_video,
            "Width original": width_old,
            "Height original": height_old,
            "Width": width,
            "Height": height,
            "Bitrate": bitrate,
            "Video Codec": video_codec,
            "FPS": fps,
            "Duration": duration,
            "MOS": mos,
            "CI": ci,
            "ComputedMos": computed_mos,
            "temporal_pooling": temporal_pooling_value
        }
        for temporal_pooling_value in temporal_pooling_values  # Crea 7 righe, ognuna con un valore diverso per temporal_pooling
    ]
    
    # Crea un DataFrame con le nuove righe
    new_df = pd.DataFrame(new_rows)
    
    # Scrivi il DataFrame nel CSV e aggiungi gli header
    new_df.to_csv(csv_filename, mode='w', header=True, index=False)
    print("CSV creato con successo con gli header.")
else:
    # Se il CSV esiste, verifica se distorted_video è già presente
    print("Il CSV esiste già, verifico se il distorted_video è presente...")
    df_existing = pd.read_csv(csv_filename)
    
    # Controlla se il distorted_video è già presente nel CSV
    if distorted_video not in df_existing['Distorted file name'].values:
        print(f"{distorted_video} non trovato nel CSV, aggiungo le righe...")
        
        # Definisci le righe da aggiungere
        temporal_pooling_values = ['mean', 'harmonic_mean', 'geometric_mean', 'total_variation', 'norm_lp1', 'norm_lp2', 'norm_lp']
        new_rows = [
            {
                "Dataset": dataset,
                "Original file name": original_video,
                "Distorted file name": distorted_video,
                "Width original": width_old,
                "Height original": height_old,
                "Width": width,
                "Height": height,
                "Bitrate": bitrate,
                "Video Codec": video_codec,
                "FPS": fps,
                "Duration": duration,
                "MOS": mos,
                "CI": ci,
                "ComputedMos": computed_mos,
                "temporal_pooling": temporal_pooling_value
            }
            for temporal_pooling_value in temporal_pooling_values  # Crea 7 righe, ognuna con un valore diverso per temporal_pooling
        ]
        
        # Aggiungi le nuove righe al DataFrame esistente
        new_df = pd.DataFrame(new_rows)
        df_existing = pd.concat([df_existing, new_df], ignore_index=True)
        # Scrivi il DataFrame aggiornato nel CSV
        df_existing.to_csv(csv_filename, mode='w', header=True, index=False)
        print("7 righe aggiunte al CSV.")
    else:
        print(f"{distorted_video} è già presente nel CSV, non viene fatto nulla.")
