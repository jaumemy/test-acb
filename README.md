# test-acb

Proyecto Django para crear tres endpoints que retornan información acerca de un partido

* Clonar repositorio
```bash
git clone https://github.com/jaumemy/test-acb.git
git clone git@github.com:jaumemy/test-acb.git
```

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

1. **Obtener token**:

POST `http://localhost:8000/acb-api/token/`
```bash
curl -X POST -d "username={usuario}&password={contraseña}" http://localhost:8000/acb-api/token/
```

2. **Actualizar token**:

POST `http://localhost:8000/acb-api/token/refresh/`
```bash
curl -X POST http://localhost:8000/acb-api/token/refresh/ -H "Content-Type: application/json" -d '{"refresh": "{refresh}"}'
```

3. **Endpoints**:

GET `http://localhost:8000/acb-api/pbp-lean/103789`
```bash
curl --location --request GET 'http://localhost:8000/acb-api/pbp-lean/103789' \
--header 'Authorization: Bearer {access}'
```

GET `http://localhost:8000/acb-api/game-leaders/103789`
```bash
curl --location --request GET 'http://localhost:8000/acb-api/game-leaders/103789' \
--header 'Authorization: Bearer {access}'
```

GET `http://localhost:8000/acb-api/game-biggest-lead/103789`
```bash
curl --location --request GET 'http://localhost:8000/acb-api/game-biggest-lead/103789' \
--header 'Authorization: Bearer {access}'
```


## Tests

Ejecutar desde directorio raíz

```bash
pytest
```
