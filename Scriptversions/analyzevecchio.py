import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import sys
from scipy.stats import gmean

if len(sys.argv) != 15:
    print("Error, format is : python3 analyze.py <dataset> <width> <height> <bitrate> <video_codec> <model_version> <output_directory> <original_video> <distorted_video> <width_old> <height_old> <fps> <duration> <mos_dir>")
    sys.exit(1)

dataset = sys.argv[1]        
width = int(sys.argv[2])     
height = int(sys.argv[3])    
bitrate = sys.argv[4]   
video_codec = sys.argv[5]   
model_version = sys.argv[6] 
output_directory = sys.argv[7] 
original_video = sys.argv[8]  
distorted_video = sys.argv[9]
width_old = sys.argv[10]
height_old = sys.argv[11]
fps = sys.argv[12]
duration = sys.argv[13]
mos_dir = sys.argv[14]

mos = -1
ci = -1
computed_mos = -1

temporal_pooling_count = 9

print(f"width_old: {width_old}, height_old: {height_old}")

temporal_pooling_values = ['mean', 'harmonic_mean', 'geometric_mean','percentile_1','percentile_5','percentile_95', 'norm_lp1', 'norm_lp2', 'norm_lp3']

vmaf_models = [
    "vmaf_v0.6.1", 
    "vmaf_v0.6.1neg", 
    "vmaf_float_v0.6.1", 
    "vmaf_float_v0.6.1neg", 
    "vmaf_float_b_v0.6.3", 
    "vmaf_b_v0.6.3", 
    "vmaf_float_4k_v0.6.1", 
    "vmaf_4k_v0.6.1", 
    "vmaf_4k_v0.6.1neg"
]

features = ["cambi",
    "float_ssim",
    "psnr_y",
    "psnr_cb",
    "psnr_cr",
    "float_ms_ssim",
    "ciede2000",
    "psnr_hvs_y",
    "psnr_hvs_cb",
    "psnr_hvs_cr",
    "psnr_hvs",
    "vmaf_float_b_v0.6.3_bagging",      
    "vmaf_float_b_v0.6.3_stddev",       
    "vmaf_float_b_v0.6.3_ci_p95_lo",    
    "vmaf_float_b_v0.6.3_ci_p95_hi",
    "vmaf_b_v0.6.3_bagging",      
    "vmaf_b_v0.6.3_stddev",       
    "vmaf_b_v0.6.3_ci_p95_lo",    
    "vmaf_b_v0.6.3_ci_p95_hi",
    "integer_vif_scale3"
    ]
mos_dataset = f"{mos_dir}/Scores{dataset}.json"
if not os.path.exists(mos_dataset):
    raise FileNotFoundError(f"Mos file '{mos_dataset}' was not found")
# read mos dataset fil
with open(mos_dataset) as f:
    data_mos = json.load(f)
#remove extension and take only the name
distorted_file_name_no_extension = distorted_video.rsplit(".", 1)[0]  
for score in data_mos["scores"]:
    # if the distorted file is found in the mos files
    if score["PVS"]["PVS_ID"] == distorted_file_name_no_extension:
        print(score["PVS"]["PVS_ID"])  
        #set mos
        mos = score["MOS"]
        # set ci
        if "CI" in score:
         ci = score["CI"]
        else:
         ci = -1
         #set computed mos
        if "Computed_MOS" in score:
         computed_mos = score["Computed_MOS"]
        else:
         computed_mos = -1
        break          
else:
    print("No mos found")

csv_filename = f'{output_directory}/{dataset}/combined_results_{dataset}.csv'

# if csv does not exits create with temporal_pooling_count entries
if not os.path.isfile(csv_filename):
    print("Csv does not exist")
    
    # rows to add
    new_rows = []
    for temporal_pooling_value in temporal_pooling_values:
        row = {
            "Dataset": dataset,
            "Original_file_name": original_video,
            "Distorted_file_name": distorted_video,
            "Width_original": width_old,
            "Height_original": height_old,
            "Width": width,
            "Height": height,
            "Bitrate": bitrate,
            "Video_codec": video_codec,
            "FPS": fps,
            "Duration": duration,
            "MOS": mos,
            "CI": ci,
            "Computed_Mos": computed_mos,
            "temporal_pooling": temporal_pooling_value
        }
        
       #add void columns for models and features
        for model in vmaf_models:
            row[model] = ""  
        
        for feature in features:
            row[feature] = ""  
        
        new_rows.append(row)
    
    # create a dataframe from the rows ( one row for temporal pooling) and convert to csv
    new_df = pd.DataFrame(new_rows)
    new_df.to_csv(csv_filename, mode='w', header=True, index=False)
    print("CSV created")
else:
    # If csv already exists , verify if distorted_video is present
    print("Csv already exists, check if distorted_video already exists : ")
    
    df_existing = pd.read_csv(csv_filename)
    
    if distorted_video not in df_existing['Distorted_file_name'].values:
        print(f"{distorted_video} not found in the csv, adds rows")
        #add new rows if it another distorted video
        new_rows = []
        for temporal_pooling_value in temporal_pooling_values:
            row = {
                "Dataset": dataset,
                "Original_file_name": original_video,
                "Distorted_file_name": distorted_video,
                "Width_original": width_old,
                "Height_original": height_old,
                "Width": width,
                "Height": height,
                "Bitrate": bitrate,
                "Video_codec": video_codec,
                "FPS": fps,
                "Duration": duration,
                "MOS": mos,
                "CI": ci,
                "Computed_Mos": computed_mos,
                "temporal_pooling": temporal_pooling_value
            }
            
            # Add void columns for models and features
            for model in vmaf_models:
                row[model] = ""  
                for feature in features:
                    row[feature] = ""  
            
            new_rows.append(row)
        
        # Add new rows to already existing dataframe
        new_df = pd.DataFrame(new_rows)
        df_existing = pd.concat([df_existing, new_df], ignore_index=True)
        
        # update csv with new dataframe
        df_existing.to_csv(csv_filename, mode='w', header=True, index=False)
        print("temporal_pooling_count rows added to csv.")
    else:
        print(f"{distorted_video} is already present in the csv")
#todo : remove lines here
if dataset in ["KUGVD", "GamingVideoSet1", "GamingVideoSet2"]:
    # Create the JSON path name
    if width_old != '1920' or height_old != '1080':
        json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}_resized_{width}x{height}.json'
    else:
        json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}.json'
elif dataset in ["AVT-VQDB-UHD-1_1", "AVT-VQDB-UHD-1_2", "AVT-VQDB-UHD-1_3"]:
    if original_video == "bigbuck_bunny_8bit.yuv":
        if width_old != '4000' or height_old != '2250':
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}_resized_{width}x{height}.json'
        else:
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}.json'
    else:
        if width_old != '3840' or height_old != '2160':
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}_resized_{width}x{height}.json'
        else:
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}.json'
else:
    if dataset in [ "ITS4S" , "AGH_NTIA_Dolby"]:
        if width_old != '1280' or height_old != '720':
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}_resized_{width}x{height}.json'
        else:
            json_filename = f'{output_directory}/{dataset}/vmaf_results/result__{dataset}__{original_video}__{width_old}x{height_old}__{bitrate}__{video_codec}__{model_version}.json'

# Print json filename
print(f"Json file path: {json_filename}")


try:
    with open(json_filename) as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: Json file  '{json_filename}' not found.")
    sys.exit(1)
    
# Read the JSON file
#with open(json_filename) as f:
#    data = json.load(f)

# Take data from the frames
frames_list = data["frames"]
frames_rows = []

for frame in frames_list:
    frame_num = frame["frameNum"]
    metrics = frame["metrics"]
    row = {"frameNum": frame_num}
    row.update(metrics)
    frames_rows.append(row)

# example of row in frames_rows : frame_number cambi ciede ecc
# Create a DataFrame for current file's metrics
dframes = pd.DataFrame(frames_rows)
#print(dframes)

def calculate_metrics(column_name):
    if column_name in dframes.columns:
        column_data = dframes[column_name]
        if np.any(np.isnan(column_data)):
            #return -1 for the column if there are null values
            print(f"NaN values found in {column_name}, returning -1 for all metrics.")
            return (-1, -1, -1, -1, -1, -1, -1,-1,-1)
        
        mean_value = np.mean(dframes[column_name])
        harmonic_mean_value = 1.0 / np.mean(1.0 / (dframes[column_name] + 1.0)) - 1.0
        geometric_mean_value = gmean(dframes[column_name])
        percentile_1 = np.percentile(dframes[column_name], 1)
        percentile_5 = np.percentile(dframes[column_name], 5)
        percentile_95 =np.percentile(dframes[column_name], 95)
        
        print(f"1st Percentile: {percentile_1}")
        print(f"5th Percentile: {percentile_5}")
        print(f"95th Percentile: {percentile_95}")

        
        # Print values
        print(f"{column_name} Mean: {mean_value}")
        print(f"Harmonic mean {column_name}: {harmonic_mean_value}")
        print(f"Geometric mean {column_name}: {geometric_mean_value}")
        #print(f"{column_name} Percentiles:")
        
        
        # Norms
        norm_lp_1 = np.power(np.mean(np.power(np.array(dframes[column_name]), 1)), 1.0 / 1)  
        print(f"Norm L_1 of {column_name} values is: {norm_lp_1}")

        norm_lp_2 = np.power(np.mean(np.power(np.array(dframes[column_name]), 2)), 1.0 / 2)  
        print(f"Norm L_2 of {column_name} values is: {norm_lp_2}")

        norm_lp_3 = np.power(np.mean(np.power(np.array(dframes[column_name]), 3)), 1.0 / 3)  
        print(f"Norm L_3 of {column_name} values is: {norm_lp_3}")

        return mean_value, harmonic_mean_value, geometric_mean_value, percentile_1,percentile_5,percentile_95, norm_lp_1, norm_lp_2, norm_lp_3
    else:
        print(f"Metric '{column_name}' not found in the DataFrame.")
        return (-1,-1,-1,-1,-1,-1,-1)

if model_version == "vmaf_v0.6.1.json":
    metrics_to_evaluate = [
        "vmaf",
        "cambi",
        "float_ssim",
        "psnr_y",
        "psnr_cb",
        "psnr_cr",
        "float_ms_ssim",
        "ciede2000",
        "psnr_hvs_y",
        "psnr_hvs_cb",
        "psnr_hvs_cr",
        "psnr_hvs",
        "integer_vif_scale3"
    ]
elif model_version in ["vmaf_b_v0.6.3.json", "vmaf_float_b_v0.6.3.json"]:
    metrics_to_evaluate = [
        "vmaf",
        "vmaf_bagging",
        "vmaf_stddev",
        "vmaf_ci_p95_lo",
        "vmaf_ci_p95_hi",
    ]
else:
    metrics_to_evaluate = ["vmaf"]

metrics_results = {}
for metric in metrics_to_evaluate:
    results = calculate_metrics(metric)
    if results:
        metrics_results[metric] = results

# example of metrics_results :
# metrics_results[ciede2000] = {mean,harmonic_mean,..} 
df_existing = pd.read_csv(csv_filename)

# The following code 
# has more cases for different model_versions
#   for metric, values in metrics_results.items():
#   - remove json extension to match the column name if the metric is vmaf,vmaf_bagging,vmaf_ci_p95_hi,vmaf_ci_p95_lo or vmaf_stddev
#   - calculate how many rows are already occupied in the column corresponding to the model or metric 
#   - start_row = rows_filled :  sets the starting row for inserting the new results. It uses the value of rows_filled to determine where the new data should begin.
#   - end_row = start_row + temporal_pooling_count : calculates the end_row by adding temporal_pooling_count to the start_row. 
#               This defines the range of rows where the new results will be inserted.
#   - df_existing.loc[start_row:end_row-1, metric] =[ mean,harmonic_mean,geometric_mean,percentile_1,percentile_5,percentile_95,norm_lp_1,norm_lp_2,norm_lp_3]
#    This inserts the new metric values (mean, harmonic_mean, etc.) into the specified rows of the df_existing DataFrame. 
#    The loc function is used to select the rows from start_row to end_row-1 (inclusive), and the column corresponding to model_version.
#    The new values are assigned to that range of rows.



if model_version == 'vmaf_v0.6.1.json':
    for metric, values in metrics_results.items():
     mean, harmonic_mean, geometric_mean, percentile_1,percentile_5,percentile_95, norm_lp_1, norm_lp_2, norm_lp_3 = values
     if metric == "vmaf":
            model_version=model_version.replace(".json","")
            rows_filled = df_existing[model_version].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_version] =[            
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
     else:
        rows_filled = df_existing[metric].notna().sum()
        start_row = rows_filled 
        end_row = start_row + temporal_pooling_count
        df_existing.loc[start_row:end_row-1, metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
elif model_version == "vmaf_b_v0.6.3.json":
     for metric, values in metrics_results.items():
         mean, harmonic_mean, geometric_mean, percentile_1,percentile_5,percentile_95, norm_lp_1, norm_lp_2, norm_lp_3 = values
         if metric == "vmaf":
            model_version=model_version.replace(".json","")
            rows_filled = df_existing[model_version].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_version] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]    
         if metric == "vmaf_bagging":
            model_version=model_version.replace(".json","")
            model_metric = f"{model_version}_bagging"
            rows_filled = df_existing[model_metric].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
         if metric == "vmaf_stddev":
            model_version=model_version.replace(".json","")
            model_metric = f"{model_version}_stddev"
            rows_filled = df_existing[model_metric].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]        
         if metric == "vmaf_ci_p95_hi":
             model_version=model_version.replace(".json","")
             model_metric = f"{model_version}_ci_p95_hi"
             rows_filled = df_existing[model_metric].notna().sum()
             start_row = rows_filled 
             end_row = start_row + temporal_pooling_count
             df_existing.loc[start_row:end_row-1, model_metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
         if metric == "vmaf_ci_p95_lo":
             model_version=model_version.replace(".json","")
             model_metric = f"{model_version}_ci_p95_lo"
             rows_filled = df_existing[model_metric].notna().sum()
             start_row = rows_filled 
             end_row = start_row + temporal_pooling_count
             df_existing.loc[start_row:end_row-1, model_metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]          
elif model_version == "vmaf_float_b_v0.6.3.json":
     for metric, values in metrics_results.items():
         mean, harmonic_mean, geometric_mean, percentile_1,percentile_5,percentile_95, norm_lp_1, norm_lp_2, norm_lp_3 = values
         if metric == "vmaf":
            model_version=model_version.replace(".json","")
            rows_filled = df_existing[model_version].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_version] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
         if metric == "vmaf_bagging":
            model_version=model_version.replace(".json","")
            model_metric = f"{model_version}_bagging"
            rows_filled = df_existing[model_metric].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_metric] =[            
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
         if metric == "vmaf_stddev":
            model_version=model_version.replace(".json","")
            model_metric = f"{model_version}_stddev"
            rows_filled = df_existing[model_metric].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]        
         if metric == "vmaf_ci_p95_hi":
            model_version=model_version.replace(".json","")
            model_metric = f"{model_version}_ci_p95_hi"
            rows_filled = df_existing[model_metric].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
         if metric == "vmaf_ci_p95_lo":
            model_version=model_version.replace(".json","")
            model_metric = f"{model_version}_ci_p95_lo"
            rows_filled = df_existing[model_metric].notna().sum()
            start_row = rows_filled 
            end_row = start_row + temporal_pooling_count
            df_existing.loc[start_row:end_row-1, model_metric] =[
                mean,
                harmonic_mean,
                geometric_mean,
                percentile_1,
                percentile_5,
                percentile_95,
                norm_lp_1,
                norm_lp_2,
                norm_lp_3,
            ]
else:
    if "vmaf" in metrics_results:
        mean, harmonic_mean, geometric_mean, percentile_1,percentile_5,percentile_95, norm_lp_1, norm_lp_2, norm_lp_3 = metrics_results["vmaf"]
        model_version=model_version.replace(".json","")
        rows_filled = df_existing[model_version].notna().sum()
        start_row = rows_filled 
        end_row = start_row + temporal_pooling_count
        df_existing.loc[start_row:end_row-1, model_version] =[
        mean,
        harmonic_mean,
        geometric_mean,
        percentile_1,
        percentile_5,
        percentile_95,
        norm_lp_1,
        norm_lp_2,
        norm_lp_3,
]
# Update the csv with the new dataframe
df_existing.to_csv(csv_filename, mode='w', header=True, index=False)

print(f"Column for {model_version} added")
