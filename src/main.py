#!/usr/bin/env python3
import argparse
import configparser
import importlib.resources
import pandas as pd 
import requests
import re
import os
config = configparser.ConfigParser()

def init_config() -> None:
    with importlib.resources.path('src', 'config.ini') as config_path:
        config.read(config_path)
        print("Configuración cargada:", config.sections())


def get_arguments() -> dict:
    parser = argparse.ArgumentParser(description="Verifica directorios en repositorios de GitHub desde un fichero y exporta resultados a Excel")
    parser.add_argument("--input-file", help="Fichero de entrada con la lista de repositorios", required=True)
    parser.add_argument("--branch", required=True, help="Nombre de la rama (por defecto la principal)")
    parser.add_argument("--token", required=True, help="Token de acceso personal de GitHub")
    return vars(parser.parse_args())
   

def read_file(file_path : str) -> pd.DataFrame:
    df = pd.read_excel(
        file_path, 
        usecols=[col.strip() for col in config['excel'].get('cabeceras').split(",")], 
        engine="openpyxl"
    ).dropna()
    print("Fichero leído correctamente:", file_path)
    return df

def get_repo_name(url: str) -> str:
    print('Obteniendo nombre del repositorio de la URL:', url)
    result =  re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if result:
       return f"{result.group(1)}/{result.group(2)}"
    else:
        return ""
    
def check_directory(repo: str, directory: str, branch: str, token: str) -> bool:
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
                pr = list(filter(lambda pr: f"[{branch}][MIG]{directory}".lower() in pr["title"].lower().replace(" ", ""), pulls))
                if pr:
                    return f"En PR: {pr[0]['html_url']}"
            url_pull = response_pull.links.get('next', {}).get('url', None)
    return """Repositorio o addon no encontrado, revisar manualmente."""
    

def current_path(path) -> str:
    name, extension = os.path.splitext(os.path.basename(path))
    return os.path.join('./', f"{name}_estado{extension}")
    

def main():
    init_config()
    kwargs = get_arguments()
    df = read_file(kwargs.get('input_file'))
    df['status'] = df.apply(
        lambda row: check_directory(
            get_repo_name(row['Sitio web']), 
            row["Nombre técnico"],
            kwargs['branch'],
            kwargs['token']
            ),
        axis=1
    )
    print("Resultados obtenidos:")
    print(df)
    print("Guardando resultados en:", current_path(kwargs.get('input_file')))
    df.to_excel(current_path(kwargs.get('input_file')) , index=True)
        
        
    
   
    
