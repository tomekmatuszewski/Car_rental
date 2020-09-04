from typing import List

from sqlalchemy import INTEGER, Column, ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, validates

from car_rental.control.data_access import Base
from car_rental.models.utils import email_validator


class Countries(Base):

    __tablename__ = "countries"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)

    cities = relationship("Cities", back_populates="country")

    @hybrid_property
    def columns(self) -> List:
        return [m.key for m in self.__table__.columns]

    def __repr__(self):
        return f"Country id: {self.id}, name: {self.name}"


class Cities(Base):

    __tablename__ = "cities"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    country_id = Column(INTEGER, ForeignKey("countries.id"), nullable=True)

    country = relationship("Countries", back_populates="cities")
    clients = relationship("Clients", back_populates="city")

    @hybrid_property
    def columns(self) -> List:
        return [m.key for m in self.__table__.columns]

    def __repr__(self):
        return f"City id: {self.id}, name: {self.name}"


class Clients(Base):

    __tablename__ = "clients"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    pesel_number = Column(String(8), nullable=True, unique=True)
    address = Column(String(128), nullable=True)
    email = Column(String(128), nullable=True, index=True, unique=True)
    city_id = Column(INTEGER, ForeignKey("cities.id"), nullable=True)

    city = relationship("Cities", back_populates="clients")
    orders = relationship("Orders", back_populates="client")

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @hybrid_property
    def columns(self) -> List:
        return [m.key for m in self.__table__.columns]

    @validates("email")
    def validate_email(self, key, clients):
        assert email_validator(clients)
        return clients

    def __repr__(self):
        return f"Client id: {self.id}, fullname: {self.full_name}, email: {self.email}, city: {self.city.name}"
