import json
import os

# 与えられたレポジトリのパスから、.openpublishing.publish.config.json ファイルを読み込み、各種情報を取得するためのクラス
# 例えば、別のファイルの情報を参照しないと取得できないようなものは利用するべきではない

class OpenPublishingConfigHandler:
    def __init__(self, repos_path: str):
        self.repos_base_path = repos_path
        self.config = self.load_openpublishing_config()
        self.build_source_folder = self.get_build_source_folder()
        self.toc_file_path = self.get_toc_file_path()

    def load_openpublishing_config(self):
        config_path = os.path.join(self.repos_base_path, ".openpublishing.publish.config.json")
        with open(config_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def get_build_source_folder(self):
        try:
            return self.config["docsets_to_publish"][0]["build_source_folder"]
        except (IndexError, KeyError) as e:
            raise ValueError(f"Error getting build source folder: {e}")

    def get_toc_file_path(self):
        build_source_folder = self.get_build_source_folder()
        toc_path = os.path.join(self.repos_base_path[0], build_source_folder, "TOC.yml")
        if not os.path.exists(toc_path):
            raise FileNotFoundError(f"TOC file not found: {toc_path}")
        return toc_path

    def get_breadcrumb_file_path(self):

        first_path = os.path.join(self.build_source_folder, "breadcrumb")
        breadcrumb_path = first_path

        if not os.path.exists(first_path):
            second_path = os.path.join(self.build_source_folder, "crumb")
            breadcrumb_path = second_path
            if not os.path.exists(second_path):
                raise FileNotFoundError(f"Breadcrumb file not found: {first_path} or {second_path}")
        return breadcrumb_path