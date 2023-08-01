import time
from concurrent.futures import ThreadPoolExecutor
import os

class Pool(ThreadPoolExecutor):
    def __init__(self, max_workers):
        ThreadPoolExecutor.__init__(self, max_workers)

        self.tasks = {'general': []}
        
        self.workers = max_workers


    def submit(self, fn, *args, group = "general", **kwargs):
        future = super().submit(fn, *args, **kwargs)
        if group not in self.tasks:
            self.tasks[group] = []
        self.tasks[group].append(future)

    def wait_group_done(self, group = "general"):
        queue = [i.done() for i in self.tasks[group]]
        
        while False in queue:
            time.sleep(0.2)
            queue = [i.done() for i in self.tasks[group]]

exe = Pool(max_workers=4)

## ------------ // ---------------

import requests
import os
import pandas as pd


save_folder = '/Users/gustavo/Documents/reductionmedia/MYFILES'

ip = input("Input server IP: ")

BASELINK = f'http://{ip}/media/'

def get_file(file_path):
    file_name = file_path.split('/')[-1]
    print(BASELINK + file_path)
    r = requests.get(BASELINK + file_path)

    if r.status_code == 200:
        f = open(os.path.join(save_folder, file_name), 'wb')
        f.write(r.content)
        f.close()
        print(f'downloaded {file_path}')
    else:
        print(f'error downloading {file_path}')

def main():
    df = pd.read_csv('files.csv')

    for key, value in df.iterrows():
        exe.submit(get_file, value['file_path'])

    exe.wait_group_done()

if __name__ == '__main__':
    main()
