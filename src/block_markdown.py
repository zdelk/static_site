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

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"
        
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
        text = text_to_textnodes(content)
        
        children.append(ParentNode("li", text))
        
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return create_paragraph(block)
    if block_type == BlockType.HEADING:
        return create_heading(block)
    if block_type == BlockType.CODE:
        return create_code(block)
    if block_type == BlockType.QUOTE:
        return create_quote(block)
    if block_type == BlockType.ULIST:
        return create_ulist(block)
    if block_type == BlockType.OLIST:
        return create_olist(block)
    raise ValueError("Invalid Block Type")
# def markdown_to_html_node(markdown):
#     child = []
#     blocks = markdown_to_blocks(markdown)
#     for block in blocks:
        
#         btype = block_to_block_type(block)

#         match btype:
#             case BlockType.PARAGRAPH:
                
#                 children = text_to_children(block)
#                 node = ParentNode('p',children)
                
#             case BlockType.HEADING:
#                 tags, content = block.split(" ", 1)
#                 count = len(tags)
#                 children = text_to_children(content)
#                 node = ParentNode(f'h{count}', children)
            
#             case BlockType.CODE: # Parent would be <pre> child are <code>
#                 block = block.replace("```", "").lstrip("\n")
#                 text_node = TextNode(block, TextType.TEXT)
#                 html_node = text_node_to_html_node(text_node)
#                 code_node = ParentNode('code', [html_node])
#                 node = ParentNode('pre', [code_node])
                
#             case BlockType.QUOTE:
#                 children = text_to_children(block)
#                 node = ParentNode('blockquote', children)
                
#             case BlockType.ULIST: # Parent would be <ul> children are <li>
#                 list_nodes = make_list_nodes(block) # Need to create
#                 node = ParentNode('ul', list_nodes)
#             case BlockType.OLIST: # Parent would be <ol> children are <li>
#                 list_nodes = make_list_nodes(block) # Need to create
#                 node = ParentNode('ol', list_nodes)
#         child.append(node)
#     parent = ParentNode("div", child)

#     return parent

def create_paragraph(block):
    lines =  block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def create_heading(block):
    level = 0
    for char in block:
        if char == "#":
            level +=1
        else:
            break
    if level +1 > len(block):
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level+1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def create_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def create_olist(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def create_ulist(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)
    
def create_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)