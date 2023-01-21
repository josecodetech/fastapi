from fastapi import FastAPI

# crea instancia de fastapi
app = FastAPI()
app.title = 'Aplicacion de ventas'
app.version = '1.0.1'
# crear punto de entrada o endpoint


@app.get('/', tags=['Inicio'])  # cambio de etiqueta en documentacion
def mensaje():
    return 'Hola, bienvenido a FastAPI cambiado de nuevo'
