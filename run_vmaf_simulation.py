import subprocess

dataset = "KUGVD"
file_path = f"/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/{dataset}/commands_{dataset}.txt"

with open(file_path, 'r') as file:
    commands = file.readlines()

for command in commands:
    command = command.strip()  
    if command:  
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in the execution of command: {command}")
            print(e)
