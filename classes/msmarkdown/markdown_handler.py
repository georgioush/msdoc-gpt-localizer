import os
from classes.msmarkdown.msmarkdown import MSMarkdown
from classes.repository_info.repository_info_handler import RepositoryInfoHandler


class MarkdownHandler:
    def __init__(self, markdown_path):
        self.markdown_path = os.path.normpath(markdown_path)
        self.markdown = self.load_markdown()
        self.repository_info_handler = self.load_repository_info_handler()

    def load_repository_info_handler(self, handler: RepositoryInfoHandler = None):
        if handler is not None:
            return handler
        else:
            normalized_path = os.path.normpath(self.markdown_path)
            parts = normalized_path.split('\\')
            top_two_dirs = os.path.join(parts[0], parts[1])
            return RepositoryInfoHandler(top_two_dirs)

    def load_markdown(self):
        with open(self.markdown_path, 'r', encoding='utf-8') as file:
            return MSMarkdown(file.read())
        

        