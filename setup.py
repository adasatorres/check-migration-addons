#setup.py
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
)