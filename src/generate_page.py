import os
from markdown_blocks import (
    markdown_to_html_node,
    extract_title
)

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r', encoding='utf-8') as md_file:
        md = md_file.read()
    
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template = template_file.read()
    
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    dest_path = dest_path.replace('.md', '.html')
    with open(dest_path, 'w', encoding='utf-8') as dest_file:
        dest_file.write(template)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    entries = os.listdir(dir_path_content)
    
    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        
        if os.path.isfile(entry_path):
            generate_page(basepath, entry_path, template_path, dest_path)
        else:
            generate_pages_recursive(basepath, entry_path, template_path, dest_path)