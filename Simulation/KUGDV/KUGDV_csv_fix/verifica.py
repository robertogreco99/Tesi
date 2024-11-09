import pandas as pd

def carica_righe_attese(file_txt):
    # Legge il file di testo e restituisce le righe come una lista
    with open(file_txt, 'r') as f:
        righe_attese = [line.strip() for line in f if line.strip()]
    return righe_attese

def verifica_righe(csv_file, file_txt, occorrenze_attese=9):
    # Carica le righe attese dal file di testo
    righe_attese = carica_righe_attese(file_txt)
    
    # Leggi il file CSV
    df = pd.read_csv(csv_file)
    
    # Assumiamo che il nome del file sia in una colonna chiamata 'NomeFile'
    colonna = 'Distorted file name'
    
    # Verifica che ogni riga sia presente esattamente 9 volte
    for riga in righe_attese:
        count = df[colonna].value_counts().get(riga, 0)
        if count != occorrenze_attese:
            print(f"La riga '{riga}' è presente {count} volte, ma dovrebbe essere {occorrenze_attese} volte.")
        else:
            print(f"La riga '{riga}' è presente esattamente {occorrenze_attese} volte.")

# Esempio di utilizzo
verifica_righe('combined_results_senza_duplicati.csv', 'righe_attese.txt')
