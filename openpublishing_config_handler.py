import json
import os
from typing import List
from repository_manager import RepositoryManager

class OpenPublishingConfigHandler:
    def __init__(self, repos_path: str):
        self.repos_base_path = repos_path
        self.config = self.load_openpublishing_config()

    def load_openpublishing_config(self):
        config_path = os.path.join(self.repos_base_path[0], ".openpublishing.publish.config.json")
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def get_build_source_folder(self):
        try:
            return self.config["docsets_to_publish"][0]["build_source_folder"]
        except (IndexError, KeyError) as e:
            raise ValueError(f"Error getting build source folder: {e}")

    def get_toc_file_path(self):
        build_source_folder = self.get_build_source_folder()
        toc_path = os.path.join(self.repos_base_path[0], build_source_folder, "TOC.yml")
        if not os.path.exists(toc_path):
            raise FileNotFoundError(f"TOC file not found: {toc_path}")
        return toc_path

if __name__ == "__main__":
    # Initialize the RepositoryManager to load the repository configuration
    repo_manager = RepositoryManager("repository_config.json")
    paths = repo_manager.get_repo_path()

    config_handler = OpenPublishingConfigHandler(paths)
    print("Build source folder:", config_handler.get_build_source_folder())
    print("TOC file path:", config_handler.get_toc_file_path())