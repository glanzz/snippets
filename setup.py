import setuptools

setuptools.setup(
    name='snippets',
    version='0.0.1',
    author='Glanzz',
    description='Import snippets',
    url='https://github.com/glanzz/snippets',
    project_urls = {
        "Bug Tracker": "https://github.com/bhargavcn/snippets/issues"
    },
    license='MIT',
    packages=['snippets'],
    install_requires=['git-python==1.0.3'],
)