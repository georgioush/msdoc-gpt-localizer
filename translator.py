import os
from openai import AzureOpenAI

class Translator:
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
        
    def translate_text(self, text):
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "Translate the following text:"},
                {"role": "user", "content": text},
            ],
        )
        
        if response.choices[0].message.content is not None:
            return response.choices[0].message.content.strip()
        else:
            raise ValueError("No translation content received")

if __name__ == "__main__":
    # 環境変数から設定を取得
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    translator = Translator(api_key, azure_endpoint, deployment_name, api_version)
    text = "Hello, how are you?"
    translated_text = translator.translate_text(text)
    print("Translated text:", translated_text)