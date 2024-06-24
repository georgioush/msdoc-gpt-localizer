import os
from repository_manager import RepositoryManager
from repository_info.repository_info_handler import RepositoryInfoHandler
from markdown_translator import MarkdownTranslator

def main():
    manager = RepositoryManager()
    manager.clone_repositories()

    repo_paths = manager.get_repo_paths()
    repository_info_handler = RepositoryInfoHandler(repo_paths[0])

    mds = repository_info_handler.toc_handler.get_md_file_names()
    source_folder = repository_info_handler.config_handler.repos_base_path
    build_source_folder = repository_info_handler.config_handler.build_source_folder

    mds_paths = [os.path.join(source_folder, build_source_folder, md) for md in mds]

    print(mds_paths)

    for md_path in mds_paths:
        markdown_handler = MarkdownTranslator(md_path)
        markdown_handler.translate()
        markdown_handler.save_translation()

if __name__ == "__main__":
    main()