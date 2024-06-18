import os
import yaml
import tiktoken
from openai import AzureOpenAI

class MarkdownTranslator:
    def __init__(self, api_key, azure_endpoint, deployment_name, api_version):
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint
        self.deployment_name = deployment_name
        self.api_version = api_version
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.azure_endpoint,
            api_version=self.api_version
        )

    def load_yaml(self, yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def extract_markdown_files(self, yaml_content):
        md_files = []
        if 'items' in yaml_content:
            for item in yaml_content['items']:
                if 'href' in item and item['href'].endswith('.md'):
                    md_files.append(item['href'])
                # Recursive call for nested items
                md_files.extend(self.extract_markdown_files(item))
        return md_files

    def token_count(self, text):
        encoding = tiktoken.encoding_for_model("davinci")
        return len(encoding.encode(text))

    def translate_header(self, text, header_level):
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": f"Translate the following {header_level} header:"},
                {"role": "user", "content": text},
            ],
        )
        
        if response.choices[0].message.content is not None:
            return response.choices[0].message.content.strip()
        else:
            raise ValueError("No translation content received")

    def translate_markdown(self, markdown_path):
        translated_lines = []
        with open(markdown_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith("#"):
                    header_level = line.count("#")
                    tokens = self.token_count(line)
                    if header_level == 1 or header_level == 2:
                        translated_line = self.translate_header(line, f"h{header_level}")
                        translated_lines.append(translated_line)
                    else:
                        translated_lines.append(line)
                else:
                    translated_lines.append(line)
        
        # Save translated content
        with open(markdown_path.replace('.md', '_translated.md'), 'w', encoding='utf-8') as file:
            file.write("\n".join(translated_lines))

    def run_translation(self, yaml_path):
        yaml_content = self.load_yaml(yaml_path)
        md_files = self.extract_markdown_files(yaml_content)
        
        for md_file in md_files:
            self.translate_markdown(md_file)

if __name__ == "__main__":
    # Environment variables for Azure OpenAI
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    translator = MarkdownTranslator(api_key, azure_endpoint, deployment_name, api_version)
    translator.run_translation("path/to/your/toc.yml")