import json

def parse_video_files(file_path, output_file):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    reference_videos = []
    distorted_videos = []
    current_list = None

    for line in lines:
        line = line.strip()
        if line == "ReferenceVideos":
            current_list = reference_videos
            continue
        elif line == "DistortedVideos":
            current_list = distorted_videos
            continue
        if line and current_list is not None:
            current_list.append(line)

    # Genera la struttura richiesta
    result = {
        "database": "KUGDV",
        "reference_videos": [{"id": i + 1, "file_name": video} for i, video in enumerate(reference_videos)],
        "distorted_videos": []
    }

    for video in distorted_videos:
        parts = video.split('_')
        try:
            # Ottieni le dimensioni dall'elemento corrispondente
            resolution = parts[-3].split('x')  # Splitta '1280x720'
            width = int(resolution[0])
            height = int(resolution[1])
            bitrate = int(parts[-2])  # bitrate è ora l'elemento giusto
            
            # Estrazione del codec video (x264, x265, ecc.)
            video_codec = parts[-1].split('.')[0]  # Cambiato per estrarre il codec
            
            # Estrazione di fps e durata dal nome
            fps = int(parts[1].replace('fps', ''))  # Supponendo che fps sia come '30fps'
            duration = int(parts[2].replace('sec', ''))  # Supponendo che la durata sia come '30sec'

            result["distorted_videos"].append({
                "id": len(result["distorted_videos"]) + 1,
                "file_name": video,
                "width": width,
                "height": height,
                "bitrate": bitrate,
                "video_codec": video_codec,
                "bitdepth": 8,
                "pixel_format": "420",
                "fps": fps,
                "duration": duration
            })
        except (IndexError, ValueError) as e:
            print(f"Errore nella riga '{video}': {e}")

    # Salva il risultato in un file JSON
    with open(output_file, 'w') as json_file:
        json.dump(result, json_file, indent=2)

# Percorso del file di input e nome del file di output
file_path = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/DatasetScript/KUGDV/KUGDVdescription.txt'
output_file = 'KUGDVjson.json'
parse_video_files(file_path, output_file)

print(f"File JSON salvato come {output_file}")
