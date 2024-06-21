class TokenizedMarkdown:
    def __init__(self):
        self.meta_info = None
        self.tokenized_sections = []

class Markdown:
    def __init__(self, content):
        self.content = content
        self.translated_content = None
        self.summarized_content = None
        self.tokenized_content = TokenizedMarkdown()