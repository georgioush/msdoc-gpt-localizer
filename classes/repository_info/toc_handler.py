import os
import yaml

class TOCHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.toc = self.load_toc()
        self.md_files = self.get_md_file_names()
        self.existing_md_files = self.check_files_exist(self.md_files)

    def load_toc(self):
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"TOC file not found: {self.file_path}")
        
        with open(self.file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def get_md_file_names(self):
        md_file_names = []

        # extract_and_find_href 関数を使ってすべての href を取得する
        all_hrefs = self.extract_and_find_href(self.toc)

        for href in all_hrefs:
            if href.endswith(".md"):
                md_file_names.append(href)
            else:
                split_href = href.split("?")
                if split_href[0].endswith(".md"):
                    md_file_names.append(split_href[0])
        
        return md_file_names

    def extract_and_find_href(self, node):
        href_files = []

        # 再帰的にすべての href を取得する
        def find_hrefs(n):
            if isinstance(n, dict):
                for key, value in n.items():
                    if key == "href":
                        href_files.append(str(value))
                    else:
                        find_hrefs(value)
            elif isinstance(n, list):
                for item in n:
                    find_hrefs(item)

        find_hrefs(node)
        return href_files

    def check_files_exist(self, md_files: list) -> list:
        existing_md_files = []
        folder_path = os.path.dirname(self.file_path)

        for file_name in md_files:
            full_path = os.path.join(folder_path, file_name)
            if not os.path.exists(full_path):
                print(f"File not found: {full_path}")
            else:
                existing_md_files.append(file_name)
        
        print(f"existing_md_files nums: {len(existing_md_files)}")
        return existing_md_files

# Example usage
if __name__ == "__main__":
    toc_file_path = "../../repos/DevOps/docs/toc.yml"
    toc_handler = TOCHandler(toc_file_path)

    folder_path = os.path.dirname(toc_handler.file_path)
    print(f"Folder path: {folder_path}")
    print(f"existing_md_files nums: {len(toc_handler.existing_md_files)}")
