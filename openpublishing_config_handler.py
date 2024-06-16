import json
import os
from typing import List

class OpenPublishingConfigHandler:
    def __init__(self, repos_base_path: str, repository_config_path: str):
        """
        Initialize the handler with the base path to the repositories and the path to the repository configuration file.
        
        :param repos_base_path: Base path where repositories are located
        :param repository_config_path: Path to the repository_config.json file
        """
        self.repos_base_path = repos_base_path
        self.repository_config_path = repository_config_path
        self.repositories = self.load_repository_config()
        self.config_data = None
        self.build_source_folder = None

    def load_repository_config(self) -> dict:
        """
        Load the repository configuration file.
        
        :return: Parsed JSON data of repository configuration
        """
        if os.path.exists(self.repository_config_path):
            with open(self.repository_config_path, 'r', encoding='utf-8') as file:
                return json.load(file).get("repositories", {})
        else:
            raise FileNotFoundError(f"Repository configuration file not found: {self.repository_config_path}")

    def find_openpublishing_config(self) -> str:
        """
        Find the .openpublishing.publish.config.json file from the repositories configuration.
        
        :return: Path to the .openpublishing.publish.config.json file
        """
        for repo_name, repo_info in self.repositories.items():
            potential_path = os.path.join(self.repos_base_path, repo_info["wiki_name"], ".openpublishing.publish.config.json")
            if os.path.exists(potential_path):
                return potential_path

        raise FileNotFoundError(".openpublishing.publish.config.json file not found in any of the configured repositories")

    def load_config(self):
        """
        Load the JSON configuration file.
        
        :return: Parsed JSON data
        """
        config_path = self.find_openpublishing_config()
        with open(config_path, 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)

    def get_build_source_folder(self):
        """
        Get the build_source_folder value from the 'docsets_to_publish' section.

        :return: The build_source_folder value
        """
        if self.config_data is None:
            self.load_config()
        
        docsets = self.config_data.get("docsets_to_publish", [])
        if docsets:
            self.build_source_folder = docsets[0].get("build_source_folder")
        else:
            raise ValueError("No docsets_to_publish found in the configuration")

    def get_docfx_json_path(self) -> str:
        """
        Get the path to the docfx.json file within the build_source_folder.

        :return: Path to the docfx.json file
        """
        if self.build_source_folder is None:
            self.get_build_source_folder()
            
        if self.build_source_folder:
            return os.path.join(self.build_source_folder, 'docfx.json')
        else:
            raise ValueError("build_source_folder is not set")

    def get_breadcrumb_toc_path(self) -> str:
        """
        Get the path to the breadcrumb/toc.yml file within the build_source_folder.

        :return: Path to the breadcrumb/toc.yml file
        """
        if self.build_source_folder is None:
            self.get_build_source_folder()
            
        if self.build_source_folder:
            return os.path.join(self.build_source_folder, 'breadcrumb', 'toc.yml')
        else:
            raise ValueError("build_source_folder is not set")
    
    def get_toc_path(self) -> str:
        """
        Get the path to the TOC.yml file within the build_source_folder.
        
        :return: Path to the TOC.yml file
        """
        if self.build_source_folder is None:
            self.get_build_source_folder()
            
        if self.build_source_folder:
            return os.path.join(self.build_source_folder, 'TOC.yml')
        else:
            raise ValueError("build_source_folder is not set")


if __name__ == "__main__":
    # Example usage
    repos_base_path = 'repos'
    repository_config_path = 'repository_config.json'

    config_handler = OpenPublishingConfigHandler(repos_base_path, repository_config_path)
    
    docfx_json_path = config_handler.get_docfx_json_path()
    print("docfx.json path:", docfx_json_path)
    
    breadcrumb_toc_path = config_handler.get_breadcrumb_toc_path()
    print("breadcrumb/toc.yml path:", breadcrumb_toc_path)
    
    toc_path = config_handler.get_toc_path()
    print("TOC.yml path:", toc_path)