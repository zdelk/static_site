from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes

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
    lines = text.split("\n")
    for line in lines:
        child = []
        if line == '':
            continue
        child.append(text_to_textnodes(line))
    children.append(child)
    return children
        
def markdown_to_html_node(markdown):
    parent = ParentNode("div")
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        btype = block_to_block_type(block)
        children = text_to_children(block)
        match btype:
            case BlockType.PARAGRAPH:
                node = HTMLNode('p',)
                
            case BlockType.HEADING:
                tags = block.split(" ", 1)
                count = len(tags) + 1
                node = HTMLNode(f'h{count}')
            
            case BlockType.CODE: # Parent would be <pre> child are <code>
                node = HTMLNode('code')
            case BlockType.QUOTE:
                node = HTMLNode('blockquote')
            case BlockType.ULIST: # Parent would be <ul> children are <li>
                node = HTMLNode('ul')
            case BlockType.OLIST: # Parent would be <ol> children are <li>
                node = HTMLNode('ol')
            
    
    return parent