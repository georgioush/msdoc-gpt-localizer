import yaml

class BreadcrumbHandler:

    # 与えられた breadcrumb フォルダ配下の TOC.yml を読み込むためのクラス
    # 問題は breadcrumb は crumb だったりするので、そこの対応が必要

    def __init__(self, file_path: str):
        self.repos_base_path = file_path
        self.config = self.load_breadcrumb_config()
        self.link_path = self.get_link_path()

    def load_breadcrumb_config(self):
        try:
            with open(self.repos_base_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"TOC file not found: {e}")
        
    def get_link_path(self):
        # TODO: Implement this method
        pass