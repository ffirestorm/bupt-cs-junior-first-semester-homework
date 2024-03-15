import re

input_file_path = './urls.txt'  
output_file_path = './data/urls/urls.txt'  

with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
    for line in input_file:
        if 'hd' not in line:
            output_file.write(line)

