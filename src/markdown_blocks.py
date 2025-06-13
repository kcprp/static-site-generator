from enum import Enum
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    lines = markdown.split("\n\n")
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        blocks.append(line)
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def convert_paragraph_to_html(block):
    paragraph = block.replace("\n", " ")
    text_children = text_to_children(paragraph)
    return ParentNode("p", text_children)

def convert_heading_to_html(block):
    level = block.count("#")
    if level > 6:
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:].strip()
    text_children = text_to_children(text)
    return ParentNode(f"h{level}", text_children)

def convert_code_to_html(block):
    code_content = block.replace("```", "").lstrip()
    return ParentNode("pre", [LeafNode("code", code_content)])

def convert_quote_to_html(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    text_children = text_to_children(content)
    return ParentNode("blockquote", text_children)

def convert_unordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        text_children = text_to_children(text)
        html_items.append(ParentNode("li", text_children))
    return ParentNode("ul", html_items)

def convert_ordered_list_to_html(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        text_children = text_to_children(text)
        html_items.append(ParentNode("li", text_children))
    return ParentNode("ol", html_items)

def convert_block_to_html(block):
    block_type = block_to_block_type(block)
    
    converters = {
        BlockType.PARAGRAPH: convert_paragraph_to_html,
        BlockType.HEADING: convert_heading_to_html,
        BlockType.CODE: convert_code_to_html,
        BlockType.QUOTE: convert_quote_to_html,
        BlockType.ULIST: convert_unordered_list_to_html,
        BlockType.OLIST: convert_ordered_list_to_html
    }
    
    converter = converters.get(block_type)
    if not converter:
        raise ValueError(f"Unknown block type: {block_type}")
    
    return converter(block)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_children = [convert_block_to_html(block) for block in blocks]
    return ParentNode(tag="div", children=html_children)