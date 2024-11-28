import subprocess

dataset = "KUGVD"
# where to found the commands file
file_path = f"/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/{dataset}/commands_{dataset}.txt"

with open(file_path, 'r') as file:
    commands = file.readlines()
# run run_experiments for every command in the commands_{dataset}.txt file
for command in commands:
    command = command.strip()  
    if command:  
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in the execution of command: {command}")
            print(e)
