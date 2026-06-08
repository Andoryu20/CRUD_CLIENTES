# Proyecto CRUD con FastAPI
Es proyecto permite gestionar clientes relacionados con diferentes propiedades. Está construido con FastAPI y SQLAlchemy con una base de datos SQLite.

# Requisitos para hacerlo funcionar
- Python 3.13
- SQLite 

# Como hacerlo funcionar
- Crear un entorno virtual (ej. virtualenv -p python3 venv).
- Activar entorno virtual (ej. .\venv\Scripts\activate).
- Instalación de librerias del archivo "requirements.txt".
- Ejecutar el archivo seed.py, por defecto agregara 30 clientes de prueba de forma aleatoria
```
python seed.py
```
- Ejecutar el archivo generate_test_files.py para crear 3 archivos csv, xml, xmlx (opcional).
- Encender el servidor (bash: uvicorn app.main:app --reload)
- Acceder al Swagger UI o el localhost por defecto que se proporciona agregando al final de la url "docs" para acceder a los endpoints (ej. http://127.0.0.1:8000/docs).

# Funciones
- Paginación: Busqueda de clientes por medio de paginación con: 
* skip:Representa el número de registros desde el cual se empieza a contar siendo 0 su valor minimo, su valor máximo dependera del número de registros en la tabla.
* limit:Representael número de registros a solicitar por consultar, siendo 0 su valor minimo (ningún registro) y su valor máximo dependerá del número de registros en la tabla.
- Carga masiva: Carga de archivos csv, xml, xmlx.
- Reporte CSV: Generación de reportes en archivo csv.

# Ejemplo archivo csv
```
name_client,city,country_id,category_id,is_active
Juan Perez,Bogota,1,1,1
Maria Gomez,Medellin,2,2,1
Carlos 123,Bogota,1,1,1
Ana Torroja,Fusagasuga,1,1,1
Luis Torres,Madrid,99,1,1
```
