import argparse
import requests
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import threading

class DirectoryManager:
    def __init__(self, user_name):
        self.user_name = user_name
        self.base_dir = os.path.expanduser(f"~/src/github.com/{user_name}")
        self.stash_dir = os.path.join(self.base_dir, 'x1')
        self.lock = threading.Lock()

    def process_directories(self):
        with ThreadPoolExecutor() as executor:
            for dir_name in os.listdir(self.base_dir):
                executor.submit(self.process_directory, dir_name)

    def process_directory(self, dir_name):
        with self.lock:
            full_dir_path = os.path.join(self.base_dir, dir_name)

            try:
                assert os.path.isdir(full_dir_path) and not self.github_url_exists(dir_name)
                response = self.get_user_input(dir_name)

                if response == 'y':
                    print(f"Attempting to delete directory: {dir_name}")
                    try:
                        shutil.rmtree(full_dir_path)
                        print(f"The directory '{dir_name}' has been deleted.: {full_dir_path}")
                    except Exception as e:
                        print(f"Failed to delete '{dir_name}': {str(e)}")
                    print(f"Executed action: delete_directory on directory: {dir_name}")
                elif response == 'n':
                    stash_path = os.path.join(self.stash_dir, dir_name)
                    self.move_directory(full_dir_path, stash_path, dir_name)
                    print(f"Executed action: move_directory on directory: {dir_name}")
                elif response == 's':
                    print(f"Executed action: skip_directory on directory: {dir_name}")
                else:
                    print("Invalid response. Skipping the directory.")

            except AssertionError:
                print(f"✅ {full_dir_path}")
                return


    def get_user_input(self, dir_name):
        return input(f"The directory '{dir_name}' does not exist on GitHub.\nDo you want to delete it? (y/n/s for skipping): ").lower()


    def github_url_exists(self, dir_name):
        url = f"https://github.com/{self.user_name}/{dir_name}"
        response = requests.get(url)
        return response.status_code == 200

    def move_directory(self, dir_path, stash_path, dir_name):
        shutil.move(dir_path, stash_path)
        print(f"Moved the directory '{dir_name}' into the stash directory.")

    def skip_directory(self, _dir_path, _stash_path, dir_name):
        print(f"Skipped the directory '{dir_name}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cleans up your GitHub directory. Assuming the directory is a public repository on your account.")
    parser.add_argument("username", nargs="?", default="aalemayhu",
                        help="GitHub username to check for repo existence. If not provided, the default is 'aalemayhu'.")
    args = parser.parse_args()

    manager = DirectoryManager(args.username)
    os.makedirs(manager.stash_dir, exist_ok=True)
    manager.process_directories()

