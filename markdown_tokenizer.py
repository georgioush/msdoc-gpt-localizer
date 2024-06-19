from markdown_handler import Markdown

class MarkdownTokenizer:
    def __init__(self, markdown: Markdown):
        self.markdown = markdown
        self.tokenized_content = None

    def tokenize(self):
        raise NotImplementedError("Subclasses should implement this method.")