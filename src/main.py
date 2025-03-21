import shutil
import os
from generator import generate_page
import sys

def copy_static(input, destination):
    if not os.path.exists(input):
        raise Exception("Input Folder Path Not valid")
    if os.path.exists(destination):
        shutil.rmtree(destination)
 
    os.mkdir(destination)
        
    item_list = os.listdir(input)
    
    for item in item_list:
        current_path = os.path.join(input, item)
        current_dest = os.path.join(destination, item)
        if os.path.isfile(current_path):
            shutil.copy(current_path, current_dest)
        else:
            copy_static(current_path, current_dest)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, BASE_PATH):
    item_list = os.listdir(dir_path_content)
    
    for item in item_list:
        current_path = os.path.join(dir_path_content, item)
        current_dest = os.path.join(dest_dir_path, item)
        if os.path.isfile(current_path):
            new_file = item[:-2] + "html"
            new_file_path = os.path.join(dest_dir_path, new_file)
            generate_page(current_path, template_path, new_file_path, BASE_PATH)
        else:
            generate_pages_recursively(current_path, template_path, current_dest, BASE_PATH)
    
dir_path_static = "static"
dir_path_docs = "docs"
dir_path_content = "content"
template_path = "template.html" 
    
def main():
    base_path = "/" if len(sys.argv) < 2 else sys.argv[1] 
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)
        
    copy_static(dir_path_static, dir_path_docs)
    generate_pages_recursively(
        dir_path_content, 
        template_path,
        dir_path_docs,
        base_path,
    )
    
main()
