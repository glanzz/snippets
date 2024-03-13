import os
from snippet.util import Utility
from snippet.gc_cache import GCCache      
from enum import Enum

class HOST(Enum):
  GITHUB = 1
  GIST = 2


class InvalidFormatException(Exception):
  def __init__(self, *args: object) -> None:
    super().__init__(*args)
    self.message = "Invalid snippet specification format given"


current_path = os.path.realpath(__file__)
local_git = Utility.get_git(file_path=current_path)
local_root_folder = Utility.get_git_root(local_git)
gc_cache = GCCache(local_root=local_root_folder)

def snippet(specification, host=HOST.GITHUB.name):
  snippet_location = ""
  if not gc_cache.manifest.get(specification):
    try:
      _specification = specification     
      author, remaining = specification.split("/", 1)
      start_line, end_line = 0,0
      repo_name, remaining = remaining.split("/", 1)
      file_path, remaining = remaining.split(":L")
      file_path, commit_hash = Utility.safe_split(file_path, "@", 2)
      if remaining:
        start_line, end_line = remaining.split("-")
    except Exception as e:
      raise InvalidFormatException()

    git_content = Utility.fetch_git_content(author, repo_name, file_path, commit_hash)
    replace_content = git_content.split("\n")[int(start_line)-1:int(end_line)]
    replace_content = "\n".join(replace_content)
    gc_cache.write_cache(replace_content, _specification)

  snippet_location = gc_cache.manifest[specification]
  return Utility.get_module(snippet_location)
