import subprocess
dataset = "KUGVD"
command=f"podman run --rm -it -v /home/greco/home/docker/Result:/results  image python3 graph_script.py {dataset}"
if command:
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
            print(f"Error in the execution of command: {command}")
            print(e)
      