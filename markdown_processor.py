import os
import markdown
from bs4 import BeautifulSoup

class MarkdownProcessor:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        
    def get_markdown_files(self):
        markdown_files = []
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith('.md'):
                    markdown_files.append(os.path.join(root, file))
        return markdown_files
    
    def parse_markdown(self, file_path):
        with open(file_path, 'r') as f:
            text = f.read()
        html = markdown.markdown(text)
        soup = BeautifulSoup(html, "html.parser")
        return soup

if __name__ == "__main__":
    processor = MarkdownProcessor('./repos')
    md_files = processor.get_markdown_files()
    for md_file in md_files:
        soup = processor.parse_markdown(md_file)
        print(soup.prettify())