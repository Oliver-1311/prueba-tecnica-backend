
FROM python:3.11-slim

# Instala pipenv
RUN pip install pipenv

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Copia el Pipfile y el Pipfile.lock a la imagen
COPY Pipfile  ./
COPY Pipfile.lock ./
# Instala las dependencias del Pipfile
RUN pipenv install --deploy
COPY init_db.sql /docker-entrypoint-initdb.d/

COPY . .

EXPOSE 5000

CMD ["pipenv", "run", "python", "src/app.py"]