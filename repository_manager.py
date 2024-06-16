import os
import json
import subprocess

class RepositoryManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

    def clone_repositories(self):
        for repo_name, repo in self.config_data.get("repositories", {}).items():
            repo_url = repo.get("repo_url")
            output_folder = self.config_data.get("output_folder")
            repo_folder_name = os.path.join(output_folder, repo_name)

            if repo_url and output_folder:
                if not os.path.exists(repo_folder_name):
                    os.makedirs(repo_folder_name)
                    self.run_clone_command(repo_url, repo_folder_name)
                else:
                    print(f"Folder '{repo_folder_name}' already exists. Skipping clone for repository '{repo_name}'.")

    def run_clone_command(self, repo_url, output_folder):
        try:
            subprocess.run(["git", "clone", repo_url, output_folder], check=True)
            print(f"Cloned {repo_url} into {output_folder}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo_url}: {e}")

if __name__ == "__main__":
    manager = RepositoryManager("repository_config.json")
    manager.clone_repositories()