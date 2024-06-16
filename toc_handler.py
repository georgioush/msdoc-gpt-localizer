import os
import yaml
from openpublishing_config_handler import OpenPublishingConfigHandler

class TOCHandler:
    def __init__(self, config_handler: OpenPublishingConfigHandler):
        self.config_handler = config_handler
        self.toc_path = self.config_handler.get_toc_path()
        self.toc_data = self.load_toc()

    def load_toc(self):
        if os.path.exists(self.toc_path):
            with open(self.toc_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        else:
            raise FileNotFoundError(f"TOC file not found: {self.toc_path}")

    def get_all_name_href_pairs(self):
        """
        Get all name and href pairs from the TOC.
        
        :return: A list of tuples containing (name, href) pairs
        """
        def extract_pairs(items, pairs):
            for item in items:
                name = item.get('name')
                href = item.get('href')
                if name and href:
                    pairs.append((name, href))
                # Recursive call if there are nested items
                if 'items' in item:
                    extract_pairs(item['items'], pairs)

        pairs = []
        extract_pairs(self.toc_data, pairs)
        return pairs

if __name__ == "__main__":
    # Example usage
    repos_base_path = 'dev/repos'
    repository_config_path = 'dev/repository_config.json'
    config_handler = OpenPublishingConfigHandler(repos_base_path, repository_config_path)

    toc_handler = TOCHandler(config_handler)

    # Get all name-href pairs
    name_href_pairs = toc_handler.get_all_name_href_pairs()
    print("All name-href pairs:", name_href_pairs)