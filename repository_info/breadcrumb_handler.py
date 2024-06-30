import yaml

class BreadcrumbHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = self.load_breadcrumb_config()
        self.link_path = self.get_weblink_path()

    def load_breadcrumb_config(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"TOC file not found: {e}")
        
    def get_weblink_path(self):
        for item in self.config:
            if 'tocHref' in item:
                return item['tocHref']
            else:
                raise KeyError("tocHref key not found in item")