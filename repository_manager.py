import os
import json
import subprocess
import shutil

class RepositoryManager:
    def __init__(self, config_path="repository_config.json"):
        self.config_path = config_path
        self.config_data = self.load_config()
        self.repo_paths = self.get_repo_paths()
        self.output_folder = self.config_data.get("output_folder")

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as file:
                return json.load(file)
        else:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

    def clone_repositories(self):
        for repo in self.config_data.get("repos", []):
            base = self.config_data.get("clone_folder")
            repo_name = repo.get("name")

            clone_destination = os.path.join(base, repo_name)
            repo_url = repo.get("repo_url")

            if repo_url:
                if not os.path.exists(clone_destination):
                    os.makedirs(clone_destination)
                    self.run_clone_command(repo_url, clone_destination)
                    self.copy_to_outrepos(repo_name, clone_destination)  # Copy to output_folder after successful clone
                else:
                    print(f"Folder '{clone_destination}' already exists. Skipping clone for repository '{repo_name}'.")

    def run_clone_command(self, repo_url, clone_destination):
        try:
            subprocess.run(["git", "clone", repo_url, clone_destination], check=True)
            print(f"Cloned {repo_url} into {clone_destination}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to clone {repo_url}: {e}")

    def copy_to_outrepos(self, repo_name, clone_destination):

        outrepos_path = os.path.join(self.output_folder, repo_name)
        if os.path.exists(outrepos_path):
            shutil.rmtree(outrepos_path)
        shutil.copytree(clone_destination, outrepos_path)
        print(f"Copied {clone_destination} to {outrepos_path}")

    def get_repo_paths(self):
        
        base = self.config_data.get("clone_folder")

        repos = self.config_data.get("repos", [])
        names = [repo["name"] for repo in repos]
        paths = [os.path.join(base, name) for name in names]

        return paths

if __name__ == "__main__":
    manager = RepositoryManager()
    manager.clone_repositories()

    # Example usage of get_repo_path
    repo_paths = manager.get_repo_paths()
    print("Repo paths:", repo_paths)