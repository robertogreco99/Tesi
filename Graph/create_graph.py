import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

from csvgraph.graph import *

fn_csv = 'combined_results_KUGVD.csv'
fn_fields = 'input_fields.txt'
sep = ','
D1 = LOAD_WITH_EXTERNAL_FIELDS(fn_csv, fn_fields, sep)
print("Loaded data")

dirn = 'plots_v1'
plot = GPLOT(grid=True, enhanced=False, w=1200, h=800, option_str='set key left top\n')
sortvar = [('Original_file_name', 'asc')]

graph_data2 = SET_DOGRAPH_v2(
    ': -Distorted_file_name -Original_file_name +MOS',
    'MOS vmaf_v0.6.1 Video_codec [1:5] [0:100] "" "" p', plot)


n = EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=0, log_level=1, sortvar=sortvar)
print(f"Generated {n} graph(s)")
