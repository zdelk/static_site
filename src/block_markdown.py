from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType

def markdown_to_blocks(markdown):
    block_list = []
    strings = markdown.split("\n\n")
    full_list = list(map(str.strip, strings))
    for item in full_list:
        if item:
            block_list.append(item)
    return block_list  

BlockType = Enum("BlockType", [
    "PARAGRAPH",
    "HEADING",
    "CODE",
    "QUOTE",
    "ULIST",
    "OLIST",
    ])
        
def block_to_block_type(block):
    heading_match = re.findall(r"^#{1,6}\s+.*$", block)
    if heading_match: # Regex #+" "
        return BlockType.HEADING
    
    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    lines = block.split("\n")
    quote_counter = 0
    unordered_counter = 0
    ordered_counter = 0
    i = 1
    for line in lines:
        if line == '':
            continue
        if line[0] == '>':
            quote_counter += 1
        if line[:2] == '- ':
            unordered_counter += 1
        if line[:3] == f"{i}. ":
            ordered_counter += 1
        i += 1
    if len(lines) == quote_counter:
        return BlockType.QUOTE
    if len(lines) == unordered_counter:
        return BlockType.ULIST
    if len(lines) == ordered_counter:
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        text_node.text = text_node.text.replace("\n"," ")
        children.append(text_node_to_html_node(text_node))
    return children
        
def make_list_nodes(text):
    children = []
    lines = text.split("\n")
    for line in lines:
        _, content = line.split(" ", 1)
        children.append(LeafNode("li", content))
        
    return children

def markdown_to_html_node(markdown):
    child = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        
        btype = block_to_block_type(block)

        match btype:
            case BlockType.PARAGRAPH:
                
                children = text_to_children(block)
                node = ParentNode('p',children)
                
            case BlockType.HEADING:
                tags, content = block.split(" ", 1)
                count = len(tags)
                children = text_to_children(content)
                node = ParentNode(f'h{count}', children)
            
            case BlockType.CODE: # Parent would be <pre> child are <code>
                block = block.replace("```", "").lstrip("\n")
                text_node = TextNode(block, TextType.TEXT)
                html_node = text_node_to_html_node(text_node)
                code_node = ParentNode('code', [html_node])
                node = ParentNode('pre', [code_node])
                
            case BlockType.QUOTE:
                children = text_to_children(block)
                node = ParentNode('blockquote', children)
                
            case BlockType.ULIST: # Parent would be <ul> children are <li>
                list_nodes = make_list_nodes(block) # Need to create
                node = ParentNode('ul', list_nodes)
            case BlockType.OLIST: # Parent would be <ol> children are <li>
                list_nodes = make_list_nodes(block) # Need to create
                node = ParentNode('ol', list_nodes)
        child.append(node)
    parent = ParentNode("div", child)

    return parent

# def create_paragraph(block):
    