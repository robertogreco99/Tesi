import json

# Percorsi dei file
text_file = "AVT-VQDB-UHD-1_3withScores.txt"
json_file = "/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Dataset/AVT-VQDB-UHD-1_3.json"

# Leggi le righe del file di testo
with open(text_file, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

# Leggi il file JSON
with open(json_file, "r") as f:
    data = json.load(f)

# Estrai tutti i filename dal vettore "distorted_videos", rimuovendo ".mp4" o ".mkv" dal campo "file_name"
distorted_videos = data.get("distorted_videos", [])
json_filenames = {
    entry.get("file_name", "").removesuffix(".mp4").removesuffix(".mkv") 
    for entry in distorted_videos if "file_name" in entry
}

# Verifica se ciascuna riga del file di testo è presente nei filename JSON
for line in lines:
    line_without_ext = line.removesuffix(".mp4").removesuffix(".mkv")  # Rimuovi estensioni se ci sono
    if line_without_ext in json_filenames:
        print(f"{line} -> Trovato")
    else:
        print(f"{line} -> Non trovato")
