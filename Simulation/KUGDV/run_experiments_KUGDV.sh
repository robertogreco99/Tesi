#!/bin/bash

input_file="/home/greco/home/docker/Result/commands.txt"
input_file1=/home/roberto/Scaricati/Tesi/Lavorosullatesi/Tesi/Result/commands.txt
while IFS= read -r command; do
    if [[ -n "$command" ]]; then
        eval "$command"
    fi
done < "$input_file1"
