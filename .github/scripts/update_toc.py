import os
import re
import yaml

def get_chapters():
    chapters = []
    for root, dirs, files in os.walk('chapters'):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r') as f:
                    content = f.read()
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    if title_match:
                        title = title_match.group(1)
                        chapters.append({
                            'file': os.path.join(root, file),
                            'title': title
                        })
    return sorted(chapters, key=lambda x: x['file'])

def update_toc():
    chapters = get_chapters()
    toc = "# Table of Contents\n\n"
    
    current_sector = ""
    for chapter in chapters:
        sector = chapter['file'].split('/')[1]
        if sector != current_sector:
            toc += f"\n## {sector.capitalize()} Sector\n"
            current_sector = sector
        
        relative_path = chapter['file'].replace('chapters/', '')
        toc += f"- [{chapter['title']}]({relative_path})\n"
    
    with open('README.md', 'r') as f:
        content = f.read()
    
    toc_pattern = r'(# Table of Contents\n)[\s\S]*?(?=\n#|$)'
    if re.search(toc_pattern, content):
        updated_content = re.sub(toc_pattern, toc, content)
    else:
        updated_content = content + "\n\n" + toc
    
    with open('README.md', 'w') as f:
        f.write(updated_content)

if __name__ == "__main__":
    update_toc()