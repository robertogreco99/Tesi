import os

def rename_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if "vmaf" in filename:
            # Aggiunge "30.0__" prima di "vmaf"
            new_filename = filename.replace("vmaf", "30.0__vmaf")
            # Costruisce i percorsi completi
            old_file_path = os.path.join(folder_path, filename)
            new_file_path = os.path.join(folder_path, new_filename)
            # Rinomina il file
            os.rename(old_file_path, new_file_path)
            print(f"Rinominato: {filename} -> {new_filename}")

# Specifica la cartella contenente i file
cartella = "."
rename_files_in_folder(cartella)
