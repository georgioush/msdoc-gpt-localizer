from abc import ABC, abstractmethod
from msmarkdown import MSMarkdown

class MarkdownTokenizer(ABC):
    def __init__(self, markdown: MSMarkdown):
        self.markdown = markdown

    @abstractmethod
    def tokenize(self):
        pass
