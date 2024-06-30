import json
import os

# 与えられたレポジトリのパスから、.openpublishing.publish.config.json ファイルを読み込み、各種情報を取得するためのクラス
# 例えば、別のファイルの情報を参照しないと取得できないようなものは利用するべきではない

class OpenPublishingConfigHandler:
    def __init__(self, repos_path: str):
        self.repos_base_path = repos_path
        self.config = self.load_openpublishing_config()
        self.docsets_paths = self.get_docsets_paths()

    def load_openpublishing_config(self):
        config_path = os.path.join(self.repos_base_path, ".openpublishing.publish.config.json")
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_docsets_paths(self):
        docsets_paths = []
        for docset in self.config["docsets_to_publish"]:
            path = os.path.join(self.repos_base_path, docset["build_source_folder"])
            docsets_paths.append(path)
        return docsets_paths
