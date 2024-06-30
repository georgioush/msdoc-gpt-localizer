import os
from repository_manager import RepositoryManager
from classes.repository_info.repository_info_handler import RepositoryInfoHandler
from classes.msmarkdown.markdown_translator import MarkdownTranslator

def main():
    manager = RepositoryManager()
    manager.clone_repositories()

    repo_paths = manager.get_repo_paths()
    repository_info_handler = RepositoryInfoHandler(repo_paths[0])

    # docset は複数の可能性がある (DevOps などはそう)
    for docset_handler in repository_info_handler.docsets_handlers:
        mds_files = docset_handler.toc_handler.existing_md_files
        folder_path = docset_handler.file_path
        mds_paths = [os.path.join(folder_path, md) for md in mds_files]

        print(mds_paths)

        for md_path in mds_paths:
            markdown_handler = MarkdownTranslator(md_path)
            markdown_handler.translate()
            markdown_handler.save_translation()

if __name__ == "__main__":
    main()