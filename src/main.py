from copystatic import copy_files
from generate_page import generate_pages_recursive
import sys

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    source = "static"
    destination = "docs"
    
    
    copy_files(source, destination)
    
    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "docs"
    
    generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path)
    
if __name__ == "__main__":
    main()