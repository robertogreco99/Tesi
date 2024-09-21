#!/bin/bash
# Directory dei video di input
INPUT_DIR="/videos"
# Directory per salvare i risultati (video codificati e risultati di valutazione)
OUTPUT_DIR="/results"
# Modello VMAF
VMAF_MODEL="/usr/local/share/model/vmaf_v0.6.1.pkl"
# Crea la directory di output se non esiste
mkdir -p "$OUTPUT_DIR"
# Funzione per codificare e valutare un file video
process_video() {
local input_file=$1
local base_name=$(basename "$input_file" .mp4)# Codifica in H.264
echo "Codificando $base_name in H.264..."
ffmpeg -i "$input_file" -c:v libx264 "$OUTPUT_DIR/${base_name}_h264.mp4"
# Codifica in H.265
echo "Codificando $base_name in H.265..."
ffmpeg -i "$input_file" -c:v libx265 "$OUTPUT_DIR/${base_name}_h265.mp4"
# Valutazione con libvmaf per H.264
echo "Valutazione qualità per $base_name H.264..."
ffmpeg -i "$OUTPUT_DIR/${base_name}_h264.mp4" -i "$input_file" -lavfi
libvmaf="model_path=$VMAF_MODEL" -f null - > "$OUTPUT_DIR/${base_name}_h264_vmaf.json"
# Valutazione con libvmaf per H.265
echo "Valutazione qualità per $base_name H.265..."
ffmpeg -i "$OUTPUT_DIR/${base_name}_h265.mp4" -i "$input_file" -lavfi
libvmaf="model_path=$VMAF_MODEL" -f null - > "$OUTPUT_DIR/${base_name}_h265_vmaf.json"
echo "Processo completato per $base_name"
}
