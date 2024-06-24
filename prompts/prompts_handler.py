import json
from repository_info.repository_info_handler import RepositoryInfoHandler

class PromptHandler:
    def __init__(self, repository_handler: RepositoryInfoHandler = None):
        # Add any initialization code here
        try:
            with open('prompts/translation.json') as f:
                self.translation = json.load(f)
        except FileNotFoundError:
            raise Exception("Failed to open translation.json. Please make sure the file exists.")

        self.system_prompt = self.read_system_prompt()
        self.user_prompt = self.read_user_prompt()
        self.repository_info_handler = repository_handler

    def read_system_prompt(self):
        try:
            with open('prompts/translation_system.md', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise Exception("Failed to open translation_system.md. Please make sure the file exists.")

    def read_user_prompt(self):
        try:
            with open('prompts/translation_user.md', 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            raise Exception("Failed to open translation_user.md. Please make sure the file exists.")
        
    
    def generate_link_fix_prompt(self):

        link_fix_prompt = ""

        if self.repository_info_handler is None:
            raise ValueError("Repository handler is not initialized.")

        try:
            with open('prompts/link_fix.md', 'r', encoding='utf-8') as file:
                link_fix_prompt = file.read()
        except FileNotFoundError:
            raise Exception("Failed to open translation_user.md. Please make sure the file exists.")
        
        link_fix_prompt += self.repository_info_handler.breadcrumb_handler.get_weblink_path()
        link_fix_prompt += "\n\n"

        return link_fix_prompt
