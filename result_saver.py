import os
import shutil

class ResultSaver:
    def __init__(self, dest_folder):
        self.dest_folder = dest_folder
        
    def save_files(self, files):
        if not os.path.exists(self.dest_folder):
            os.makedirs(self.dest_folder)
        for file in files:
            shutil.copy(file, self.dest_folder)
        print(f"Files saved to {self.dest_folder}")

if __name__ == "__main__":
    files = ['./translated.md', './image.png']
    saver = ResultSaver('./results')
    saver.save_files(files)