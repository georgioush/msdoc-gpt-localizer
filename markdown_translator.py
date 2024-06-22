import re
from utils.aoai_handler import AOAIHandler
from utils.token_counter import TokenCounter
from msmarkdown import MSMarkdown

# Utility functions for different header levels
HEADER_PATTERNS = [
    (2, r'(?:^|\n)\s*(## .+?)(?=(?:\n\s*## |\Z))'),
    (3, r'(?:^|\n)\s*(### .+?)(?=(?:\n\s*### |\Z))'),
    (4, r'(?:^|\n)\s*(#### .+?)(?=(?:\n\s*#### |\Z))'),
    (5, r'(?:^|\n)\s*(##### .+?)(?=(?:\n\s*##### |\Z))'),
]

def split_large_section(section, token_counter, max_tokens):
    
    # section は markdown の一部なので、まずは行数を数える
    lines = section.split('\n')
    line_count = len(lines)

    # section のトークン数を max_tokens で割った商を求める なお、端数を切り上げた自然数にする
    section_num = -(-token_counter.count_tokens(section) // max_tokens)

    # line_count を section_num で割り、分割セクションの行数を決定する 念の為行数を 1 つ減らす
    split_line_count = line_count // section_num - 1 

    # 最初の行数から split_line_count ずつ取り出して、分割セクションを作成する
    tokenized_sections = []
    for i in range(section_num):
        start = i * split_line_count
        end = (i + 1) * split_line_count
        tokenized_sections.append("\n".join(lines[start:end]))

    return tokenized_sections

def tokenize_section(section, token_counter, max_tokens, level=0):

    if token_counter.count_tokens(section) <= max_tokens:
        return [section]

    if (level + 2) > len(HEADER_PATTERNS) + 1:
        # If we have reached the maximum header depth, split the section
        return split_large_section(section, token_counter, max_tokens)

    tokenized_sections = []
    pattern = HEADER_PATTERNS[level][1]
    sub_sections = re.split(pattern, section, flags=re.DOTALL)

    for sub_section in sub_sections:
        if sub_section.strip():
            print("Header Level:", f"{level + 2}", "Section Size:", f"{token_counter.count_tokens(sub_section)}")
            tokenized_sections.extend(tokenize_section(sub_section, token_counter, max_tokens, level + 1))

    return tokenized_sections

def tokenize_markdown(markdown: MSMarkdown, max_tokens: int):
    token_counter = TokenCounter()

    pattern = r'(?:^|\n)\s*(# .+?)(?=(?:\n\s*# |\Z))'
    sections = re.split(pattern, markdown.content, flags=re.DOTALL)
    
    if sections[0].startswith('---'):
        markdown.tokenized_content.meta_info = sections.pop(0)
    else:
        raise ValueError("No meta info found in markdown file.")
    
    for section in sections:
        if section.strip():
            print("Section Size:", f"{token_counter.count_tokens(section)}")

    for section in sections:
        if section.strip():
            markdown.tokenized_content.tokenized_sections.extend(tokenize_section(section, token_counter, max_tokens))

    return markdown

def translate(markdown: MSMarkdown):
    aoai_handler = AOAIHandler()

    for section in markdown.tokenized_content.tokenized_sections:
        
        response = aoai_handler.translate_text(section, "japanese")

        print("Translated Section:", response)
        markdown.translated_content += response + "\n"

if __name__ == "__main__":
    with open("repos/Edge/edgeenterprise/edge-ie-mode-cloud-site-list-mgmt.md", 'r', encoding='utf-8') as file:
        content = file.read()

    token_counter = TokenCounter()
    markdown_instance = MSMarkdown(content)
    tokenize_markdown(markdown_instance, 2048)

    print("Meta Info:")
    print(markdown_instance.tokenized_content.meta_info)
    
    print("Tokenized Sections:")
    print("Section Num:", len(markdown_instance.tokenized_content.tokenized_sections))

    for section in markdown_instance.tokenized_content.tokenized_sections:
        print("Tokens:", token_counter.count_tokens(section))

    print("Translation Started")
    translate(markdown_instance)

    with open("outrepos/Edge/edgeenterprise/edge-ie-mode-cloud-site-list-mgmt.md", 'w', encoding='utf-8') as file:
        file.write(markdown_instance.translated_content)
        print("Translation Finished")
