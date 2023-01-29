from fastapi import FastAPI, Body

from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

# crea instancia de fastapi
app = FastAPI()
app.title = 'Aplicacion de ventas'
app.version = '1.0.1'
ventas = [
    {
        "id": 1,
        "fecha": "01/01/23",
        "tienda": "Tienda01",
        "importe": 2500
    },
    {
        "id": 2,
        "fecha": "22/01/23",
        "tienda": "Tienda02",
        "importe": 4500
    }
]
# creamos el modelo
class Ventas(BaseModel):
    id: Optional[int]=None
    fecha: str
    tienda:str
    importe:float
    
# crear punto de entrada o endpoint


@app.get('/', tags=['Inicio'])  # cambio de etiqueta en documentacion
def mensaje():
    return HTMLResponse('<h2>Titulo html desde FastAPI</h2>')


@app.get('/ventas', tags=['Ventas'])
def dame_ventas():
    return ventas


@app.get('/ventas/{id}', tags=['Ventas'])
def dame_ventas(id: int):
    for elem in ventas:
        if elem['id'] == id:
            return elem
    return []


@app.get('/ventas/', tags=['Ventas'])
def dame_ventas_por_tienda(tienda: str):  # para mas parametros ,id:int
    # return tienda
    return [elem for elem in ventas if elem['tienda'] == tienda]


@app.post('/ventas', tags=['Ventas'])
def crea_venta(venta:Ventas):
    # return tienda
    ventas.append(venta)
    return ventas
@app.put('/ventas/{id}',tags=['Ventas'])
def actualiza_ventas(id: int, venta:Ventas):
    # recorrer los elementos de la lista

    for elem in ventas:

        if elem['id'] == id:
           elem['fecha'] = venta.fecha
           elem['tienda'] = venta.tienda
           elem['importe'] = venta.importe

    return ventas
@app.delete('/ventas/{id}',tags=['Ventas'])
def borra_venta(id:int):
    # recorremos elementos de la lista
    for elem in ventas:
        if elem['id'] == id:
            ventas.remove(elem)
    return ventas