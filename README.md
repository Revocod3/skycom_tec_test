
### Proyecto de Django Rest Framework (Backend)

```markdown
# Django Rest Framework API

Este proyecto es una API construida con Django y Django Rest Framework.

## Requisitos

Asegúrate de tener instalado lo siguiente:

- [Python 3.8+](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/) (gestor de paquetes de Python)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (opcional pero recomendado para aislar las dependencias del proyecto)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Revocod3/skycom_tec_test.git

2. Accede al directorio del proyecto: cd nombre_proyecto o cd tab

3. Crea un entorno virtual:
    python -m venv venv
    source venv/bin/activate 

4. Instala las dependencias: pip install -r requirements.txt

5. Aplica las migraciones:
   python manage.py makemigrations
   python manage.py migrate

6. Ejecuta el script para popular data:
   python manage.py populate_data

7. Ejecuta el servidor localmente:
   python manage.py runserver
