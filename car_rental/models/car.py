from sqlalchemy import Column, String, INTEGER, FLOAT, ForeignKey
from sqlalchemy.orm import relationship, validates
from car_rental.models import Base
from sqlalchemy.ext.hybrid import hybrid_property


class CarTypes(Base):

    __tablename__ = "car_types"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    type_name = Column(String(128), nullable=False)

    car_item = relationship("CarItems", back_populates="car_type")

    @hybrid_property
    def columns(self):
        return [m.key for m in self.__table__.columns]

    def __repr__(self):
        return f"Car Type id: {self.id}, type name: {self.type_name}"


class Cars(Base):

    __tablename__ = "cars"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    brand = Column(String(128), nullable=True, index=True)
    model = Column(String(128), nullable=True)

    car_item = relationship("CarItems", back_populates="car")

    @hybrid_property
    def columns(self):
        return [m.key for m in self.__table__.columns]

    def __repr__(self):
        return f"Car id: {self.id}, brand: {self.brand}, model {self.model}"


class CarItems(Base):

    __tablename__ = "car_items"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    car_id = Column(INTEGER, ForeignKey("cars.id"), nullable=True)
    car_type_id = Column(INTEGER, ForeignKey("car_types.id"), nullable=True)
    price_per_day = Column(FLOAT(precision="6,2"), nullable=True)
    production_year = Column(String(4), nullable=False)
    engine = Column(String(20))
    fuel = Column(String(20), nullable=False)
    availability = Column(INTEGER, nullable=False, default=1)

    car = relationship("Cars", back_populates="car_item")
    car_type = relationship("CarTypes", back_populates="car_item")
    order = relationship("Orders", back_populates="car_item")

    @hybrid_property
    def columns(self):
        return [m.key for m in self.__table__.columns]

    @validates("availability")
    def validate_availability(self, key, availability):
        assert int(availability) in (0, 1)
        return availability

    def __repr__(self):
        return f"Car item: {self.id}, brand: {self.car.brand}, model: {self.car.model}, type: {self.car_type.type_name}"
