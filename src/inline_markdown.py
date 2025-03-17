import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception("Markdown Error: Missing matching delimiter")
            for i in range(len(split_text)):
                if split_text[i] == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
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
            
        matches = extract_markdown_links(node.text)
        
        if not matches:
            new_nodes.append(node)
            continue
        
        text, url = matches[0]
        
        sections = node.text.split(f"[{text}]({url})", 1)
        
        if sections[0]:
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
        
        new_nodes.append(TextNode(text, TextType.LINK, url))
        
        if sections[1]:
            remaining_nodes = split_nodes_link([TextNode(sections[1], TextType.TEXT)])
            new_nodes.extend(remaining_nodes)
            
    return new_nodes

def text_to_textnodes(text):
    old_node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes,"_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes,"`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    
    return link_nodes