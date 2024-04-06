# Utiliza una imagen base de Python con Pipenv
FROM python:3.11-slim

# Instala pipenv
RUN pip install pipenv

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el Pipfile y el Pipfile.lock a la imagen
COPY Pipfile Pipfile.lock ./

# Instala las dependencias del Pipfile
RUN pipenv install --system --deploy

COPY . .

EXPOSE 5000

CMD ["pipenv", "run", "python", "src/app.py"]