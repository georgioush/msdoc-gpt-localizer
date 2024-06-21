import os
from utils.aoai_handler import AOAIHandler
from utils.token_counter import TokenCounter
from .markdown import Markdown

def tokenize_markdown(markdown: Markdown, max_tokens: int):
    # Here we will implement the logic to split markdown.content into sections,
    # each having a maximum of 'max_tokens' tokens. For simplicity, let's assume
    # paragraphs are separated by double newline characters.
    
    # Tokenizer initialization
    token_counter = TokenCounter()
    
    paragraphs = markdown.content.split('\n\n')
    tokenized_sections = []
    current_section = ""
    current_token_count = 0
    
    for paragraph in paragraphs:
        paragraph_token_count = token_counter.count_tokens(paragraph)
        
        if current_token_count + paragraph_token_count > max_tokens:
            tokenized_sections.append(current_section.strip())
            current_section = paragraph
            current_token_count = paragraph_token_count
        else:
            current_section += '\n\n' + paragraph
            current_token_count += paragraph_token_count
    
    if current_section:
        tokenized_sections.append(current_section.strip())
    
    # Returning meta_info which might be located in markdown.meta_info
    # For this example, we'll keep it simple and return None
    meta_info = None
    
    return meta_info, tokenized_sections

def translate(markdown: Markdown):
    # Initialize the Azure OpenAI handler
    aoai_handler = AOAIHandler()
    # Initialize the TokenCounter
    token_counter = TokenCounter()
    
    # Define a maximum token limit (this would be based on Azure OpenAI's max tokens per request)
    max_tokens = 4096

    # Tokenize the markdown content
    meta_info, tokenized_sections = tokenize_markdown(markdown, max_tokens)
    
    translated_sections = []
    
    for section in tokenized_sections:
        translated_text = aoai_handler.translate_text(section, target_language="ja")  # Example: translating to Japanese
        translated_sections.append(translated_text)
    
    # Combine the translated sections into the full translated content
    markdown.translated_content = "\n\n".join(translated_sections)
    markdown.tokenized_content.meta_info = meta_info
    markdown.tokenized_content.tokenized_sections = tokenized_sections
    
    return markdown

# Example usage:
if __name__ == "__main__":

    # open a file in "repos/Edge/edgeenterprise/configure-edge-with-intune.md"
    with open("repos/Edge/edgeenterprise/configure-edge-with-intune.md", 'r', encoding='utf-8') as file:
        content = file.read()

    markdown_instance = Markdown()
    markdown_instance.content = content

    translated_markdown_instance = translate(markdown_instance)
    
    print("Translated Content:")
    print(translated_markdown_instance.translated_content)