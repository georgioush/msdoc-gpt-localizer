import os
from utils.aoai_handler import AOAIHandler  # 'dev'を削除してパスを修正
from markdown_translator import MarkdownTranslator  # 'dev'を削除してパスを修正
from markdown_summarizer import MarkdownSummarizer  # 'dev'を削除してパスを修正
from toc_handler import TOCHandler
from openpublishing_config_handler import OpenPublishingConfigHandler
from repository_manager import RepositoryManager

class Markdown:
    def __init__(self, content):
        self.content = content
        self.translated_content = None
        self.summary_content = None
        self.tokenized_sections = []  # トークナイズされた内容を保持

class MarkdownHandler:
    def __init__(self, markdown_path):
        self.markdown_path = markdown_path
        self.markdown = self.load_markdown()
        
    def load_markdown(self):
        with open(self.markdown_path, 'r', encoding='utf-8') as file:
            return Markdown(file.read())

    def save_markdown(self, markdown, output_path):
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(markdown.content)

    def translate_markdown(self):
        translator = MarkdownTranslator(self.markdown)
        translator.translate()

    def summarize_markdown(self):
        summarizer = MarkdownSummarizer(self.markdown)
        summarizer.summarize()

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

    # マークダウンファイルの翻訳と保存
    handler.translate_markdown()
    translated_output_path = first_md_file_path.replace('.md', '_translated.md')
    handler.save_markdown(Markdown(handler.markdown.translated_content), translated_output_path)

    # マークダウンファイルのサマリーと保存
    handler.summarize_markdown()
    summary_output_path = first_md_file_path.replace('.md', '_summary.md')
    handler.save_markdown(Markdown(handler.markdown.summary_content), summary_output_path)