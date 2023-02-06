from config.base_de_datos import base
from sqlalchemy import Column, Integer, String, Float

class Ventas(base):
    # nombre de la tabla
    __tablename__ = "ventas"
    id = Column(Integer, primary_key= True)
    fecha = Column(String)
    tienda = Column(String)
    importe = Column(Float)