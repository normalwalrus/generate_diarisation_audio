import json 
import os
from os import listdir
from os.path import isfile, join
 
def read_json_file(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
        return data
    
    except:
        data = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                record = json.loads(line.strip())  # parse each line as a JSON object
                data.append(record)
            
        return data

def write_manifest(output_filepath, final_list):
    
    with open(output_filepath, "w", encoding="utf-8") as f:
        for entry in final_list:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            
            
def read_txt_from_file(txt_filepath):
    ''' Read contents of a txt file '''
    with open(txt_filepath, "r") as f:
        
        return f.read()
    
def get_all_files_in_directory(directory):
    ''' Get all files in a directory '''

    return [f for f in listdir(directory) if isfile(join(directory, f))]

def delete_file(filepath):
    '''
    delete a file given a filepath
    '''
    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(f"Deleted: {filepath}")
        else:
            print(f"File not found or not a file: {filepath}")
    except Exception as e:
        print(f"Error deleting file {filepath}: {e}")
        
    
    