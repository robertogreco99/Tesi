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
    "eSSIM":(0, 1),
    "SSIM":(0, 1),
}
temporal_pooling_marker_map = {
    'mean': '^',  
    'harmonic_mean': 's',  
    'geometric_mean': 'D',  
    'percentile_50': 'o',  
    'percentile_5': 'v',  
    'percentile_95': 'p',  
    'norm_lp1': '*',  
    'norm_lp2': 'h',  
    'norm_lp3': 'x',  
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
        "vmaf_b_v0.6.3_bagging", "integer_vif_scale3","eSSIM","SSIM"
        ]
    #temporal_pooling_values = ["mean", "harmonic_mean", "geometric_mean", "total_variation,"percentile_5","percentile_95","norm_lp1", "norm_lp2", "norm_lp3"]
    temporal_pooling_graph = ["mean", "harmonic_mean", "geometric_mean","percentile_50","percentile_5","percentile_95","norm_lp1", "norm_lp2", "norm_lp3"]

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

    hi_lo_output_path = os.path.join(output_path,"HI_LO")
    pvs_path=os.path.join(output_path,"PVS")
    percentile_path = os.path.join(output_path,"Percentile5_95_vsVmafMeanPercentile_50")
    
    os.makedirs(hi_lo_output_path, exist_ok=True)
    os.makedirs(pvs_path, exist_ok=True)
    os.makedirs(percentile_path, exist_ok=True)
    
    # extract all the different pvs
    pvs=data['Distorted_file_name'].unique()
    colors_temporal_pooling=plt.cm.twilight(np.linspace(0,1,len(temporal_pooling_graph)))
    # Create dictionaries that map each element (e.g., codec, FPS, duration, bitrate, temporal pooling) to a specific color
    # based on its position in the respective list. Each color is selected from the previously generated color palettes.
    temporal_pooling_color_map={temporal_pooling : colors_temporal_pooling[i] for i ,temporal_pooling in enumerate(temporal_pooling_graph)}

   
    
    for vmaf_model in vmaf_models:
        plt.figure(figsize=(10, 6))
        labels = []
        added_labels = set()
    
        for pvs_value in pvs:
            print(pvs_value)
            output_dir = f"{percentile_path}/error_bar/"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir) 
            
            filtered_data = data[data['Distorted_file_name'] == pvs_value]
            if filtered_data.empty:
                print(f"No data found for the pvs sequence: {pvs_value} in dataset {dataset}")
                continue
        
            x_value = filtered_data['MOS'].values[0]
        
            for temporal_pooling_value in ["mean", "percentile_50"]:
                temporal_filtered_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_value]
                temporal_pooling_lo = "percentile_5"
                percentile_5_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_lo]
                temporal_pooling_hi = "percentile_95"
                percentile_95_data = filtered_data[filtered_data['temporal_pooling'] == temporal_pooling_hi]
            
                if temporal_filtered_data.empty:
                    print(f"No data found for temporal pooling {temporal_pooling_value} in {pvs_value}")
                    continue
            
                y_value = temporal_filtered_data[vmaf_model].values
                if y_value == -1:
                    continue
            
                lo_value_percentile_5 = percentile_5_data[vmaf_model].values
                hi_value_percentile_95 = percentile_95_data[vmaf_model].values
                if(y_value- lo_value_percentile_5 <0):
                        print(x_value)
                        print(y_value)
                        print(lo_value_percentile_5)
                        print(hi_value_percentile_95)
                        print(pvs_value)
                marker = temporal_pooling_marker_map.get(temporal_pooling_value, 'o')  # o is the default marker
                if temporal_pooling_value == "mean":
                    color='blue'
                else:
                    color='red'
                    
                plt.errorbar(
                x_value, 
                y_value, 
                yerr=[y_value - lo_value_percentile_5, hi_value_percentile_95 - y_value], 
                marker=marker,
                color=color, 
                label=f"{temporal_pooling_value}" if temporal_pooling_value not in added_labels else ""
                )
                added_labels.add(temporal_pooling_value)

        plt.title(f"{x_column} vs {vmaf_model} with percentiles")
        plt.xlabel("MOS")
        plt.ylabel(vmaf_model)
        if "MOS" in axis_limits:
            plt.xlim(axis_limits["MOS"])
        if vmaf_model in axis_limits:
            plt.ylim(axis_limits[vmaf_model])
    
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title="Temporal Pooling", loc='center left', bbox_to_anchor=(1, 0.5))
    
        output_file = f"{percentile_path}/error_bar/combined_mean_median_{vmaf_model}.png"
        print(f"Graph saved: {output_file}")
        plt.savefig(output_file, bbox_inches='tight')
        plt.close()
    
