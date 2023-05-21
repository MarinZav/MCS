FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./proyecto_mineria_de_contrastes ./proyecto_mineria_de_contrastes

CMD ["python", "./proyecto_mineria_de_contrastes/modelo_stucco.py"]