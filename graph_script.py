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
    #temporal_pooling_values = ["mean", "harmonic_mean", "geometric_mean", "total_variation","percentile_1","percentile_5","percentile_95","norm_lp1", "norm_lp2", "norm_lp3"]
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
    # - for all the pvs a graph for the vmaf_float_b_v0.6.3 and vmaf_b_v0.6.3  with hilo and stdev: for every pvs different points for the different temporal pooling  : "HILO dir"
    # - for every features all the pvs : for every pvs  different points for the different temporal pooling  : "PVS dir"
    # - for every features all the pvs : for every pvs  different points for the different temporal pooling : "PVS dir"
    
    
    
    # where to save analysis    
    #vmaf_output_path = os.path.join(output_path, "VMAF_Models")
    #features_output_path = os.path.join(output_path, "Features")
    hi_lo_output_path = os.path.join(output_path,"HI_LO")
    pvs_path=os.path.join(output_path,"PVS")
    #os.makedirs(vmaf_output_path, exist_ok=True)
    #os.makedirs(features_output_path, exist_ok=True)
    os.makedirs(hi_lo_output_path, exist_ok=True)
    os.makedirs(pvs_path, exist_ok=True)

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


    for feature in features:
     plt.figure(figsize=(10, 6))
     # Initialize lists for labels and colors, and a set to avoid duplicate labels
     labels = []
     colors = []
     added_labels = set()
     for pvs_value in pvs:
         output_dir = f"{pvs_path}/all_features/"
         if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Filter the data for the current pvs_value
         filtered_data = data[data['Distorted_file_name'] == pvs_value]
         if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
         # Extract the MOS value
         x_value = filtered_data['MOS'].values[0]
         for temporal_pooling_value in temporal_pooling_graph:
             # Filter the data for the current temporal_pooling value
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue
            # Extract the feature value for the temporal filtered data
            feature_value = temporal_filtered_data[feature].values
            if feature_value == -1:
                continue
            # Get the color associated with the temporal_pooling value
            color = temporal_pooling_color_map[temporal_pooling_value]
            # Create a scatter plot with the x_value and feature_value, using the corresponding color
            plt.scatter(x_value, feature_value, color=color, marker='o', alpha=0.7)
            if temporal_pooling_value not in added_labels:
               labels.append(f"{temporal_pooling_value}")
               added_labels.add(temporal_pooling_value)
     
     
     plt.title(f"{x_column} vs {feature}")
     plt.xlabel(x_column)
     plt.ylabel(feature)
     # Set axis limits
     if "MOS" in axis_limits:
         plt.xlim(axis_limits["MOS"])  
     if feature in axis_limits:
         plt.ylim(axis_limits[feature])  
     plt.grid(True)
     plt.xticks(rotation=45)
     # display the legend
     plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))

     output_file = f"{pvs_path}/all_features/scatter_{feature}.png"
     plt.savefig(output_file, bbox_inches='tight')
     print(f"Graph saved: {output_file}")
     plt.close()
    for vmaf_model in vmaf_models:
        plt.figure(figsize=(10, 6))
        labels = []
        colors = []
        added_labels = set()
        for pvs_value in pvs:
            output_dir = f"{pvs_path}/all_vmaf_models/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            filtered_data = data[data['Distorted_file_name'] == pvs_value]
            if filtered_data.empty:
                print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
                continue
            x_value = filtered_data['MOS'].values[0]
            for temporal_pooling_value in temporal_pooling_graph:
                temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
                if temporal_filtered_data.empty:
                    print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                    continue
                model_value = temporal_filtered_data[vmaf_model].values
                if model_value == -1:
                    continue
                color = temporal_pooling_color_map[temporal_pooling_value]
                plt.scatter(x_value, model_value, color=color, marker='o', alpha=0.7)
                if temporal_pooling_value not in added_labels:
                    labels.append(f"{temporal_pooling_value}")
                    added_labels.add(temporal_pooling_value)

        plt.title(f"{x_column} vs {vmaf_model}")
        plt.xlabel(x_column)
        plt.ylabel(vmaf_model)
        if "MOS" in axis_limits:
         plt.xlim(axis_limits["MOS"])  
        if vmaf_model in axis_limits:
         plt.ylim(axis_limits[vmaf_model]) 
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))

        output_file = f"{pvs_path}/all_vmaf_models/scatter_{vmaf_model}.png"
        plt.savefig(output_file, bbox_inches='tight')
        print(f"Graph saved: {output_file}")
        plt.close()
    
    # float b model

    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/float_b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]
        for temporal_pooling_value in temporal_pooling_graph:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue
            y_value = temporal_filtered_data["vmaf_float_b_v0.6.3"].values 
            if  y_value == -1:
                continue
            color = temporal_pooling_color_map[temporal_pooling_value]
            lo_value = temporal_filtered_data["vmaf_float_b_v0.6.3_ci_p95_lo"].values 
            hi_value = temporal_filtered_data["vmaf_float_b_v0.6.3_ci_p95_hi"].values 
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value,hi_value-y_value], color=color,fmt='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f"{x_column} vs vmaf_float_b_v0.6.3")
        plt.xlabel("MOS")
        plt.ylabel("vmaf_float_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_float_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_float_b_v0.6.3"])
            
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))   
    output_file = f"{hi_lo_output_path}/float_b_model/hilo_vmaf_float_b_v0.6.3.png"
    print(f"Graph saved: {output_file}")  
    plt.savefig(output_file, bbox_inches='tight') 
    plt.close()
    
     # float b model stdev
    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/float_b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]  
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]   
        for temporal_pooling_value in temporal_pooling_graph:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue 
            y_value = temporal_filtered_data["vmaf_float_b_v0.6.3"].values    
            if  y_value == -1:
                continue
            color = temporal_pooling_color_map[temporal_pooling_value]
            stddev_float_b_value = temporal_filtered_data["vmaf_float_b_v0.6.3_stddev"].values
            lo_value_float_stddev= y_value - stddev_float_b_value
            hi_value_float_stdev = y_value + stddev_float_b_value
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value_float_stddev,hi_value_float_stdev-y_value],color=color, fmt='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f"{x_column} vs vmaf_float_b_v0.6.3 with stddev")
        plt.xlabel("MOS")
        plt.ylabel("vmaf_float_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_float_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_float_b_v0.6.3"])
       
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))  
    output_file = f"{hi_lo_output_path}/float_b_model/hilostddev_vmaf_float_b_v0.6.3_stddev.png"
    print(f"Graph saved: {output_file}")
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()

     # b model

    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]
        for temporal_pooling_value in temporal_pooling_graph:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue
            y_value = temporal_filtered_data["vmaf_b_v0.6.3"].values  
            if  y_value == -1:
                continue
            color = temporal_pooling_color_map[temporal_pooling_value]
            lo_value = temporal_filtered_data["vmaf_b_v0.6.3_ci_p95_lo"].values 
            hi_value = temporal_filtered_data["vmaf_b_v0.6.3_ci_p95_hi"].values 
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value,hi_value-y_value], color=color,fmt='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f"{x_column} vs vmaf_b_v0.6.3")
        plt.xlabel("MOS")
        plt.ylabel("vmaf_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_b_v0.6.3"])
            
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))   
    output_file = f"{hi_lo_output_path}/b_model/hilo_vmaf_b_v0.6.3.png"
    print(f"Graph saved: {output_file}")  
    plt.savefig(output_file, bbox_inches='tight') 
    plt.close()
    
    # b model stdev
    plt.figure(figsize=(10, 6))
    labels = []
    colors = []
    added_labels = set()
    for pvs_value in pvs : 
        output_dir = f"{hi_lo_output_path}/b_model/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir) 
        filtered_data = data[data['Distorted_file_name'] == pvs_value]  
        if filtered_data.empty:
            print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
            continue
        x_value = filtered_data['MOS'].values[0]   
        for temporal_pooling_value in temporal_pooling_graph:
            temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
            if temporal_filtered_data.empty:
                print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                continue 
            y_value= temporal_filtered_data["vmaf_b_v0.6.3"].values    
            if  y_value == -1:
                continue
            color = temporal_pooling_color_map[temporal_pooling_value]
            stddev_b_value = temporal_filtered_data["vmaf_b_v0.6.3_stddev"].values
            lo_value_b_stddev= y_value - stddev_b_value
            hi_value_b_stdev = y_value + stddev_b_value
            plt.errorbar(x_value, y_value, yerr=[y_value-lo_value_b_stddev,hi_value_b_stdev-y_value],color=color, fmt='o')
            if temporal_pooling_value not in added_labels:
                labels.append(f"{temporal_pooling_value}")
                added_labels.add(temporal_pooling_value)
        plt.title(f"{x_column} vs vmaf_b_v0.6.3 with stddev")
        plt.xlabel("MOS")
        plt.ylabel("vmaf_b_v0.6.3")
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if "vmaf_b_v0.6.3" in axis_limits:
            plt.ylim(axis_limits["vmaf_b_v0.6.3"])
       
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", labels=labels, loc='center left', bbox_to_anchor=(1, 0.5))  
    output_file = f"{hi_lo_output_path}/b_model/hilostddev_vmaf_b_v0.6.3_stddev.png"
    print(f"Graph saved: {output_file}")
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()