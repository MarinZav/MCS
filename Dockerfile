# Usa una imagen base de Python
FROM python:3.8-slim-buster

# Establece un directorio de trabajo
WORKDIR /app

# Copia los requerimientos de la aplicación al contenedor
COPY requirements.txt .

# Instala los requerimientos de la aplicación
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente de la aplicación al contenedor
COPY ./proyecto_mineria_de_contrastes ./proyecto_mineria_de_contrastes

# Establece el comando para ejecutar tu aplicación
CMD ["python", "./proyecto_mineria_de_contrastes/modelo_stucco.py"]
