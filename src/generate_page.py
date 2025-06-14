import os
from markdown_blocks import (
    markdown_to_html_node,
    extract_title
)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r', encoding='utf-8') as md_file:
        md = md_file.read()
    
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template = template_file.read()
    
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(template)
