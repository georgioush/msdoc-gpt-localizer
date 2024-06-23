import os
from repository_manager import RepositoryManager
from repository_info.repository_info_handler import RepositoryInfoHandler
from markdown_handler import MarkdownHandler

def main():
    manager = RepositoryManager()
    manager.clone_repositories()

    repo_paths = manager.get_repo_paths()
    repository_info_handler = RepositoryInfoHandler(repo_paths[0])

    mds = repository_info_handler.toc_handler.get_md_file_names()
    source_folder = repository_info_handler.config_handler.build_source_folder

    relative_md_paths = [os.path.join(source_folder, md) for md in mds]

    markdown_handler = MarkdownHandler(relative_md_paths[0])
    markdown_handler.repository_info_handler = repository_info_handler
    
    markdown_handler.translate_markdown()

if __name__ == "__main__":
    main()