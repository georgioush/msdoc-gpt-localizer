import os
from repository_manager import RepositoryManager
from result_saver import ResultSaver
from translator import Translator

def main():
    # 環境変数から設定を取得
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    # MarkdownProcessorのテスト
    print("Running MarkdownProcessor...")
    md_processor = MarkdownProcessor('../repos')
    md_files = md_processor.get_markdown_files()
    for md_file in md_files:
        soup = md_processor.parse_markdown(md_file)
        print(soup.prettify())
    
    # RepositoryManagerのテスト
    print("\nRunning RepositoryManager...")
    repo_manager = RepositoryManager('repository_config.json')
    repo_manager.clone_repositories()
    
    # ResultSaverのテスト
    print("\nRunning ResultSaver...")
    files_to_save = ['../translated.md', '../image.png']
    if not os.path.exists(files_to_save[0]):
        open(files_to_save[0], 'w').close()  # テスト用の空ファイルを作成
    if not os.path.exists(files_to_save[1]):
        open(files_to_save[1], 'w').close()
    result_saver = ResultSaver('../results')
    result_saver.save_files(files_to_save)
    
    # Translatorのテスト
    print("\nRunning Translator...")
    translator = Translator(api_key, azure_endpoint, deployment_name, api_version)
    text = "Hello, how are you?"
    translated_text = translator.translate_text(text)
    print("Translated text:", translated_text)

if __name__ == "__main__":
    main()