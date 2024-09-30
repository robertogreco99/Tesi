#!/bin/bash

# Directory dei video di input
INPUT_DIR="/inputs"
# Directory per salvare i risultati
OUTPUT_DIR="/results"
# Modello VMAF da utilizzare
VMAF_MODEL="/vmaf/model/vmaf_v0.6.1.json"

# Controllo se la directory di input esiste
if [ ! -d "$INPUT_DIR" ]; then
    echo "Errore: la directory di input '$INPUT_DIR' non esiste."
    exit 1
fi

# Codifica e valutazione con vmaf
#Parto con input in mp4 ( file è h.264)
video_coding_vmafevaluation(){
input_file=$1
video_name=$(basename "$input_file" .mp4)

# Codifica in h264 : avc
echo "Codificando $video_name in H.264..."
ffmpeg -i "$input_file" -c:v libx264 "$OUTPUT_DIR/${video_name}_h264.mp4"
# Codifica in in H.265 : hevc
echo "Codificando $video_name in H.265..."
ffmpeg -i "$input_file" -c:v libx265 "$OUTPUT_DIR/${video_name}_h265.mp4"
# Codifica in AV1
#echo "Codificando $video_name in AV1..."
#ffmpeg -i "$input_file" -c:v libaom-av1 -crf 30 -b:v 2000k "$OUTPUT_DIR/${video_name}_av1.mp4"

# Valutazione con libvmaf per H.264 (avc)
echo "Valutazione qualità per $video_name H.264..."
ffmpeg -i "$OUTPUT_DIR/${video_name}_h264.mp4" -i "$input_file" -lavfi "libvmaf=log_path=$OUTPUT_DIR/${video_name}_h264_vmaf.json:log_fmt=json" -f null -



# Valutazione con libvmaf per H.265 (hevc)
echo "Valutazione qualità per $video_name H.265..."
ffmpeg -i "$OUTPUT_DIR/${video_name}_h265.mp4" -i "$input_file" -lavfi "libvmaf=log_path=$OUTPUT_DIR/${video_name}_h265_vmaf.json:log_fmt=json" -f null -



# Valutazione con libvmaf per AV1
#echo "Valutazione qualità per $video_name AV1..."
#ffmpeg -i "$OUTPUT_DIR/${video_name}_AV1.mp4" -i "$input_file" -lavfi "libvmaf=log_path=$OUTPUT_DIR/${video_name}_av1_vmaf.json:log_fmt=json" -f null -

## Stampa della fine 
echo "Processo completato per $video_name"
}

# Scorri tutti i file .mp4 nella directory di input e chiama la funzione
for video_file in "$INPUT_DIR"/*.mp4; do
    if [ -f "$video_file" ]; then
        video_coding_vmafevaluation "$video_file"
    else
        echo "Nessun file video trovato in '$INPUT_DIR'."
    fi
done

