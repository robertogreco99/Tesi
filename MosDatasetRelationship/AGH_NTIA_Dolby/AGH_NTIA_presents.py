import json

input_file = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Mos/ScoresAGH_NTIA_Dolby.json'
output_file = './AllScoresAGH_NTIA_Dolby.txt'

with open(input_file, 'r') as f:
    data = json.load(f)

with open(output_file, 'w') as f:
    for entry in data.get('scores', []):
        if 'PVS' in entry and 'PVS_ID' in entry['PVS']:
            f.write(entry['PVS']['PVS_ID'] + '.y4m\n')

print(f"PVS_ID values have been extracted to {output_file}")