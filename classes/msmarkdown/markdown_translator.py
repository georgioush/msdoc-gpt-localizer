import os
from utils.token_counter import TokenCounter
from utils.aoai_handler import AOAIHandler
from prompts.prompts_handler import PromptHandler
from classes.msmarkdown.markdown_handler import MarkdownHandler
from classes.msmarkdown.translate_tokenizer import TranslateTokenizer

class MarkdownTranslator(MarkdownHandler):
    def __init__(self, markdown_path: str):
        super().__init__(markdown_path)

    def translate(self):
        # Initialize the Azure OpenAI handler
        aoai_handler = AOAIHandler()
        token_counter = TokenCounter()
        prompts_handler = PromptHandler(self.repository_info_handler)

        tokenizer = TranslateTokenizer(self.markdown)
        tokenizer.tokenize()

        system_prompt = prompts_handler.system_prompt
        user_prompt = ""
        user_prompt += prompts_handler.generate_link_fix_prompt()
        user_prompt += prompts_handler.user_prompt

        print("Meta Info:")
        print(self.markdown.tokenized_content.meta_info)
        
        print("Tokenized Sections:")
        print("Section Num:", len(self.markdown.tokenized_content.tokenized_sections))

        for section in self.markdown.tokenized_content.tokenized_sections:
            print("Tokens:", token_counter.count_tokens(section))

        for section in self.markdown.tokenized_content.tokenized_sections:

            # print("user_prompt:", user_prompt + section)

            messages = [{"role":"system", "content": system_prompt},
                        {"role": "user", "content": user_prompt + section}]

            response = aoai_handler.execute(messages)
            # print("Translated Section:", response)
            if response is not None:
                self.markdown.translated_content += response + "\n"

        return self.markdown.translated_content

    def save_translation(self):

        if self.markdown.translated_content == "":
            raise Exception("No translation to save")

        markdown_path = self.markdown_path

        parts = markdown_path.split('\\')
        parts[0] = "outrepos"

        output_path = os.path.join(*parts)

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(self.markdown.translated_content)
            print("Translation saved to:", output_path)

if __name__ == "__main__":
    markdown_translator = MarkdownTranslator("repos/Edge/edgeenterprise/edge-ie-mode-cloud-site-list-mgmt.md")
    markdown_translator.translate()

    with open("outrepos/Edge/edgeenterprise/edge-ie-mode-cloud-site-list-mgmt.md", 'w', encoding='utf-8') as file:
        file.write(markdown_translator.markdown.translated_content)
        print("Translation Finished")
