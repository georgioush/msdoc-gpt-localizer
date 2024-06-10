import json
import subprocess

class RepositoryManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.repositories = self.load_config()
        
    def load_config(self):
        with open(self.config_path, 'r') as f:
            config = json.load(f)
        return config['repositories']
    
    def clone_repositories(self):
        for repo in self.repositories:
            repo_url = repo['url']
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            subprocess.run(['git', 'clone', '--depth=1', repo_url, f'./repos/{repo_name}'])
            print(f'Repository {repo_name} cloned.')
    
if __name__ == "__main__":
    manager = RepositoryManager('./config.json')
    manager.clone_repositories()