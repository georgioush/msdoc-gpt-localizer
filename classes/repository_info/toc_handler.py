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
        # yaml ファイルを再帰的に探索し、md ファイルのパスを取得する
        md_file_names = []

        all_hrefs = self.extract_and_find_href(self.toc)

        for href in all_hrefs:
            if href.endswith(".md"):
                md_file_names.append(href)
            else:
                split_href = href.split("?")
                if split_href[0].endswith(".md"):
                    md_file_names.append(split_href[0])
        
        return md_file_names

    # node の一番下にしか href がない
    def extract_and_find_href(self, node):
        href_files = []

        # node の最下層に href があるので、そこまで再帰的に探索していく
        if isinstance(node, list):
            for item in node:
                href_files.extend(self.extract_and_find_href(item))
        elif isinstance(node, dict):
            if "href" in node:
                href_files.append(str(node["href"]))
            else:
                for key, value in node.items():
                    href_files.extend(self.extract_and_find_href(value))

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
        return existing_md_files

# Example usage
if __name__ == "__main__":
    toc_file_path = "../../repos/DevOps/docs/toc.yml"
    toc_handler = TOCHandler(toc_file_path)

    folder_path = os.path.dirname(toc_handler.file_path)
    print(f"Folder path: {folder_path}")
    # print(f"existing_md_files: {toc_handler.existing_md_files}")