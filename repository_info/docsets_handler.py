import os
from docfx_handler import DocfxHandler
from toc_handler import TOCHandler
from breadcrumb_handler import BreadcrumbHandler

class DocsetsHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.docfx_handler = self.load_docfx_handler(file_path)
        self.toc_handler = self.load_toc_handler(file_path)
        self.breadcrumb_handler = self.load_breadcrumb()

    # docsets で指定されたパスの直下に存在するため
    def load_docfx_handler(self, file_path: str):
        docfx_path = os.path.join(file_path, "docfx.json")
        return DocfxHandler(docfx_path)
        
    # docsets で指定されたパスの直下に存在するため
    def load_toc_handler(self, file_path: str):
        toc_path = os.path.join(file_path, "TOC.yml")
        return TOCHandler(toc_path)

    def load_breadcrumb(self):
        bread_crumb_path = self.docfx_handler.bread_crumb_path
        return BreadcrumbHandler(bread_crumb_path)
    
if __name__ == "__main__":
    file_path = "../repos/DevOps/release-notes"
    docsets_handler = DocsetsHandler(file_path)
    print("\ndocfx_config: \n")
    print(docsets_handler.docfx_handler.docfx_config)
    print("\nTOC.yml: \n")
    print(docsets_handler.toc_handler.toc)
    print("\nbreadcrumb toc.yml: \n")
    print(docsets_handler.breadcrumb_handler.config)