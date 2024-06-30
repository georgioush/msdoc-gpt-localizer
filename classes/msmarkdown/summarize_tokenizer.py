from classes.msmarkdown.markdown_tokenizer import MarkdownTokenizer
from classes.msmarkdown.msmarkdown import MSMarkdown

class SummarizeTokenizer(MarkdownTokenizer):
    def tokenize(self, markdown: MSMarkdown):
        # 具体的な要約処理を実装
        return "Summary of the markdown text"
