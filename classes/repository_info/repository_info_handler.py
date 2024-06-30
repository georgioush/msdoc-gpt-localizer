from classes.repository_info.open_publishing_config_handler import OpenPublishingConfigHandler
from classes.repository_info.docsets_handler import DocsetsHandler

# InfoHandler は repository_manager によってクローンされてきた各フォルダの情報を処理するクラスです。
# レポジトリに対して 1v1 で対応する。
# それ以前の各レポごとに Markdown 用の Handler を用意するのはユーザーの責任にする。
# レポジトリに対して、.openpublishing_config は 1 つ存在

# ただし "docsets_to_publish": [ は複数存在する場合がある     
#  "build_source_folder": "release-notes", も複数存在する
# よって docset Class を作成するべき。ただし docset が複数入れられる場合もあることをクラスとしては想定する

# breadcrumb や TOC.yml は必ず存在するので、密結合しているものとして info にする

class RepositoryInfoHandler:
    def __init__(self, repo_path: str):
        self.file_path = repo_path
        self.open_publishing_config_handler = OpenPublishingConfigHandler(repo_path)
        self.docsets_handlers = self.load_docsets(self.open_publishing_config_handler)

    def load_docsets(self, open_publishing_config_handler: OpenPublishingConfigHandler):
        docsets_handlers = []

        docsets_paths = open_publishing_config_handler.docsets_paths

        for docset_path in docsets_paths:
            docsets_handlers.append(DocsetsHandler(docset_path))

        return docsets_handlers

if __name__ == "__main__":
    repo_path = "../repos/DevOps"
    repo_info_handler = RepositoryInfoHandler(repo_path)

    print("file_path:")
    print(repo_info_handler.file_path)

    print("open_publishing_config:")
    print(repo_info_handler.open_publishing_config_handler.file_path)

    print("")

    for docset in repo_info_handler.docsets_handlers:
        print("docset_path:")
        print(docset.file_path)

        print("docfx_path:")
        print(docset.docfx_handler.file_path)

        print("TOC.yml:")
        print(docset.toc_handler.file_path)

        print("breadcrumb toc.yml:")
        print(docset.breadcrumb_handler.file_path)
