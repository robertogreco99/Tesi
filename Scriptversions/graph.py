import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
import sys

if len(sys.argv) < 3:
    print("You need to call like graph_script <output_dir> <dataset_name>")
    sys.exit(1)
# define axis_limits
axis_limits = {
    "MOS": (1, 5),
    "vmaf_v0.6.1": (0, 100),
    "vmaf_v0.6.1neg" : (0, 100),
    "vmaf_float_v0.6.1": (0, 100),
    "vmaf_float_v0.6.1neg": (0,100),
    "vmaf_float_b_v0.6.3": (0,100),
    "vmaf_b_v0.6.3": (0,100),
    "vmaf_float_4k_v0.6.1": (0,100),
    "vmaf_4k_v0.6.1": (0,100),
    "vmaf_4k_v0.6.1neg": (0,100),
    "float_ssim": (0.6, 1),
    "float_ms_ssim": (0.6, 1),
    "psnr_y": (20, 50),
    "psnr_cb": (20, 50),
    "psnr_cr": (20, 50),
    "psnr_hvs_y": (20, 50),
    "psnr_hvs_cb" : (20, 50),
    "psnr_hvs_cr": (20, 50),
    "psnr_hvs": (20, 50),
    "ciede2000": (20, 50), #to do
    "cambi": (0, 10),  #to do
    "integer_vif_scale3" : (0.5,1),
    "vmaf_float_b_v0.6.3_bagging" :(0, 100),      
    "vmaf_float_b_v0.6.3_stddev" : (0, 100),       
    "vmaf_float_b_v0.6.3_ci_p95_lo":(0, 100),    
    "vmaf_float_b_v0.6.3_ci_p95_hi":(0, 100),
    "vmaf_b_v0.6.3_bagging":(0, 100),      
    "vmaf_b_v0.6.3_stddev":(0, 100),       
    "vmaf_b_v0.6.3_ci_p95_lo":(0, 100),    
    "vmaf_b_v0.6.3_ci_p95_hi":(0, 100),
}
output_dir = sys.argv[1]
dataset = sys.argv[2]
print(dataset)

csv_file = f'{output_dir}/{dataset}/combined_results_{dataset}.csv'
print(csv_file)

if not os.path.exists(csv_file):
    print(f"File CSV for dataset {dataset} not found")
else:
    data = pd.read_csv(csv_file)
    # define x columns, vmaf models, features, temporal pooling values and other for b models
    x_column = "MOS"
    vmaf_models = [
        "vmaf_v0.6.1", "vmaf_v0.6.1neg", "vmaf_float_v0.6.1", "vmaf_float_v0.6.1neg",
        "vmaf_float_b_v0.6.3", "vmaf_b_v0.6.3", "vmaf_float_4k_v0.6.1",
        "vmaf_4k_v0.6.1", "vmaf_4k_v0.6.1neg",
    ]
    features = ["cambi", "float_ssim", "psnr_y",
        "psnr_cb", "psnr_cr", "float_ms_ssim", "ciede2000", "psnr_hvs_y",
        "psnr_hvs_cb", "psnr_hvs_cr", "psnr_hvs","vmaf_float_b_v0.6.3_bagging",
        "vmaf_b_v0.6.3_bagging", "integer_vif_scale3"
        ]
    temporal_pooling_values = ["mean", "harmonic_mean", "geometric_mean", "total_variation","percentile_1","percentile_5","percentile_95","norm_lp1", "norm_lp2", "norm_lp3"]
    temporal_pooling_graph = ["mean", "harmonic_mean", "geometric_mean","percentile_1","percentile_5","percentile_95","norm_lp1", "norm_lp2", "norm_lp3"]

    lo_column_float_b = "vmaf_float_b_v0.6.3_ci_p95_lo"
    hi_column_float_b = "vmaf_float_b_v0.6.3_ci_p95_hi"
    lo_column_b = "vmaf_b_v0.6.3_ci_p95_lo"
    hi_column_b = "vmaf_b_v0.6.3_ci_p95_hi"
    stddev_column_float_b_v0_6_3 = "vmaf_float_b_v0.6.3_stddev"
    stddev_column_b_v0_6_3 = "vmaf_b_v0.6.3_stddev"

    if x_column not in data.columns:
        raise ValueError(f"Columns {x_column} not found in the csv for {dataset}.")
    # create the output path for every dataset
    output_path = f"{output_dir}/{dataset}/graph_results/"
    os.makedirs(output_path, exist_ok=True)
    # Graph 
    # - for all the PVS, a scatter plot with the VMAF model's mean as the central value and error bars based on the hi and lo values as the lower and upper limits: HILO.
    # - for all the PVS, a scatter plot with the VMAF model's mean with standard deviation as the central value and error bars based on the hi and lo values as the lower and upper limits: HILO.
    # - for all the pvs  a scatter plot with the VMAF model's mean as the central value and error bars based on the 5th and 95th percentiles as lower and upper limits : "Percentile5_95_vsVmafMean"
    # - for every features all the pvs : for every pvs  different points for the different temporal pooling  : "PVS dir"
    # - for every features all the pvs : for every pvs  different points for the different temporal pooling : "PVS dir"
    
    
    
    # where to save analysis    
    vmaf_output_path = os.path.join(output_path, "VMAF_Models")
    features_output_path = os.path.join(output_path, "Features")
    hi_lo_output_path = os.path.join(output_path,"HI_LO")
    pvs_path=os.path.join(output_path,"PVS")
    percentile_path = os.path.join(output_path,"Percentile5_95_vsVmafMean")
    os.makedirs(vmaf_output_path, exist_ok=True)
    os.makedirs(features_output_path, exist_ok=True)
    os.makedirs(hi_lo_output_path, exist_ok=True)
    os.makedirs(pvs_path, exist_ok=True)
    os.makedirs(percentile_path, exist_ok=True)

    # extract all the unique video_codescs,fps,duration,bitrate,vmaf_float_b.v0.6.3, vmaf_b_v0.6.3 values
    # video_codes graph are generated only if there is more than one video_codecs
    # fps graphs only if there is a minimun difference of 15 fps
    video_codecs = data['Video_codec'].unique()
    FPS_values = data['FPS'].unique()
    Duration_values = data['Duration'].unique()
    bitrate_values = data['Bitrate'].unique()
    vmaf_float_b_values = data['vmaf_float_b_v0.6.3'].unique()
    vmaf_b_values = data['vmaf_b_v0.6.3'].unique()
    # extract all the different pvs
    pvs=data['Distorted_file_name'].unique()
    # Create color palettes using Matplotlib colormap functions. Each palette contains a range of colors that are evenly distributed
    # across an interval from 0 to 1, where each value in the interval corresponds to a specific color in the palette.
    # The number of colors in each palette depends on the number of elements in the respective input list.
    colors_video_codec = plt.cm.tab10(np.linspace(0, 1, len(video_codecs)))
    colors_FPS = plt.cm.viridis(np.linspace(0, 1, len(FPS_values)))
    colors_Duration = plt.cm.plasma(np.linspace(0, 1, len(Duration_values)))
    colors_bitrate = plt.cm.cool(np.linspace(0, 1, len(bitrate_values)))
    colors_temporal_pooling=plt.cm.twilight(np.linspace(0,1,len(temporal_pooling_graph)))
    # Create dictionaries that map each element (e.g., codec, FPS, duration, bitrate, temporal pooling) to a specific color
    # based on its position in the respective list. Each color is selected from the previously generated color palettes.
    codec_color_map = {codec: colors_video_codec[i] for i, codec in enumerate(video_codecs)}
    FPS_color_map = {FPS: colors_FPS[i] for i, FPS in enumerate(FPS_values)}
    Duration_color_map = {Duration: colors_Duration[i] for i, Duration in enumerate(Duration_values)}
    bitrate_color_map = {bitrate: colors_bitrate[i] for i, bitrate in enumerate(bitrate_values)}
    temporal_pooling_color_map={temporal_pooling : colors_temporal_pooling[i] for i ,temporal_pooling in enumerate(temporal_pooling_graph)}
    
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
               
              if y_column in axis_limits:
                  plt.ylim(axis_limits[y_column]) 
              if x_column in axis_limits:
                  plt.xlim(axis_limits[x_column]) 
                   
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
                if y_column in axis_limits:
                  plt.ylim(axis_limits[y_column]) 
                if x_column in axis_limits:
                  plt.xlim(axis_limits[x_column]) 
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

        # float b model
       
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
            plt.xlabel("MOS")
            plt.ylabel("vmaf_float_b_v0.6.3")
            if "MOS" in axis_limits:
                plt.xlim(axis_limits["MOS"])
            if "vmaf_float_b_v0.6.3" in axis_limits:
                plt.ylim(axis_limits["vmaf_float_b_v0.6.3"])
            
            plt.grid(True)
            output_file = f"{hi_lo_output_path}/hilo_vmaf_float_b_v0.6.3_{temporal_pooling_value}.png"
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
            plt.xlabel("MOS")
            plt.ylabel("vmaf_float_b_v0.6.3")
            if "MOS" in axis_limits:
                plt.xlim(axis_limits["MOS"])
            if "vmaf_float_b_v0.6.3" in axis_limits:
                plt.ylim(axis_limits["vmaf_float_b_v0.6.3"])
            plt.grid(True)

            output_file = f"{hi_lo_output_path}/hilostddev_vmaf_float_b_v0.6.3_{temporal_pooling_value}_stddev.png"
            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()
        # b model
        
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
            plt.xlabel("MOS")
            plt.ylabel("vmaf_b_v0.6.3")
            if "MOS" in axis_limits:
                plt.xlim(axis_limits["MOS"])
            if "vmaf_b_v0.6.3" in axis_limits:
                plt.ylim(axis_limits["vmaf_b_v0.6.3"])
            plt.grid(True)

            output_file = f"{hi_lo_output_path}/hilo_vmaf_b_v0.6.3_{temporal_pooling_value}.png"
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
            plt.xlabel("MOS")
            plt.ylabel("vmaf_float_b_v0.6.3")
            if "MOS" in axis_limits:
                plt.xlim(axis_limits["MOS"])
            if "vmaf_b_v0.6.3" in axis_limits:
                plt.ylim(axis_limits["vmaf_b_v0.6.3"])
            plt.grid(True)

            output_file = f"{hi_lo_output_path}/hilostdev_vmaf_b_v0.6.3_{temporal_pooling_value}_stddev.png"
            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()

        # Bitrate 
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
            if y_column in axis_limits:
                  plt.ylim(axis_limits[y_column]) 
            if x_column in axis_limits:
                  plt.xlim(axis_limits[x_column]) 
            plt.legend(title='Bitrate (kbps)', bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True)

            if y_column in vmaf_models:
                output_file = f"{vmaf_output_path}/scatter_{y_column}_{temporal_pooling_value}_bitrate.png"
            else:
                output_file = f"{features_output_path}/scatter_{y_column}_{temporal_pooling_value}_bitrate.png"

            plt.savefig(output_file, bbox_inches='tight')
            print(f"Graph saved: {output_file}")
            plt.close()
    