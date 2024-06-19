import os
from openai import AzureOpenAI

class AOAIHandler:
    def __init__(self):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        
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

    def summarize_text(self, text):
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": "Summarize the following text:"},
                {"role": "user", "content": text},
            ],
        )
        
        if response.choices[0].message.content is not None:
            return response.choices[0].message.content.strip()
        else:
            raise ValueError("No summary content received")