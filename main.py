
# Paso a paso detallado para crear un agente que explique SQL usando GPT y FastAPI

# Paso 1: Crear un entorno de trabajo
# -----------------------------------
# 1.1 Crea una carpeta para tu proyecto, por ejemplo: "sql-explainer-agent"
# 1.2 Abre esa carpeta en VS Code
# 1.3 Crea un entorno virtual (opcional pero recomendable):
#     python -m venv venv
#     source venv/bin/activate  # En Linux/Mac
#     .\venv\Scripts\activate   # En Windows

# Paso 2: Instalar dependencias necesarias
# ----------------------------------------
# En la terminal, instala estas librerías:
# pip install fastapi uvicorn openai

# Paso 3: Crear el archivo del agente (main.py)
# ---------------------------------------------
# Dentro de tu carpeta, crea un archivo llamado "main.py" con este contenido:




# Importa FastAPI para crear el servidor web
from fastapi import FastAPI

# Importa BaseModel para definir el esquema del JSON de entrada
from pydantic import BaseModel

# Importa el cliente oficial de OpenAI
from openai import OpenAI

# Importa módulos para acceder a variables de entorno
import os
from dotenv import load_dotenv

# Carga las variables del archivo .env (como la clave API)
load_dotenv()

# Crea el cliente OpenAI con tu clave y la URL oficial
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # Clave obtenida del archivo .env
    base_url="https://api.openai.com/v1"  # URL de la API oficial
)

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Define el modelo de datos que espera el endpoint (JSON con clave 'query')
class SQLQuery(BaseModel):
    query: str

# Define el endpoint POST /explicar
@app.post("/explicar")
def explicar_sql(data: SQLQuery):
    try:
        # Crea el prompt que se enviará a GPT para que explique la consulta
        prompt = f"Explica de forma clara y sencilla qué hace esta consulta SQL:\n\n{data.query}"
        
        # Envía el prompt al modelo gpt-3.5-turbo de OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Modelo de lenguaje usado
            messages=[{"role": "user", "content": prompt}],  # Mensaje del usuario
            temperature=0.3  # Grado de creatividad (bajo = más preciso)
        )
        
        # Extrae y limpia la respuesta generada por el modelo
        texto = response.choices[0].message.content.strip()
        
        # Devuelve la explicación como respuesta JSON
        return {"explicacion": texto}
    
    # Captura errores y los devuelve como mensaje de error
    except Exception as e:
        return {"error": str(e)}


# Paso 4: Ejecutar el agente localmente
# -------------------------------------
# En la terminal:
# uvicorn main:app --reload

# Esto levanta el servidor en http://localhost:8000
# Y puedes probarlo visualmente en http://localhost:8000/docs

# Paso 5: Probar el endpoint
# --------------------------
# Ve a /docs en el navegador y usa el endpoint POST /explicar
# Ingresa una consulta como:
# {
#   "query": "SELECT nombre FROM clientes WHERE edad > 60;"
# }
# Y recibirás algo como:
# "Selecciona el nombre de los clientes que tienen más de 60 años."

# Una vez esto funcione, el próximo paso será conectar esto con una extensión de VS Code

