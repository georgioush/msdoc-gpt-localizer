from markdown_tokenizer import MarkdownTokenizer
from msmarkdown import MSMarkdown

class SummarizeTokenizer(MarkdownTokenizer):
    def tokenize(self, markdown: MSMarkdown):
        # 具体的な要約処理を実装
        return "Summary of the markdown text"
