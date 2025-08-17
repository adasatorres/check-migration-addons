#!/usr/bin/env python3
"""
This script verifies the existence of specific directories in GitHub repositories
based on a list provided in an input Excel file. It utilizes the GitHub API to check
the status of directories in specified branches of the repositories.

The script performs the following key functions:
1. Initializes configuration settings from a 'config.ini' file.
2. Parses command-line arguments to obtain the input file, branch name, and GitHub token.
3. Reads an Excel file containing a list of repositories and their corresponding directories.
4. Checks if the specified directories exist in the given repositories and branches.
5. Outputs the results to the console and saves them to a new Excel file.

Usage:
    python main.py --input-file <input_file_path> --branch <branch_name> --token <github_token>

Dependencies:
    - pandas
    - requests
    - openpyxl
"""

import argparse
import configparser
import importlib.resources
import pandas as pd 
import requests
import re
import os
config = configparser.ConfigParser()

def init_config() -> None:
    """
    Initializes the configuration by loading settings from the 'config.ini' file.

    This function reads the configuration file located in the 'src' directory
    and prints the sections of the configuration that have been loaded.

    Returns:
        None: This function does not return any value.
    """
    with importlib.resources.path('src', 'config.ini') as config_path:
        config.read(config_path)
        print("Configuración cargada:", config.sections())
        
def get_arguments() -> dict:
    """
    Parses command-line arguments for the GitHub repository verification script.

    This function uses argparse to handle input from the command line, requiring
    the user to specify an input file containing a list of repositories, a branch name,
    and a personal access token for GitHub.

    Returns:
        dict: A dictionary containing the parsed command-line arguments.
            - 'file': The input file with the list of repositories (str).
            - 'branch': The name of the branch (str).
            - 'token': The personal access token for GitHub (str).
    """
    parser = argparse.ArgumentParser(description="Verifica directorios en repositorios de GitHub desde un fichero y exporta resultados a Excel")
    parser.add_argument("--file", help="Fichero de entrada con la lista de repositorios", required=True)
    parser.add_argument("--branch", required=True, help="Nombre de la rama (por defecto la principal)")
    parser.add_argument("--token", required=True, help="Token de acceso personal de GitHub")
    return vars(parser.parse_args())
   

def read_file(file_path: str) -> pd.DataFrame:
    """
    Reads an Excel file and returns its content as a pandas DataFrame.

    Parameters:
    file_path (str): The path to the Excel file to be read.

    Returns:
    pd.DataFrame: A DataFrame containing the data from the specified Excel file,
                  with specified columns and without any missing values.

    Raises:
    FileNotFoundError: If the specified file does not exist.
    ValueError: If the file cannot be read or the specified columns are not found.
    """
    df = pd.read_excel(
        file_path, 
        usecols=[col.strip() for col in config['options'].get('headers').split(",")], 
        engine="openpyxl"
    ).dropna()
    print("Fichero leído correctamente:", file_path)
    return df

def get_repo_name(url: str) -> str:
    """
    Extracts the repository name from a given GitHub URL.

    Args:
        url (str): The URL of the GitHub repository.

    Returns:
        str: The repository name in the format 'owner/repo' if the URL is valid,
             otherwise an empty string.
    """
    
    print('Obteniendo nombre del repositorio de la URL:', url)
    result =  re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if result:
       return f"{result.group(1)}/{result.group(2)}"
    else:
        return ""
    
def check_directory(repo: str, directory: str, branch: str, token: str) -> str:
    """
    Checks if a specific directory exists in a given GitHub repository and branch.

    Args:
        repo (str): The full name of the repository (e.g., 'owner/repo').
        directory (str): The path of the directory to check.
        branch (str): The branch name to check in the repository.
        token (str): The GitHub personal access token for authentication.

    Returns:
        str: A message indicating the result of the check. It can indicate
             whether the directory exists, if it is found in an open pull request,
             or if the repository or directory was not found.
    """
    headers = {
        'Accept' : 'application/vnd.github.v3+json',
        'Authorization' : f'token {token}' if token else ''
    }
    print('Comprobando addon:', directory, 'en repositorio:', repo, 'en rama:', branch)
    url = f"https://api.github.com/repos/{repo}/contents/{directory}?ref={branch}"
    response = requests.get(url, headers=headers, stream=True)
    code = response.status_code
    response.close()
    if code == 200:
        return f"Addon migrado en {branch}."
    elif code == 404:
        print(f"Addon no encontrado en {branch}, comprobando si hay PR abierto...")
        url_pull = f"https://api.github.com/repos/{repo}/pulls?state=open&per_page=20&page=1"
        while url_pull:
            response_pull = requests.get(url_pull, headers=headers, stream=True)
            if response_pull.status_code == 200:
                pulls = response_pull.json()
                pattern = rf"\[{branch}\]\[(ADD|MIG)\]{directory}".lower()

                #pr = list(filter(lambda pr: f"[{branch}][MIG]{directory}".lower() in pr["title"].lower().replace(" ", ""), pulls))
                pr = list(filter(lambda pr: re.search(pattern, pr["title"].lower().replace(" ", "")), pulls))
                if pr:
                    return f"PR: {pr[0]['html_url']}"
            url_pull = response_pull.links.get('next', {}).get('url', None)
    return """Repositorio o addon no encontrado, revisar manualmente."""
    

def current_path(path) -> str:
    """
    Generate a new file path based on the provided path.

    This function takes a file path, extracts the file name and its extension,
    and returns a new path with the same name but with '_estado' appended before
    the file extension. The new path is relative to the current directory.

    Args:
        path (str): The original file path.

    Returns:
        str: The modified file path with '_estado' appended to the file name.
    """
    name, extension = os.path.splitext(os.path.basename(path))
    return os.path.join('./', f"{name}_estado{extension}")
    

def main() -> None:
    """
    Main function to execute the script.

    This function initializes the configuration, retrieves command-line arguments,
    reads an input file into a DataFrame, checks the status of directories based on
    the repository names and other parameters, and then saves the results to an Excel file.

    The following steps are performed:
    1. Initialize configuration settings.
    2. Get command-line arguments.
    3. Read the input file into a DataFrame.
    4. Apply a function to each row of the DataFrame to determine the status of directories.
    5. Print the results to the console.
    6. Save the modified DataFrame to an Excel file.

    Returns:
        None
    """
    init_config()
    kwargs = get_arguments()
    df = read_file(kwargs.get('file'))
    df['status'] = df.apply(
        lambda row: check_directory(
            get_repo_name(row[config['options'].get('column_url_github')]), 
            row[config['options'].get('column_dir_name')],
            kwargs['branch'],
            kwargs['token']
            ),
        axis=1
    )
    print("Resultados obtenidos:")
    print(df)
    print("Guardando resultados en:", current_path(kwargs.get('file')))
    df.to_excel(current_path(kwargs.get('file')) , index=True)
        
        
    
   
    
