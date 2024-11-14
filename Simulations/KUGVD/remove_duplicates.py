# Specifica il percorso del file di input e del file di output
input_file = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/KUGVD/analyzescriptcommands_KUGVD.txt'
output_file = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/KUGVD/analyzescriptcommands_KUGVDfixed.txt'

# Inizializza un set per memorizzare le righe uniche
unique_lines = set()

# Leggi il file di input e aggiungi solo le righe uniche
with open(input_file, 'r') as file:
    for line in file:
        # Rimuovi eventuali spazi bianchi o newline all'inizio/fine della riga
        line = line.strip()
        # Aggiungi la riga al set (ignora duplicati automaticamente)
        unique_lines.add(line)

# Scrivi le righe uniche nel file di output
with open(output_file, 'w') as file:
    for line in unique_lines:
        file.write(line + '\n')

print(f"Righe duplicate rimosse e salvate in {output_file}")
