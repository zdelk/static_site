from extract_header import extract_title
from block_markdown import markdown_to_html_node
import os

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    content = open(from_path).read()
    template = open(template_path).read()
    
    html_node = markdown_to_html_node(content)
    html_string = html_node.to_html()
    
    title = extract_title(content)
    
    output = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    path = os.path.dirname(dest_path)
    
    os.makedirs(path, exist_ok=True)
    
    with open(dest_path, 'w') as f:
        f.write(output)
    f.close()
    