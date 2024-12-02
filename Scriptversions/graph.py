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
    """