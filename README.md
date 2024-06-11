# test-acb

Proyecto Django para crear tres endpoints que retornan información acerca de un partido

## Activar el Entorno Virtual

Para este proyecto, se recomienda utilizar un entorno virtual de Python para gestionar las dependencias de manera aislada. Sigue estos pasos para activar el entorno virtual:

1. **Crear el Entorno Virtual**:

   ```bash
   python3.12 -m venv <nombre_del_entorno>
   ```
   *Ya existe uno llamado acb-env

1. **Activar el Entorno Virtual**: 

    ```bash
    source <nombre_del_entorno>/bin/activate
    ```
    ```bash
    source acb-env/bin/activate
    ```

2. **Instalar Dependencias**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Desactivar el Entorno Virtual**:

    ```bash
    deactivate
    ```

## Inicialización del Proyecto Django

1. **Migraciones**:
   
    ```bash
    acb/manage.py migrate
    ```

2. **Crear usuario**:
   
   ```bash
   acb/manage.py createsuperuser
   ```

3. **Ejecutar servidor de desarrollo**:
   
   ```bash
   acb/manage.py runserver
   ```

## Endpoints de prueba

`http://127.0.0.1:8000/acb-api/pbp-lean/103789`

`http://127.0.0.1:8000/acb-api/game-leaders/103789`

`http://127.0.0.1:8000/acb-api/game-biggest-lead/103789`

*También funciona para otros partidos

### Pendiente
* Tests
* Autenticación
* Code Review
* ... 
