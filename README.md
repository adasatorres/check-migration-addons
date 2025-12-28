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
- `--branches` →  Este parámetro índica las rama destino separadas por comas. Por ejemplo :  17.0,18.0
- `--token` → Este parámetro índica el token de github a usar.
- `--column-dir-name` → Este parametro indica la columna del nombre tecnico del addon o directorio a buscar en el repositorio.
- `--column-url-github` → Este parametro indica la columna del con la url del repositorio a buscar.

Ejemplo:

```bash
  check-migration-addons --file=./test/test.xlsx --branches=17.0,18.0 --token=your_api_token  --column-dir-name="Nombre técnico" --column-url-github="Sitio web"
```
## Dependencias

Las dependencias python que utiliza este proyecto son las siguientes: 
- `requests>=2.30.0`
- `openpyxl>=3.1.0`
- `pandas>=2.1.0`
  
