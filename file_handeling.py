import json
import os
import shutil


def create_new_directory(path, directory_Name):
    try:
        if not os.path.exists(os.path.join(path, directory_Name)):
            os.mkdir(os.path.join(path, directory_Name))
        else:
            raise Exception("this directory already exist")
    except Exception as e:
        return "Error: " + e

def create_new_file(path, file_Name):
    try:
        open(os.path.join(path, file_Name), 'x')
    except FileExistsError:
        pass

def write_a_in_file(path, text):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(text+",\n")

def write_w_in_file(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)

def delete_file_in_spesipic_path(path):
    os.remove(path)

def directory_content(path):
    for  dirnames, filenames in os.walk(path):
        print('path: ', dirpath)
        print('directories: ', dirnames)
        print('files: ', filenames)
        print()

def display_current_path_of_directory():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path)

def read_file(path):
    with open(path,'r',encoding='utf-8') as file:
        return file.read()

def read_json_file(path):
    with open(path,'r',encoding='utf-8') as jyson_file:
        return json.load(jyson_file)

def replace_files(file_pathes,src_dir,dest_dir):
    for src_f in file_pathes:
        relative_path=os.path.relpath(src_f,src_dir)
        # print(f"dest dir:   {dest_dir}      \n relative_path:    {relative_path}\n")
        dest_f=os.path.join(dest_dir,relative_path)
        # print(f"coping from:   {src_f}      to:   {dest_f}")
        shutil.copy2(src_f,dest_f)
        # print("success")
