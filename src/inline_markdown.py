import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = [] 
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Markdown Error: Missing matching delimiter")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern ,text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        matches = extract_markdown_images(node.text)
        
        if not matches:
            new_nodes.append(node)
            continue
        
        text, url = matches[0]
        
        sections = node.text.split(f"![{text}]({url})", 1)
        
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
        new_nodes.append(TextNode(text, TextType.IMAGE, url))
        
        if sections[1]:
            remaining_nodes = split_nodes_image([TextNode(sections[1], TextType.TEXT)])
            new_nodes.extend(remaining_nodes)
            
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        base_text = node.text 
        matches = extract_markdown_links(base_text)
        
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        for link in matches:
            sections = base_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            base_text = sections[1]
        if base_text != "":
            new_nodes.append(TextNode(base_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text):
    old_node = [TextNode(text, TextType.TEXT)]
    # bold_nodes = split_nodes_delimiter(old_node, "**", TextType.BOLD)
    # italic_nodes = split_nodes_delimiter(bold_nodes,"_", TextType.ITALIC)
    # code_nodes = split_nodes_delimiter(italic_nodes,"`", TextType.CODE)
    # image_nodes = split_nodes_image(code_nodes)
    # link_nodes = split_nodes_link(image_nodes)
    
    
    bold_nodes = split_nodes_delimiter(old_node, "**", TextType.BOLD)
    code_nodes = split_nodes_delimiter(bold_nodes,"`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    
    italic_nodes = split_nodes_delimiter(link_nodes,"_", TextType.ITALIC)
    
    
    
    
    return italic_nodes