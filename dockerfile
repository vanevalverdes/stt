# Usa la imagen oficial de Python
FROM python:3.10

# Establece el directorio de trabajo
WORKDIR /code

ENV FLASK_APP app.py

ENV FLASK_RUN_HOST 0.0.0.0

COPY requirements.txt requirements.txt

# Instala las dependencias
RUN pip install -r requirements.txt

COPY . .

# Comando para ejecutar la aplicación
CMD ["flask", "run"]
