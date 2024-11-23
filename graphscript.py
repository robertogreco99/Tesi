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
    vmaf_models = [
        "vmaf_v0.6.1", "vmaf_v0.6.1neg", "vmaf_float_v0.6.1", "vmaf_float_v0.6.1neg",
        "vmaf_float_b_v0.6.3", "vmaf_b_v0.6.3", "vmaf_float_4k_v0.6.1", 
        "vmaf_4k_v0.6.1", "vmaf_4k_v0.6.1neg",
    ]
    features = ["cambi", "float_ssim", "psnr_y",
        "psnr_cb", "psnr_cr", "float_ms_ssim", "ciede2000", "psnr_hvs_y",
        "psnr_hvs_cb", "vmaf_float_b_v0.6.3_bagging",
        "vmaf_b_v0.6.3_bagging", 
        ]
    temporal_pooling_values = ["mean", "harmonic_mean", "geometric_mean", "total_variation", "norm_lp1", "norm_lp2", "norm_lp3"]
    temporal_pooling_graph = ["mean", "harmonic_mean", "geometric_mean","norm_lp1", "norm_lp2", "norm_lp3"]

    lo_column_float_b = "vmaf_float_b_v0.6.3_ci_p95_lo"
    hi_column_float_b = "vmaf_float_b_v0.6.3_ci_p95_hi"
    lo_column_b = "vmaf_b_v0.6.3_ci_p95_lo"
    hi_column_b = "vmaf_b_v0.6.3_ci_p95_hi"
    stddev_column_float_b_v0_6_3 = "vmaf_float_b_v0.6.3_stddev"
    stddev_column_b_v0_6_3 = "vmaf_b_v0.6.3_stddev"
    
    if x_column not in data.columns:
        raise ValueError(f"Columns {x_column} not found in the csv for {dataset}.")

    output_path = f"/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Graph_results/Scatter_{dataset}"
    os.makedirs(output_path, exist_ok=True)

    vmaf_output_path = os.path.join(output_path, "VMAF_Models")
    features_output_path = os.path.join(output_path, "Features")
    hi_lo_output_path = os.path.join(output_path,"HI_LO")
    pvs_path=os.path.join(output_path,"PVS")
    os.makedirs(vmaf_output_path, exist_ok=True)
    os.makedirs(features_output_path, exist_ok=True)
    os.makedirs(hi_lo_output_path, exist_ok=True)
    os.makedirs(pvs_path, exist_ok=True)



    # Extract unique values for the graphs
    video_codecs = data['Video_codec'].unique()
    FPS_values = data['FPS'].unique()
    Duration_values = data['Duration'].unique()
    bitrate_values = data['Bitrate'].unique()
    vmaf_float_b_values = data['vmaf_float_b_v0.6.3'].unique()
    vmaf_b_values = data['vmaf_b_v0.6.3'].unique()

    # Unique pvs
    pvs=data['Distorted_file_name'].unique()

    colors_video_codec = plt.cm.tab10(np.linspace(0, 1, len(video_codecs)))
    colors_FPS = plt.cm.viridis(np.linspace(0, 1, len(FPS_values)))
    colors_Duration = plt.cm.plasma(np.linspace(0, 1, len(Duration_values)))
    colors_bitrate = plt.cm.cool(np.linspace(0, 1, len(bitrate_values)))
    colors_temporal_pooling=plt.cm.twilight(np.linspace(0,1,len(temporal_pooling_graph)))

    # Create dictionary to map the colors
    codec_color_map = {codec: colors_video_codec[i] for i, codec in enumerate(video_codecs)}
    FPS_color_map = {FPS: colors_FPS[i] for i, FPS in enumerate(FPS_values)}
    Duration_color_map = {Duration: colors_Duration[i] for i, Duration in enumerate(Duration_values)}
    bitrate_color_map = {bitrate: colors_bitrate[i] for i, bitrate in enumerate(bitrate_values)}
    temporal_pooling_color_map={temporal_pooling : colors_temporal_pooling[i] for i ,temporal_pooling in enumerate(temporal_pooling_graph)}


    # Per every temporal pooling create different graph
    """
    for temporal_pooling_value in temporal_pooling_values:
        filtered_data = data[data['temporal_pooling'] == temporal_pooling_value]

        if filtered_data.empty:
            print(f"No data found for the temporal pooling: {temporal_pooling_value} in dataset {dataset}")
            continue
        
        # Video Codec
        if len(video_codecs) > 1:
            for y_column in vmaf_models + features:
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
              
              if y_column in vmaf_models:
                  output_file = f"{vmaf_output_path}/scatter_{y_column}_{temporal_pooling_value}_video_codec.png"
              else:
                  output_file = f"{features_output_path}/scatter_{y_column}_{temporal_pooling_value}_video_codec.png"
                
              plt.savefig(output_file, bbox_inches='tight')
              print(f"Graph saved: {output_file}")
              plt.close()
        else :
            print("There is only one video codec")
        
        # FPS
        if len(FPS_values) > 1 and max(FPS_values) - min(FPS_values) >= 15:
            for y_column in vmaf_models + features:
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

                if y_column in vmaf_models:
                    output_file = f"{vmaf_output_path}/scatter_{y_column}_{temporal_pooling_value}_FPS.png"
                else:
                    output_file = f"{features_output_path}/scatter_{y_column}_{temporal_pooling_value}_FPS.png"

                plt.savefig(output_file, bbox_inches='tight')
                print(f"Graph saved: {output_file}")
                plt.close()
        else :
            print("There are only similar fps values")
        # Duration
        
        for y_column in vmaf_models + features:
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

            if y_column in vmaf_models:
                output_file = f"{vmaf_output_path}/scatter_{y_column}_{temporal_pooling_value}_Duration.png"
            else:
                output_file = f"{features_output_path}/scatter_{y_column}_{temporal_pooling_value}_Duration.png"

            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()
            
        # float b model
        if temporal_pooling_value !="total_variation":
            if lo_column_float_b not in filtered_data.columns or hi_column_float_b not in filtered_data.columns:
               print(f"Columns {lo_column_float_b} or {hi_column_float_b} not found in {dataset}")
            else:
               plt.figure(figsize=(10, 6))
               for vmaf_float_b_value in vmaf_float_b_values:
                subset = filtered_data[filtered_data['vmaf_float_b_v0.6.3'] == vmaf_float_b_value]
                y_values = subset["vmaf_float_b_v0.6.3"].values  
                lo_values = subset["vmaf_float_b_v0.6.3_ci_p95_lo"].values 
                hi_values = subset["vmaf_float_b_v0.6.3_ci_p95_hi"].values  
                plt.errorbar(subset[x_column], y_values, yerr=[y_values-lo_values,hi_values-y_values], fmt='o')
         
               plt.title(f"{x_column} vs vmaf_float_b_v0.6.3 (temporal pooling: {temporal_pooling_value})")
               plt.xlabel("Mos")
               plt.ylabel("vmaf_float_b_v0.6.3")
               plt.grid(True)
          
               output_file = f"{hi_lo_output_path}/scatter_vmaf_float_b_v0.6.3_{temporal_pooling_value}.png"
               plt.savefig(output_file, bbox_inches='tight')
               print(f"Graph saved: {output_file}")
               plt.close()

            if stddev_column_float_b_v0_6_3 not in filtered_data.columns:
                print(f"Columns {stddev_column_float_b_v0_6_3}  not found in {dataset}")
            else:
                plt.figure(figsize=(10, 6))
                for vmaf_float_b_value in vmaf_float_b_values:
                    subset = filtered_data[filtered_data['vmaf_float_b_v0.6.3'] == vmaf_float_b_value]
                    y_values = subset["vmaf_float_b_v0.6.3"].values  
                    stddev_float_b_value = subset["vmaf_float_b_v0.6.3_stddev"].values
                    lo_values_float_stddev= y_values - stddev_float_b_value 
                    hi_values_float_stdev = y_values + stddev_float_b_value 
                    plt.errorbar(subset[x_column], y_values, yerr=[y_values-lo_values_float_stddev,hi_values_float_stdev-y_values], fmt='o')
              
                plt.title(f"{x_column} vs vmaf_float_b_v0.6.3 with stddev (temporal pooling: {temporal_pooling_value})")
                plt.xlabel("Mos")
                plt.ylabel("vmaf_float_b_v0.6.3")
                plt.grid(True)
          
                output_file = f"{hi_lo_output_path}/scatter_vmaf_float_b_v0.6.3_{temporal_pooling_value}_stddev.png"
                plt.savefig(output_file, bbox_inches='tight')
                print(f"Graph saved: {output_file}")
                plt.close()
        # b model
        if temporal_pooling_value !="total_variation":
            if lo_column_b not in filtered_data.columns or hi_column_b not in filtered_data.columns:
                print(f"Columns {lo_column_b} or {hi_column_b} not found in {dataset}")
            else:
                plt.figure(figsize=(10, 6))
                for vmaf_b_value in vmaf_b_values:
                    subset = filtered_data[filtered_data['vmaf_b_v0.6.3'] == vmaf_b_value]
                    y_values = subset["vmaf_b_v0.6.3"].values  
                    lo_values = subset["vmaf_b_v0.6.3_ci_p95_lo"].values  
                    hi_values = subset["vmaf_b_v0.6.3_ci_p95_hi"].values  
                    plt.errorbar(subset[x_column], y_values, yerr=[y_values-lo_values,hi_values-y_values], fmt='o')
           
                plt.title(f"{x_column} vs vmaf_b_v0.6.3 (temporal pooling: {temporal_pooling_value})")
                plt.xlabel("Mos")
                plt.ylabel("vmaf_b_v0.6.3")
                plt.grid(True)
            
                output_file = f"{hi_lo_output_path}/scatter_vmaf_b_v0.6.3_{temporal_pooling_value}.png"
                plt.savefig(output_file, bbox_inches='tight')
                print(f"Graph saved: {output_file}")
                plt.close()
         
            if stddev_column_b_v0_6_3 not in filtered_data.columns:
                print(f"Columns {stddev_column_b_v0_6_3}  not found in {dataset}")
            else:
                plt.figure(figsize=(10, 6))
                for vmaf_b_value in vmaf_b_values:
                    subset = filtered_data[filtered_data['vmaf_b_v0.6.3'] == vmaf_b_value]
                    y_values = subset["vmaf_b_v0.6.3"].values  
                    stddev_b_value = subset["vmaf_float_b_v0.6.3_stddev"].values
                    lo_values_b_stddev= y_values - stddev_b_value 
                    hi_values_b_stddev = y_values + stddev_b_value
                    plt.errorbar(subset[x_column], y_values, yerr=[y_values-lo_values_b_stddev,hi_values_b_stddev-y_values], fmt='o')
                    
                plt.title(f"{x_column} vs vmaf_b_v0.6.3 with stddev (temporal pooling: {temporal_pooling_value})")
                plt.xlabel("Mos")
                plt.ylabel("vmaf_float_b_v0.6.3")
                plt.grid(True)
          
                output_file = f"{hi_lo_output_path}/scatter_vmaf_b_v0.6.3_{temporal_pooling_value}_stddev.png"
                plt.savefig(output_file, bbox_inches='tight')
                print(f"Graph saved: {output_file}")
                plt.close()

        # Bitrate models and features
        for y_column in vmaf_models + features:
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

            if y_column in vmaf_models:
                output_file = f"{vmaf_output_path}/scatter_{y_column}_{temporal_pooling_value}_bitrate.png"
            else:
                output_file = f"{features_output_path}/scatter_{y_column}_{temporal_pooling_value}_bitrate.png"

            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()
"""  
    for pvs_value in pvs:
        output_dir = f"{pvs_path}/{pvs_value}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filtered_data = data[data['Distorted_file_name'] == pvs_value]

        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue

        x_value = filtered_data['MOS'].values[0]

        for feature in features:
            plt.figure(figsize=(10, 6))
            x_values = []
            y_values = []
            labels = []
            colors = []
            for temporal_pooling_value in temporal_pooling_graph:
                if temporal_pooling_value == "total_aggregation":
                    continue   
                temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
                if temporal_filtered_data.empty:
                    print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                    continue
                feature_value = temporal_filtered_data[feature].values
                x_values.append(x_value)  
                y_values.append(feature_value[0])  
                labels.append(f"{temporal_pooling_value}")
                colors.append(temporal_pooling_color_map[temporal_pooling_value])  
             # Aggiungi scatter per ogni metodo di pooling
            print(f"x value : {x_value}, y value : {y_values}")

            for i, temporal_pooling_value in enumerate(temporal_pooling_graph):
                if temporal_pooling_value == "total_aggregation":
                    continue
                plt.scatter(x_values[i], y_values[i], label=labels[i], color=colors[i], marker='o', alpha=0.7) 
            #plt.scatter(x_values, y_values, label=labels, color=features_color_map[feature], marker='o', alpha=0.7) 
            plt.title(f"{x_column} vs {feature} - feature:{feature}")
            plt.xlabel(x_column)
            plt.ylabel(feature)
            plt.grid(True)
            plt.legend(title="Temporal Pooling", loc='center left', bbox_to_anchor=(1, 0.5))

            output_file = f"{pvs_path}/{pvs_value}/scatter_{feature}.png"
            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()
    
    