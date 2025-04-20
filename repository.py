# import win32api
# import win32con
import re
# import ast

import json
import os.path
import shutil
from datetime import datetime

from commit import *
from file_handeling import *

class Repository:
    def __init__(self):
        self.commit_list = {}
        self.staging = []

    @staticmethod
    def wit_init(path):
        new_repo = Repository()
        wit_path = os.path.join(path, ".wit")
        try:
            create_new_directory(path, ".wit")
            create_new_directory(wit_path, "commits")
            create_new_file(os.path.join(wit_path,'commits'), "commits.json")
            create_new_file(wit_path, "staging.txt")
            # win32api.SetFileAttributes(wit_path, win32con.FILE_ATTRIBUTE_HIDDEN)
        except Exception as e:
            print("Reinitialized existing Wit repository in " + wit_path)

    def wit_add(self, path, file_name):
        file_path = os.path.join(path, file_name)
        #אם הקובץ נמצא בתוך תיקיות שבפרויקט ולא ישירות
        # נוסיף isExistFile(האם הקובץ בכלל קיים)

        with open(f"{os.path.join(path, '.wit/staging.txt')}","r", encoding='utf-8' ) as file:
            for line in file:
                line=line[:-2]
                if file_path.strip() == line.strip():
                    print("this file already added")
                    break
            else:
                self.staging.append(file_path)
                write_a_in_file(f"{os.path.join(path, '.wit/staging.txt')}", file_path)

    def wit_commit(self, path):
        if os.path.getsize(f"{os.path.join(path, '.wit/staging.txt')}") != 0 :
            author=input("insert author name! ")
            messege=input("insert messege! ")
            new_hash=str(hash(datetime.now()))
            new_commit = Commit(author,datetime.now(),messege)
            new_commit_path=f"{os.path.join(path,'.wit/commits',(str)(new_hash))}"

            # if the file: commits.json is empty - create the new folder
            if os.path.getsize(f"{os.path.join(path, '.wit/commits/commits.json')}") == 0 :
                create_new_directory(f"{os.path.join(path,'.wit/commits')}",(str)(new_hash))
            else:
                #read the file commits.json and convert it to dict
                with open(f"{os.path.join(path, '.wit/commits/commits.json')}", 'r')as file:
                    self.commit_list=json.load(file)
                last_hash=next(reversed(self.commit_list))
                last_commit_path=f"{os.path.join(path,'.wit/commits',(str)(last_hash))}"
                if os.path.exists(new_commit_path):#delete existing directory before coping
                    shutil.rmtree(new_commit_path)
                shutil.copytree(last_commit_path,new_commit_path)

            # change files that were in staging
            self.staging=(read_file(f"{os.path.join(path, '.wit/staging.txt')}")).split(",\n")
            self.staging.pop()
            replace_files(self.staging,path,new_commit_path)

            # update commit_list
            self.commit_list[new_hash] = str(new_commit)

            #המרת המילון לjson תקין
            with open(f"{os.path.join(path, '.wit/commits/commits.json')}", 'w') as file:
                json.dump(self.commit_list,file)

            # reset staging
            self.staging=[]
            write_w_in_file(f"{os.path.join(path, '.wit/staging.txt')}","")

    def wit_log(self, path):
        with open(f"{os.path.join(path, '.wit/commits/commits.json')}", 'r') as file:
            self.commits_list = json.load(file)
        for key, value in self.commits_list.items():
            # שימוש ב-regex כדי לחלץ את המידע
            match = re.match(r"Author: (\S+)\s*Date: ([\d\-:.\s]+)\s*Message: (.+)", value)
            if match:
                author = match.group(1)
                date = match.group(2)
                message = match.group(3)

                commit = Commit(author, date, message)

                print("\n" + key)
                print(commit)
            else:
                print(f"לא הצלחנו לחלץ את המידע מהמחרוזת: {value}")

    def wit_status(self,path):
        print("Changes to be committed:")
        self.staging = (read_file(f"{os.path.join(path, '.wit/staging.txt')}")).split(",\n")
        index=0
        while index<len(self.staging)-1:
            print("     "+os.path.relpath(self.staging[index],path))
            index+=1

    def wit_checkout(self, path, commit_id):
        #delete the content of project whithout .wit folder
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.path.isfile(file_path):  # אם מדובר בקובץ ולא בתיקיה
                delete_file_in_spesipic_path(file_path)
            elif os.path.isdir(file_path) and filename != ".wit":
                shutil.rmtree(file_path)
        #copy the content of selected commit
        shutil.copytree(f"{os.path.join(path, r".wit\commits", commit_id)}", path, dirs_exist_ok=True)


r = Repository()
# r.wit_init(r"C:\ריקי\תכנות\פייתון\wit example_2")
# r.wit_add(r"C:\ריקי\תכנות\פייתון\wit example_2", "my.txt")
# r.wit_add(r"C:\ריקי\תכנות\פייתון\wit example_2", "!!!Happy Chanucah!!!.docx")
# r.wit_commit(r"C:\ריקי\תכנות\פייתון\wit example_2")
r.wit_log(r"C:\ריקי\תכנות\פייתון\wit example_2")
# r.wit_status(r"C:\ריקי\תכנות\פייתון\wit example_2")
r.wit_checkout(r"C:\ריקי\תכנות\פייתון\wit example_2","-8682881253553902719")