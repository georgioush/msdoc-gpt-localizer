import json
import git
import os

class RepositoryManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.repositories = self.load_config()
        
    def load_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config['repositories']
    
    def clone_repositories(self):
        for name, repo in self.repositories.items():
            repo_url = repo['git_url']
            dest_path = os.path.join('.', 'repos', name)
            if not os.path.exists(dest_path):
                # --depth 1 オプションを使用して直近のコミットだけを取得
                git.Repo.clone_from(repo_url, dest_path, depth=1)
                print(f'Repository {name} cloned.')
            else:
                print(f'Repository {name} already exists at {dest_path}.')

if __name__ == "__main__":
    manager = RepositoryManager('repository_config.json')
    manager.clone_repositories()