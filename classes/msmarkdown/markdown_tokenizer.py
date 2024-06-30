from abc import ABC, abstractmethod
from classes.msmarkdown.msmarkdown import MSMarkdown

class MarkdownTokenizer(ABC):
    def __init__(self, markdown: MSMarkdown):
        self.markdown = markdown

    @abstractmethod
    def tokenize(self):
        pass
