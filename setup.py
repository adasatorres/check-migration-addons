"""
setup.py

This script is used for packaging the 'check_migration_addons' Python project.
It utilizes setuptools to define the package metadata and dependencies.

Package Information:
- Name: check_migration_addons
- Version: 1.0.0
- Author: Adasat Torres de León
- Author Email: adasat.torres.dev@gmail.com
- Description: Verifies migrated addons in GitHub repositories and generates Excel reports.
- URL: https://github.com/adasatorres/check-migration-addons

Dependencies:
- requests (>=2.30.0)
- openpyxl (>=3.1.0)
- pandas (>=2.1.0)

Entry Points:
- Console script: check-migration-addons, which executes the main function from src.main module.
"""
from setuptools import setup, find_packages

setup(
    name="check_migration_addons",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests>=2.30.0",
        "openpyxl>=3.1.0",
        "pandas>=2.1.0",
    ],
    entry_points={
        "console_scripts": [
            "check-migration-addons=src.main:main",  # mi_script.py con función main()
        ],
    },
    author="Adasat Torres de León",
    author_email="adasat.torres.dev@gmail.com",
    description="Verifica addons migrados en repositorios de GitHub y genera Excel",
    url="https://github.com/adasatorres/check-migration-addons",
)