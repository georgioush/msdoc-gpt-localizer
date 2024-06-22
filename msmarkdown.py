class TokenizedMarkdown:
    def __init__(self):
        self.meta_info = None
        self.tokenized_sections = []

class MSMarkdown:
    def __init__(self, content):
        self.content = content
        self.translated_content = ""
        self.summarized_content = ""
        self.tokenized_content = TokenizedMarkdown()