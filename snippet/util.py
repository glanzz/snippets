import os
import importlib.util
import git
from snippet.constants import GC_CACHE

class Utility:
  @classmethod
  def get_git(cls, file_path):
    try:
        repo = git.Repo(file_path, search_parent_directories=True)
        return repo
    except git.exc.InvalidGitRepositoryError:
        Utility.exit_program("Error: The file is not in a Git repository.")
    except Exception as e:
      Utility.exit_program("Error: Failed to retrive git. Is git installed ?")

  @classmethod
  def get_git_root(cls, repo):
    return repo.git.rev_parse("--show-toplevel")
    
  @classmethod
  def is_gc_initalized(cls, local_git_root):
    return os.path.exists(local_git_root + f"/{GC_CACHE}")

  @classmethod
  def exit_program(cls, message):
    if message: print(message)
    exit(1)

  @classmethod
  def fetch_git_content(cls, author, repo_name, file_path, commit_hash=None, branch="main"):
    print(author, repo_name, commit_hash)
    repository_url = f"https://github.com/{author}/{repo_name}.git"
    try:
        # Initialize a Repo object without cloning the repository
        remote_repo = git.Repo.init('/tmp/remote-repo', bare=True)
        if 'origin' in remote_repo.remotes:
            remote_repo.delete_remote('origin')
        
        # Add 'origin' remote
        remote_repo.create_remote('origin', url=repository_url)
        
        # Fetch only the specific branch
        remote_repo.remote('origin').fetch(refspec=branch)

        
        # Get the commit object of the given commit hash
        commit = remote_repo.commit(f'refs/remotes/origin/{branch}') if not commit_hash else remote_repo.commit(commit_hash)
        
        # Get the content of the file from the commit
        file_content = commit.tree / file_path
        
        return file_content.data_stream.read().decode('utf-8')
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

  @classmethod
  def safe_split(cls, string, char, expected_char=2):
    char_count = string.count(char)
    if char_count == expected_char:
      return string.split(char)
    elif not char_count or (char_count > expected_char):
      empty_replacement = [""]*(expected_char - 1)
      return (string, *empty_replacement)
    else:
      split_results = string.split(char)
      empty_replacement = [""]*(expected_char - len(split_results) - char_count)
      return string.split(char, *empty_replacement)

  @classmethod
  def get_module(cls, file):
    spec = importlib.util.spec_from_file_location("module_creator", file)
    module_creator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_creator)
    return module_creator