import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        if delimiter not in node.text:
            raise Exception(f"Invalid Markdown syntax: {delimiter} not in any text node")
            
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if len(part) == 0:
                continue
            
            node_type = text_type if i % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(part, node_type))
            
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_by_markdown(old_nodes, extract_func, pattern, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        matches = extract_func(node.text)
        if not matches:
            new_nodes.append(node)
            continue
       
        parts = [x for x in re.split(pattern, node.text) if x]
        match_index = 0
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                text, url = matches[match_index]
                match_index += 1
                new_nodes.append(TextNode(text, text_type, url))
                
    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_by_markdown(
        old_nodes,
        extract_markdown_images,
        r'(!\[[^\[\]]+\]\([^()\s]+\))',
        TextType.IMAGE
    )

def split_nodes_link(old_nodes):
    return split_nodes_by_markdown(
        old_nodes,
        extract_markdown_links,
        r'((?<!!)\[[^\[\]]+\]\([^()\s]+\))',
        TextType.LINK
    )