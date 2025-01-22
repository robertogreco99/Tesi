import subprocess
import sys
import json
schema_file_path = 'Json/configschema.json'

if __name__ == '__main__':
    # Check for the correct number of arguments
    if len(sys.argv) != 2:
        print("The script needs two arguments. You need to call it like: python3 graph_simulations_run Json/config.json")
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
    dataset = config['DATASET']
    image_name = config["IMAGE_NAME"]
    #command=f"podman run --rm -it -v {output_dir}:/results  {image_name} python3 graph_script.py {dataset}"
    command=f" python3 graph_script_error.py {output_dir} {dataset}"

    
    if command:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error in the execution of command: {command}")
            print(e)

      