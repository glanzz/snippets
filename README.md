### Snippets

Import snippets of code from any git repository dynamically to your working repository.

#### Use Cases
- Control part of code without deployment just by development. Version your config file and use it
- Runtime import of utility functions from one repository for personal projects
- Reuse API integrations functions across multiple repositories
- Run scripts for cron jobs without deploying multiple times to during development


Easy Install:

1. `pip install snippets`
2. Import snippet by specifying the format (`author/repository/path_to_file[@commit_hash]:L{start_line}-{end_line}`)
```python
  from snippet import snippet
  snip = snippet("glanzz/flask_doc_gen/flask_doc_gen/constants.py:L1-10")
```

3. Use the snip similar to a module
```python
print(snip.var1)
```


This is beta version for demonstrating the idea. If any issues found or feature to be added feel free to contribute.
