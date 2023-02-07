from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional,List
from config.base_de_datos import sesion, motor, base
from modelos.ventas import Ventas as VentasModelo
from jwt_config import dame_token,valida_token

# crea instancia de fastapi
app = FastAPI()
app.title = 'Aplicacion de ventas'
app.version = '1.0.1'
base.metadata.create_all(bind=motor)
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
class Usuario(BaseModel):
    email:str
    clave:str
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
# Portador token
class Portador(HTTPBearer):
    async def __call__(self, request:Request):
        autorizacion = await super().__call__(request)
        dato = valida_token(autorizacion.credentials)
        if dato['email'] != 'josecodetech@gmail.com':
            raise HTTPException(status_code=403, detail='No autorizado')
# crear punto de entrada o endpoint


@app.get('/', tags=['Inicio'])  # cambio de etiqueta en documentacion
def mensaje():
    return HTMLResponse('<h2>Titulo html desde FastAPI</h2>')


@app.get('/ventas', tags=['Ventas'], response_model=List[Ventas], status_code=200, dependencies=[Depends(Portador())])
def dame_ventas() -> List[Ventas]:
    return JSONResponse(content=ventas)


@app.get('/ventas/{id}', tags=['Ventas'], response_model = Ventas, status_code = 200)
def dame_ventas(id: int = Path(ge=1,le=1000)) -> Ventas:
    for elem in ventas:
        if elem['id'] == id:
            return JSONResponse(content=elem, status_code=200)
    return JSONResponse(content=[], status_code=404) 


@app.get('/ventas/', tags=['Ventas'], response_model=List[Ventas], status_code=200)
# para mas parametros ,id:int
def dame_ventas_por_tienda(tienda: str = Query(min_length=4, max_length=20)) -> List[Ventas]:
    # return tienda
    datos = [elem for elem in ventas if elem['tienda'] == tienda]
    return JSONResponse(content=datos, status_code=200)


@app.post('/ventas', tags=['Ventas'], response_model=dict, status_code=201)
def crea_venta(venta:Ventas) -> dict:
    db = sesion()
    # extraemos atributos para paso como parametros
    nueva_venta = VentasModelo(**venta.dict())
    # añadir a bd y hacemos commit para actualizar datos
    db.add(nueva_venta)
    db.commit()
    return JSONResponse(content={'mensaje': 'Venta registrada'}, status_code=200)


@app.put('/ventas/{id}', tags=['Ventas'], response_model=dict, status_code=201)
def actualiza_ventas(id: int, venta: Ventas) -> dict:
    # recorrer los elementos de la lista
    
    for elem in ventas:        
        if elem['id'] == id:
           elem['fecha'] = venta.fecha
           elem['tienda'] = venta.tienda
           elem['importe'] = venta.importe
    return JSONResponse(content={'mensaje': 'Venta actualizada'}, status_code=201)


@app.delete('/ventas/{id}', tags=['Ventas'], response_model=dict, status_code=200)
def borra_venta(id: int) -> dict:
    # recorremos elementos de la lista
    for elem in ventas:
        if elem['id'] == id:
            ventas.remove(elem)
    return JSONResponse(content={'mensaje':'Venta borrada'}, status_code=200)
#creamos ruta para login
@app.post('/login',tags=['autenticacion'])
def login(usuario:Usuario):
    if usuario.email == 'josecodetech@gmail.com' and usuario.clave == '1234':
        # obtenemos el token con la funcion pasandole el diccionario de usuario
        token:str=dame_token(usuario.dict())
        return JSONResponse(status_code=200,content=token)
    else:
        return JSONResponse(content={'mensaje':'Acceso denegado'}, status_code=404)