
import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

from csvgraph.graph import *


fn_csv='combined_results_KUGVD.csv'
#namePVS,nameSRC,codec,rate,mos,vmaf,vmaf_bagging,vmaf_stddev,vmaf_ci_p95_lo,vmaf_ci_p95_hi
fn_fields='input_fields.txt'
sep=','
D1=LOAD_WITH_EXTERNAL_FIELDS(fn_csv, fn_fields, sep)

print("Loaded data")

print(D1.h)
#D1.pf_short()


dirn='plots_v1'
n=0

plot=GPLOT(grid=True, enhanced=False, w=1200, h=800, option_str='set key left top\n')
sortvar=[('nameSRC','asc')]
#plot.option_str = 'set ytics 0.1\n'  # Or any other option that precedes the "plot" command

graph_data2=SET_DOGRAPH_v2(
': -namePVS -nameSRC -rate +mos',
'mos vmaf codec  [1:5] [0:100] "" "" p', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -namePVS -nameSRC -rate +vmaf',
'vmaf vmaf_bagging codec [0:100] [0:100] "" "" p', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -namePVS -nameSRC -rate +vmaf',
'vmaf vmaf_stddev codec [0:100] [0:] "" "" p', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

##########################################################################################################################################
sys.exit()
##########################################################################################################################################

graph_data2=SET_DOGRAPH_v2(
': -namePVS ',
'rate vmaf codec [0:] [0:100] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -namePVS -rate +mos',
'mos vmaf nameSRC  [1:5] [0:100] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

#D2=D1.dup_all()
#D2=CSV('FILTER',D2,'$resH==540')

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate -bitRate +VQit_tv',
'VQit_tv VQuk  SRC  [0:5] [1:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate -bitRate +VMAF',
'VMAF VQit_tv  SRC  [0:100] [0:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate -bitRate +VMAF',
'VMAF PSNR  SRC  [0:100] [20:50] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary



##########################################################################################################################################
graph_data2=SET_DOGRAPH_v2(
': -V -frameRate -bitRate +VMAF',
'VMAF VQuk  SRC  [0:100] [1:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -frameRate -bitRate +VQit_tv',
'VQit_tv VQuk  SRC  [0:5] [1:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -frameRate -bitRate +VMAF',
'VMAF VQit_tv  SRC  [0:100] [0:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -frameRate -bitRate +VMAF',
'VMAF PSNR  SRC  [0:100] [20:50] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary



##########################################################################################################################################
graph_data2=SET_DOGRAPH_v2(
': -V   -SRC -frameRate -bitRate +VMAF',
'VMAF VQuk  category,H  [0:100] [1:5] "" "" p', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V   -SRC -frameRate -bitRate +VQit_tv',
'VQit_tv VQuk  category,H  [0:5] [1:5] "" "" p', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V   -SRC -frameRate -bitRate +VMAF',
'VMAF VQit_tv  category,H  [0:100] [0:5] "" "" p', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V   -SRC -frameRate -bitRate +VMAF',
'VMAF PSNR  category,H  [0:100] [20:50] "" "" p', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary






graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate +VMAF',
'VMAF VQuk  SRC  [0:100] [0:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate +VQit_tv',
'VQit_tv VQuk  SRC  [0:5] [0:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate +VMAF',
'VMAF VQit_tv  SRC  [0:100] [0:5] "" "" lp', plot)
n=EXEC_GRAPHS(D1, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary



##########################################################################################################################################
sys.exit()
##########################################################################################################################################


D2=CSV('FILTER',D2,'"JEG" in $SRC')

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate -bitRate +VMAF',
'VMAF VQuk  SRC  [0:] [:] "" "" lp', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate -bitRate +VQit_tv',
'VQit_tv VQuk  SRC  [0:] [:] "" "" lp', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate -bitRate +VMAF',
'VMAF VQit_tv  SRC  [0:] [:] "" "" lp', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -V -H -frameRate -bitRate +VMAF',
'VMAF PSNR  SRC  [0:] [:] "" "" lp', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary


##########################################################################################################################################
sys.exit()
##########################################################################################################################################



graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +MOS',
'MOS PSNR_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +MOS',
'MOS SSIM_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +MOS',
'MOS MSSSIM_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +MOS',
'MOS VIFP_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

###############################################################################################################################################

D2=D1.dup_all()
#D2=CSV('FILTER',D2,'$resH==540')
graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +SupersetMOS',
'SupersetMOS VQEG_PSNR hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +SupersetMOS',
'SupersetMOS PSNR_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +SupersetMOS',
'SupersetMOS SSIM_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +SupersetMOS',
'SupersetMOS MSSSIM_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary

graph_data2=SET_DOGRAPH_v2(
': -sequence -hrc +SupersetMOS',
'SupersetMOS VIFP_frame_histmatch_aligned hd,src [0:] [:] "" "" p', plot)
n=EXEC_GRAPHS(D2, graph_data2, dirname=dirn, graph_cnt=n, log_level=1, sortvar=sortvar) # Generate the output in the plots directory, created if necessary



sys.exit()
###############################################################################################################################################

