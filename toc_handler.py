import os
import yaml
from openpublishing_config_handler import OpenPublishingConfigHandler
from repository_manager import RepositoryManager

class TOCHandler:
    def __init__(self, config_handler: OpenPublishingConfigHandler):
        self.config_handler = config_handler
        self.toc_file_path = self.config_handler.get_toc_file_path()

    def load_toc(self):
        if not os.path.exists(self.toc_file_path):
            raise FileNotFoundError(f"TOC file not found: {self.toc_file_path}")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def get_name_href_pairs(self):
        toc_content = self.load_toc()
        return self.extract_name_href_pairs(toc_content)

    def extract_name_href_pairs(self, content):
        pairs = []
        if isinstance(content, list):
            for item in content:
                pairs.extend(self.extract_name_href_pairs(item))
        elif isinstance(content, dict):
            name = content.get('name', None)
            href = content.get('href', None)
            if name and href:
                pairs.append({'name': name, 'href': href})

            items = content.get('items', [])
            pairs.extend(self.extract_name_href_pairs(items))
        return pairs

    def get_md_files_paths(self):
        """
        Extracts href paths from the TOC and filters those that end with '.md' and exist as files.
        Returns the relative paths to these markdown files.
        """
        md_file_paths = []
        toc_content = self.load_toc()
        hrefs = self.extract_hrefs(toc_content)
        
        build_source_folder = self.config_handler.get_build_source_folder()

        for href in hrefs:
            if href.endswith('.md'):
                relative_path = os.path.join(
                    self.config_handler.repos_base_path[0], 
                    build_source_folder,
                    href
                )
                if os.path.exists(relative_path):
                    md_file_paths.append(relative_path)
                    
        return md_file_paths

    def extract_hrefs(self, content):
        hrefs = []
        if isinstance(content, list):
            for item in content:
                hrefs.extend(self.extract_hrefs(item))
        elif isinstance(content, dict):
            href = content.get('href', None)
            if href:
                hrefs.append(href)

            items = content.get('items', [])
            hrefs.extend(self.extract_hrefs(items))
        return hrefs

if __name__ == "__main__":
    # Initialize the RepositoryManager to load the repository configuration
    repo_manager = RepositoryManager("repository_config.json")
    paths = repo_manager.get_repo_path()

    config_handler = OpenPublishingConfigHandler(paths)
    toc_handler = TOCHandler(config_handler)

    name_href_pairs = toc_handler.get_name_href_pairs()
    for pair in name_href_pairs:
        print(pair)

    md_file_paths = toc_handler.get_md_files_paths()
    print("Markdown file paths:", md_file_paths)