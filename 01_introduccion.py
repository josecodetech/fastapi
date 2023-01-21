from fastapi import FastAPI

# crea instancia de fastapi
app = FastAPI()

# crear punto de entrada o endpoint


@app.get('/')
def mensaje():
    return 'Hola, bienvenido a FastAPI cambiado de nuevo'
