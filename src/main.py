from copystatic import copy_files
from generate_page import generate_page

def main():
    source = "static"
    destination = "public"
    
    copy_files(source, destination)
    
    page_source = "content/index.md"
    template = "template.html"
    page_destination = "public/index.html"
    generate_page(page_source, template, page_destination)
    
if __name__ == "__main__":
    main()