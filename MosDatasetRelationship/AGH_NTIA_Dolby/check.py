import json

# Legge il file JSON
with open('/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Dataset/AGH_NTIA_Dolby.json', 'r') as json_file:
    data = json.load(json_file)

# Legge la lista dei file con MOS dal file di testo
with open('/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/MosDatasetRelationship/AGH_NTIA_Dolby/AllScoresAGH_NTIA_Dolby.txt', 'r') as txt_file:
    mos_files = {line.strip() for line in txt_file.readlines()}  # Usa un set per efficienza

# Estrae solo i nomi dei file presenti sia nel JSON che nel file TXT
matching_files = [
    video["file_name"] for video in data["distorted_videos"]
    if video["file_name"] in mos_files
]

# Salva la lista dei file corrispondenti su file
with open('matching_files.txt', 'w') as output_file:
    for file_name in matching_files:
        output_file.write(file_name + '\n')

print("La lista dei file corrispondenti è stata salvata in 'matching_files.txt'.")
