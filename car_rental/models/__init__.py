from sqlalchemy.ext.declarative import declarative_base
from car_rental.models.car import CarItems, Cars, CarTypes
from models.order import Orders

Base = declarative_base()
