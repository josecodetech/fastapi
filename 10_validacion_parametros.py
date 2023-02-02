from fastapi import FastAPI, Body, Path, Query

from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
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
    id: int = Field(ge=0, le=20)
    #id: Optional[int]=None
    fecha: str
    #tienda: str = Field(default="Tienda01",min_length=4, max_length=10)
    tienda: str = Field(min_length=4, max_length=10)
    #tienda:str
    importe:float
    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "fecha":"01/02/23",
                "tienda":"Tienda09",
                "importe":131
            }
        }

# crear punto de entrada o endpoint


@app.get('/', tags=['Inicio'])  # cambio de etiqueta en documentacion
def mensaje():
    return HTMLResponse('<h2>Titulo html desde FastAPI</h2>')


@app.get('/ventas', tags=['Ventas'])
def dame_ventas():
    return ventas


@app.get('/ventas/{id}', tags=['Ventas'])
def dame_ventas(id: int = Path(ge=1,le=1000)):
    for elem in ventas:
        if elem['id'] == id:
            return elem
    return []


@app.get('/ventas/', tags=['Ventas'])
def dame_ventas_por_tienda(tienda: str=Query(min_length=4,max_length=20)):  # para mas parametros ,id:int
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