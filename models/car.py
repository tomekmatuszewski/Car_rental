from sqlalchemy import Column, String, INTEGER, FLOAT, DATE, BINARY, ForeignKey
from sqlalchemy.orm import relationship
from models import Base


class CarTypes(Base):

    __tablename__ = "car_types"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    type_name = Column(String(128), nullable=False)

    car_item = relationship("CarItems", back_populates="car_type")

    def __repr__(self):
        return f"Car Type id: {self.id}, type name: {self.type_name}"


class Cars(Base):

    __tablename__ = "cars"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    brand = Column(String(128), nullable=True, index=True)
    model = Column(String(128), nullable=True)

    car_item = relationship("CarItems", back_populates="car")


    def __repr__(self):
        return f"Car id: {self.id}, brand: {self.brand}, model {self.model}"


class CarItems(Base):

    __tablename__ = "car_items"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    car_id = Column(INTEGER, ForeignKey("cars.id"), nullable=True)
    car_type_id = Column(INTEGER, ForeignKey("car_types.id"), nullable=True)
    price_per_hour = Column(FLOAT(precision='6,2'), nullable=True)
    production_date = Column(DATE, nullable=False)
    engine = Column(String(20))
    fuel = Column(String(20), nullable=False)
    availability = Column(BINARY, nullable=False)

    car = relationship("Cars", back_populates="car_item")
    car_type = relationship("CarTypes", back_populates="car_item")

    def __repr__(self):
        return f"Car item: {self.id}, brand: {self.car.brand}, model: {self.car.model}, type: {self.car_type.type_name}"


