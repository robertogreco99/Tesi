#!/bin/bash

# Cicla attraverso tutti i file che iniziano con 'result__KUGVD__' nella directory corrente
for file in result__KUGVD__*; do
    # Verifica se il file esiste
    if [ -f "$file" ]; then
        # Estrai la parte del nome del file dopo 'KUGVD__'
        rest="${file#result__KUGVD__}"
        
        # Crea il nuovo nome aggiungendo 'CSGO_30fps_30sec_v2.yuv' dopo 'KUGDV'
        new_name="result__KUGVD__CSGO_30fps_30sec_v2.yuv__${rest}"
        
        # Rinomina il file
        mv "$file" "$new_name"
    fi
done
