def markdown_to_blocks(markdown):
    blocks = []
    
    lines = markdown.split("\n\n")
    for line in lines:
        line = line.strip()

        if line == "":
            continue
        
        blocks.append(line)
        
    return blocks
        