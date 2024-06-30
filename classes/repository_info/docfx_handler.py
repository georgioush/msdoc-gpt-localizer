import yaml
import os

class DocfxHandler:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.docfx_config = self.load_docfx_config(file_path)
        self.bread_crumb_path = self.get_breadcrumb_path()

    def load_docfx_config(self, file_path: str):
        try:
            with open(file_path, "r") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"docfx.json not found: {file_path}")

    def get_breadcrumb_path(self):
        breadcrumb_path = self.docfx_config["build"]["globalMetadata"]["breadcrumb_path"]

        # "breadcrumb_path": "~/breadcrumb/toc.yml", というかたちで指定されている
        # breadcrumb/toc.yml という形で指定されていることを想定して、後ろ2つのみを取得する
        # また file_path と同じ階層にあることを想定
        parts = breadcrumb_path.split('/')
        docfx_folder = os.path.dirname(self.file_path)
 
        # なぜか toc.json とかいう形式も globalMetadata にあるので、それを除外する
        breadcrumb_path = parts[-2]
        breadcrumb_path = os.path.join(docfx_folder, breadcrumb_path, "toc.yml")

        return breadcrumb_path


if __name__ == "__main__":
    file_path = "../repos/DevOps/release-notes/docfx.json"
    docfx_handler = DocfxHandler(file_path)
    print(docfx_handler.bread_crumb_path)