import os
import yaml

# 与えられた TOC ファイルから情報を取得するために使用されるべきクラス。
# 例えば、別のファイルの情報を参照しないと取得できないようなものは利用するべきではない

class TOCHandler:
    def __init__(self, file_path : str):
        self.toc_file_path = file_path
        self.toc = self.load_toc()
        self.md_files_paths = self.get_md_files_paths()

    def load_toc(self):
        if not os.path.exists(self.toc_file_path):
            raise FileNotFoundError(f"TOC file not found: {self.toc_file_path}")
        
        with open(self.toc_file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def get_name_href_pairs(self):
        return self.extract_name_href_pairs(self.toc)

    def extract_name_href_pairs(self, content: yaml):
        pairs = []
        if isinstance(content, list):
            for item in content:
                pairs.extend(self.extract_name_href_pairs(item))
        elif isinstance(content, dict):
            name = content.get('name', None)
            href = content.get('href', None)
            if name and href:
                pairs.append({'name': name, 'href': href})

            items = content.get('items', [])
            pairs.extend(self.extract_name_href_pairs(items))
        return pairs

    def extract_hrefs(self, content: yaml):
        hrefs = []
        if isinstance(content, list):
            for item in content:
                hrefs.extend(self.extract_hrefs(item))
        elif isinstance(content, dict):
            href = content.get('href', None)
            if href:
                hrefs.append(href)

            items = content.get('items', [])
            hrefs.extend(self.extract_hrefs(items))
        return hrefs

    def get_md_file_names(self):
        md_file_paths = []
        hrefs = self.extract_hrefs(self.toc)
        

        for href in hrefs:
            if href.endswith('.md'):
                md_file_paths.append(href)
        return md_file_paths

