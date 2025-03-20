from textnode import TextNode, TextType
import shutil
import os

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
    
def main():
    node = TextNode("Hello There", TextType.LINK, "https://www.boot.dev")
    print(node)
    print(f"working directory: {os.getcwd()}")
    print(f"abs path: {os.path.abspath("static")}")
    copy_static("static", "public")

main()
