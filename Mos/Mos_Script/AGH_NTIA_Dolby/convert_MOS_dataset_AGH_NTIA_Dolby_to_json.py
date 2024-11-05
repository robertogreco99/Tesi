import sys
import re
import json

#Files down; Subject right,0,1,2,3,4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,120,121,122,201,202,205,206,207,208,211,212,214,216,217,218,219,223,224,227,228,229
#AGH-NTIA-Dolby_AspenWalk_MPEG2at2M.avi,1,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1


def decode_line(line):
    v_line = line.split(',')
    #print(f"vline: {v_line}")
    # first element of the line
    PVS_params={}
    PVS_ID = v_line[0].strip().replace('.avi','')
    #print(f"PVS_ID: {PVS_ID}")
    PVS_params['SRC']=PVS_ID
    subject_right=v_line[1]
    print(v_line)
    total = 0
    MOS=0
    OS={}

    computed_MOS=0
    print(v_line)

    for i in range(2, len(v_line)):
        print(v_line[i]) 
        valuewhithoutnewline = v_line[i].strip()     

        if valuewhithoutnewline:  
                OS[i+1-2]=valuewhithoutnewline
                total += float(valuewhithoutnewline)
    computed_MOS = total / float(len(v_line)-2)

    return {'PVS': {'PVS_ID': PVS_ID} | PVS_params, 'Subject right': subject_right,'MOS': computed_MOS,'OS':OS,'Computed_MOS' : computed_MOS}

## __main__ ##

if len(sys.argv) <= 1:
    sys.stderr.write("ERROR: missing datafile.csv\n")
    sys.exit()

# dictionary
csv_information = {}
# void list: save each line of the file
file_line_information = []
# open the file
f = open(sys.argv[1], 'r')
# read first line of the file
header = f.readline()
# read second line of the file
line = f.readline()
while line:
    # work on the current line and save in the list file_line_information
    file_line_information.append(decode_line(line))
    line = f.readline()
f.close()

csv_information['dataset_name'] = 'AGH_NTIA_Dolby'
csv_information['SRC'] = list(set([x['PVS']['SRC'] for x in file_line_information]))
csv_information['scores'] = file_line_information

# Save to JSON file
json_file_path = "ScoresAGH_NTIA_Dolby.json"  
with open(json_file_path, 'w') as json_file:
    json.dump(csv_information, json_file, indent=4)

#print(f"Data has been written to {json_file_path}")
#print(json.dumps(csv_information, sort_keys=False, indent=4))
