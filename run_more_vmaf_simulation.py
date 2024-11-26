import subprocess

database1 = 'AVT-VQDB-UHD-1_2'
database2 = 'AVT-VQDB-UHD-1_3'

file_path1 = f'/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/commands_{database1}.txt'
file_path2 = f'/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/commands_{database2}.txt'

def run_commands_from_file(file_path):
    try:
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
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

run_commands_from_file(file_path1)
run_commands_from_file(file_path2)
