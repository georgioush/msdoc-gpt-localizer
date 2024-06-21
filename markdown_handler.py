import os
from openpublishing_config_handler import OpenPublishingConfigHandler
from repository_manager import RepositoryManager
from toc_handler import TOCHandler
from .markdown import Markdown
from markdown_translator import translate
from markdown_summarizer import summarize

class MarkdownHandler:
    def __init__(self, markdown_path):
        self.markdown_path = markdown_path
        self.markdown = self.load_markdown()
        
    def load_markdown(self):
        with open(self.markdown_path, 'r', encoding='utf-8') as file:
            return Markdown(file.read())

    def translate_markdown(self):
        translate(self.markdown)
        return self

    def summarize_markdown(self):
        summarize(self.markdown)
        return self

if __name__ == "__main__":
    # Initialize the RepositoryManager to load the repository configuration
    repo_manager = RepositoryManager("repository_config.json")
    paths = repo_manager.get_repo_path()

    config_handler = OpenPublishingConfigHandler(paths)
    toc_handler = TOCHandler(config_handler)

    # Get Markdown file paths from TOC
    md_file_paths = toc_handler.get_md_files_paths()

    if md_file_paths:
        first_md_file_path = md_file_paths[0]
    else:
        raise FileNotFoundError("No markdown files found in TOC.")

    handler = MarkdownHandler(first_md_file_path)

    print("Original Content:")
    print(handler.markdown.content)

    handler.markdown.translate_markdown()
    print("Translated Content:")
    print(handler.markdown.translated_content)

    handler.markdown.summriize_markdown()
    print("Summarized Content:")
    print(handler.markdown.summarized_content)
    