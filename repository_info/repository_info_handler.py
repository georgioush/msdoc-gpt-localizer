from open_publishing_config_handler import OpenPublishingConfigHandler
from breadcrumb_handler import BreadcrumbHandler
from toc_handler import TOCHandler

# InfoHandler は repository_manager によってクローンされてきた各フォルダの情報を処理するクラスです。
# レポジトリに対して 1v1 で対応するべき。なので、それ以前の各レポごとに Handler を用意するのはユーザーの責任にする。
# レポジトリに対して、.openpublishing_config や breadcrumb や TOC.yml は必ず存在するので、密結合しているものとして info にする

class RepositoryInfoHandler:
    def __init__(self, repo_path: str):
        self.repos_base_path = repo_path
        self.config_handler = OpenPublishingConfigHandler(repo_path)
        self.toc_handler = TOCHandler(self.config_handler.toc_file_path)
        self.breadcrumb_handler = BreadcrumbHandler(repo_path)
