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

    def translate_text(self, text, target_language):
        # Implementation of the translation using Azure OpenAI service
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_language}:"},
                {"role": "user", "content": text},
            ],
        )
        
        if response.choices[0].message.content is not None:
            return response.choices[0].message.content.strip()
        else:
            raise ValueError("No translation content received")