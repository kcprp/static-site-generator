from copystatic import copy_files
from generate_page import generate_pages_recursive

def main():
    source = "static"
    destination = "public"
    
    copy_files(source, destination)
    
    dir_path_content = "content"
    template_path = "template.html"
    dest_dir_path = "public"
    
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)
    
if __name__ == "__main__":
    main()