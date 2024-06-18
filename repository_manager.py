import os
import json
import subprocess

class RepositoryManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config_data = self.load_config()
        self.repo_paths = self.get_repo_path()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

    def clone_repositories(self):
        for repo in self.config_data.get("repos", []):
            repo_name = repo.get("name")
            repo_url = repo.get("repo_url")
            repo_path = repo.get("path")
            repo_folder_name = os.path.join(repo_path)  # Use the path from the configuration

            if repo_url:
                if not os.path.exists(repo_folder_name):
                    os.makedirs(repo_folder_name)
                    self.run_clone_command(repo_url, repo_folder_name)
                else:
                    print(f"Folder '{repo_folder_name}' already exists. Skipping clone for repository '{repo_name}'.")
                
                self.repo_paths.append(repo_folder_name)  # Append the repo folder path to repo_paths

    def run_clone_command(self, repo_url, output_folder):
        try:
            subprocess.run(["git", "clone", repo_url, output_folder], check=True)
            print(f"Cloned {repo_url} into {output_folder}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo_url}: {e}")

    def get_repo_path(self):
        repos = self.config_data.get("repos", [])
        paths = [repo["path"] for repo in repos]
        return paths

if __name__ == "__main__":
    manager = RepositoryManager("repository_config.json")
    manager.clone_repositories()

    # Example usage of get_repo_path
    repo_paths = manager.get_repo_path()
    print("Repo paths:", repo_paths)