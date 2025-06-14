import os
import shutil

def copy_files(source, destination):
    if not os.path.exists(source):
        raise Exception("Source path does not exist")
    
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)
    
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dst_path = os.path.join(destination, item)
        
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        else:
            shutil.copytree(src_path, dst_path)