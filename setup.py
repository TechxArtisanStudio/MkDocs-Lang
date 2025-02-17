from setuptools import setup, find_packages

setup(
    name='mkdocs-lang',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML',
        'mkdocs-material',
    ],
    entry_points={
        'console_scripts': [
            'mklang=mkdocs_lang.cli:main',
        ],
    },
) 