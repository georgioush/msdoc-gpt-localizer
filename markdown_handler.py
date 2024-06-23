from msmarkdown import MSMarkdown
from repository_info.repository_info_handler import RepositoryInfoHandler
from markdown_translator import translate
from markdown_summarizer import summarize

class MarkdownHandler:
    def __init__(self, markdown_path):
        self.markdown_path = markdown_path
        self.markdown = self.load_markdown()
        self.repository_info_handler = None

    def load_repository_info(self, repo_path):
        self.repository_info_handler = RepositoryInfoHandler(repo_path)

    def load_markdown(self):
        with open(self.markdown_path, 'r', encoding='utf-8') as file:
            return MSMarkdown(file.read())

    def translate_markdown(self):
        if self.repository_info_handler is None:
            raise ValueError("Repository information not loaded.")
        translate(self.markdown)

    def summarize_markdown(self):
        if self.repository_info_handler is None:
            raise ValueError("Repository information not loaded.")
        summarize(self.markdown)

