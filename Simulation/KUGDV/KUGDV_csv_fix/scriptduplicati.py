import pandas as pd

def process_csv(input_file, output_unique_file, output_duplicates_file):
    # Leggi il file CSV in un DataFrame
    df = pd.read_csv(input_file)

    # Trova le righe duplicate (considerando tutte le colonne) e salva in un file separato
    df_duplicates = df[df.duplicated(keep=False)]
    df_duplicates.to_csv(output_duplicates_file, index=False)

    # Rimuovi le righe duplicate e salva le righe uniche in un altro file
    df_unique = df.drop_duplicates()
    df_unique.to_csv(output_unique_file, index=False)

    print(f"File '{output_unique_file}' creato con le righe uniche.")
    print(f"File '{output_duplicates_file}' creato con le righe duplicate.")

# Esempio di utilizzo
process_csv('combined_results_duplicati.csv', 'combined_results_senza_duplicati.csv', 'output_duplicati.csv')
