# check-migration-addons

**Descripción corta:**  

Este script permite revisar si existe el addon migrado en la rama destino,
o si hay un PR abierto y genera un excel con el estado de cada addon.

---

## Contenido del Proyecto

- `main.py` → Script principal que ejecuta la lógica del proyecto.  
- `setup.py` → Script de instalación del paquete.  
- `config.ini` → Archivo de configuración.

---

## Instalación

Se recomienda instalar con pip:

```bash
pip install .
```

o pipx:

```bash
pipx install .
```
Nota: Actualmente debes de utilizar este comando dentro de la ruta del proyecto donde se encuentra el archivo setup.

## Configuración y uso

Para utilizar check-migration-addons necesitas 3 parametros obligatorios.

- `--file` → Este parámetro índica la ruta absoluta o relativa de donde se encuentra el archivo excel a utilizar.
- `--branch` →  Este parámetro índica la rama destino.
- `--token` → Este parámetro índica el token de github a usar.

Ejemplo:

```bash
  check-migration-addons --file=./test/test.xlsx --branch=17.0 --token=your_api_token
```
## Dependencias

Las dependencias python que utiliza este proyecto son las siguientes: 
- `requests>=2.30.0`
- `openpyxl>=3.1.0`
- `pandas>=2.1.0`
  
