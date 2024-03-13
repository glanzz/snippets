import string
import random
import json
import os
from snippet.constants import GC_CACHE, GC_MANIFEST_FILE

class GCCache:
  def __init__(self, local_root) -> None:
    self.root_path = local_root
    self.cache_path = f"{self.root_path}/{GC_CACHE}"
    if not self.is_gc_initalized():
      self.init_cache()
    self.load_manifest()

  def is_gc_initalized(self):
    return os.path.exists(self.cache_path)

  def init_cache(self):
    with open(self.root_path + "/.gitignore", "a+") as gitignore:
      gitignore.seek(0)
      content = gitignore.read()
      if GC_CACHE not in content:
          gitignore.write("\n" + GC_CACHE+ "\n")

    os.mkdir(self.cache_path)
    with open(self.__get_manifest_filename(), mode="w") as cache_file:
      json.dump({}, cache_file)

  def __get_manifest_filename(self):
    return self.cache_path + f"/{GC_MANIFEST_FILE}"

  def load_manifest(self):
    with open(self.__get_manifest_filename()) as manifest:
      self.manifest = json.load(manifest)

  def write_cache(self, contents, specification):
    content_cache_filename = self.generate_file_name() + ".py"
    content_cache_path = self.cache_path + "/" + content_cache_filename
    # Write to manifest, save the new content
    with open(content_cache_path, "w") as cache_file:
      cache_file.write(contents)
    

    if not self.manifest.get(specification):
      self.manifest[specification] = os.path.abspath(content_cache_path)
    else:
      print("Existing Key")

    self.write_manifest()
  
  @classmethod
  def generate_file_name(cls):
    return "".join(random.choices(string.ascii_letters, k=20)) # Change k relative to file size in git

  def write_manifest(self, mode="w"):
    with open(self.__get_manifest_filename(), mode=mode) as manifest:
        json.dump(self.manifest, manifest)