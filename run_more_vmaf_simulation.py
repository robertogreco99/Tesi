import subprocess
import sys
import json
schema_file_path = 'Json/configschema.json'

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
        
if __name__ == '__main__':
    # Check for the correct number of arguments
    if len(sys.argv) != 2:
        print("The script needs two arguments. You need to call it like: python3 run_more_vmaf_simulation.py Json/config.json")
        sys.exit(1)
    
    # Get the config file from the command-line argument
    config_file = sys.argv[1]

    # Load the config file
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)

    # Load the schema file
    try:
        with open(schema_file_path) as schema_file:
            schema = json.load(schema_file)
    except FileNotFoundError:
        print(f"Error: Schema file '{schema_file_path}' not found.")
        sys.exit(1)

    output_dir = config['OUTPUT_DIR']
    database1 = 'AVT-VQDB-UHD-1_2'
    database2 = 'AVT-VQDB-UHD-1_3'

    file_path1 = f'{output_dir}/{database1}/commands_{database1}.txt'
    file_path2 = f'{output_dir}/{database2}/commands_{database2}.txt'
    run_commands_from_file(file_path1)
    run_commands_from_file(file_path2)
