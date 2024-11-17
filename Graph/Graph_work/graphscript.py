import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

dataset = "KUGVD"

csv_file = f'/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/{dataset}/combined_results_{dataset}.csv'

if not os.path.exists(csv_file):
    print(f"File CSV for dataset {dataset} not found")
else:
    data = pd.read_csv(csv_file)

    x_column = "MOS"
    columns = [
        "vmaf_v0.6.1", "vmaf_v0.6.1neg", "vmaf_float_v0.6.1", "vmaf_float_v0.6.1neg",
        "vmaf_float_b_v0.6.3", "vmaf_b_v0.6.3", "vmaf_float_4k_v0.6.1", 
        "vmaf_4k_v0.6.1", "vmaf_4k_v0.6.1neg","cambi","float_ssim","psnr_y",
        "psnr_cb","psnr_cr","float_ms_ssim","ciede2000","psnr_hvs_y",
        "psnr_hvs_cb","vmaf_float_b_v0.6.3_bagging",
        "vmaf_float_b_v0.6.3_stddev","vmaf_float_b_v0.6.3_ci_p95_lo",
        "vmaf_float_b_v0.6.3_ci_p95_hi","vmaf_b_v0.6.3_bagging","vmaf_b_v0.6.3_stddev",
        "vmaf_b_v0.6.3_ci_p95_lo","vmaf_b_v0.6.3_ci_p95_hi"
    ]

    if x_column not in data.columns:
        raise ValueError(f"Columns {x_column} not found in the csv for {dataset}.")

    output_path = f"/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Graph/Graph_work/Graph_results/Scatter_{dataset}/Different_Video_codec_FPS_Duration"
    os.makedirs(output_path, exist_ok=True)

    # Extract unique values for the graphs
    video_codecs = data['Video_codec'].unique()
    FPS_values = data['FPS'].unique()
    Duration_values = data['Duration'].unique()
    bitrate_values = data['Bitrate'].unique()

    colors_video_codec = plt.cm.tab10(np.linspace(0, 1, len(video_codecs)))
    colors_FPS = plt.cm.viridis(np.linspace(0, 1, len(FPS_values)))
    colors_Duration = plt.cm.plasma(np.linspace(0, 1, len(Duration_values)))
    colors_bitrate = plt.cm.cool(np.linspace(0, 1, len(bitrate_values)))

    # Create dictionary to map the colors
    codec_color_map = {codec: colors_video_codec[i] for i, codec in enumerate(video_codecs)}
    FPS_color_map = {FPS: colors_FPS[i] for i, FPS in enumerate(FPS_values)}
    Duration_color_map = {Duration: colors_Duration[i] for i, Duration in enumerate(Duration_values)}
    bitrate_color_map = {bitrate: colors_bitrate[i] for i, bitrate in enumerate(bitrate_values)}

    temporal_pooling_values = ["mean", "harmonic_mean", "geometric_mean", "total_variation", "norm_lp1", "norm_lp2", "norm_lp3"]

    # Per every temporal pooling create different graph
    for temporal_pooling_value in temporal_pooling_values:
        filtered_data = data[data['temporal_pooling'] == temporal_pooling_value]

        if filtered_data.empty:
            print(f"No data found for the  temporal pooling: {temporal_pooling_value} in dataset {dataset}")
            continue
        
        # Video Codec
        for y_column in columns:
            if y_column not in filtered_data.columns:
                print(f"Columns {y_column} not found in {dataset}")
                continue

            plt.figure(figsize=(10, 6))

            for codec in video_codecs:
                subset = filtered_data[filtered_data['Video_codec'] == codec]
                plt.scatter(subset[x_column], subset[y_column], 
                            label=f'{codec} (Video Codec)', 
                            color=codec_color_map[codec], 
                            marker='o', alpha=0.7)

            plt.title(f"{x_column} vs {y_column} (temporal pooling: {temporal_pooling_value}) - Video Codec")
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.legend(title='Video Codec', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)

            output_file = f"{output_path}/scatter_{y_column}_temporal_pooling_{temporal_pooling_value}_video_codec.png"
            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()

        # FPS
        for y_column in columns:
            if y_column not in filtered_data.columns:
                print(f"Columns {y_column} not found in {dataset}")
                continue

            plt.figure(figsize=(10, 6))

            for FPS in FPS_values:
                subset = filtered_data[filtered_data['FPS'] == FPS]
                plt.scatter(subset[x_column], subset[y_column], 
                            label=f'{FPS} FPS', 
                            color=FPS_color_map[FPS], 
                            marker='x', alpha=0.5)

            plt.title(f"{x_column} vs {y_column} (temporal pooling: {temporal_pooling_value}) - FPS")
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.legend(title='FPS', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)

            output_file = f"{output_path}/scatter_{y_column}_temporal_pooling_{temporal_pooling_value}_FPS.png"
            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()

        # Duration
        for y_column in columns:
            if y_column not in filtered_data.columns:
                print(f"Columns {y_column} not found in {dataset}")
                continue

            plt.figure(figsize=(10, 6))

            for Duration in Duration_values:
                subset = filtered_data[filtered_data['Duration'] == Duration]
                plt.scatter(subset[x_column], subset[y_column], 
                            label=f'{Duration} Duration', 
                            color=Duration_color_map[Duration], 
                            marker='^', alpha=0.5)

            plt.title(f"{x_column} vs {y_column} (temporal pooling: {temporal_pooling_value}) - Duration")
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.legend(title='Duration', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)

            output_file = f"{output_path}/scatter_{y_column}_temporal_pooling_{temporal_pooling_value}_Duration.png"
            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()

        # Bitrate
        for y_column in columns:
            if y_column not in filtered_data.columns:
                print(f"Columns {y_column} not found in {dataset}")
                continue

            plt.figure(figsize=(10, 6))

            for bitrate in bitrate_values:
                subset = filtered_data[filtered_data['Bitrate'] == bitrate]
                plt.scatter(subset[x_column], subset[y_column], 
                            label=f'{bitrate} kbps', 
                            color=bitrate_color_map[bitrate], 
                            marker='s', alpha=0.5)

            plt.title(f"{x_column} vs {y_column} (temporal pooling: {temporal_pooling_value}) - Bitrate")
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.legend(title='Bitrate (kbps)', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)

            output_file = f"{output_path}/scatter_{y_column}_temporal_pooling_{temporal_pooling_value}_bitrate.png"
            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()
