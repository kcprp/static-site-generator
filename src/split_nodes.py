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
            node_type = text_type if i % 2 == 1 else TextType.TEXT
            new_nodes.append(TextNode(part, node_type))
            
    return new_nodes