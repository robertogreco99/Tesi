import subprocess

file_path = '/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/commands.txt'

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
