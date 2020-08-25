from sqlalchemy import Column, String, INTEGER, ForeignKey
from sqlalchemy.orm import relationship, validates
from models import Base
from models.utils import email_validator


class Countries(Base):

    __tablename__ = "countries"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)

    cities = relationship("Cities", back_populates="country")

    def __repr__(self):
        return f"Country id: {self.id}, name: {self.name}"


class Cities(Base):

    __tablename__ = "cities"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    country_id = Column(
        INTEGER, ForeignKey("countries.id", ondelete="CASCADE"), nullable=True
    )

    country = relationship("Countries", back_populates="cities")
    clients = relationship("Clients", back_populates="city")

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

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @validates("email")
    def validate_email(self, key, clients):
        assert email_validator(clients)
        return clients

    def __repr__(self):
        return f"Client id: {self.id}, fullname: {self.full_name}, email: {self.email}, city: {self.city.name}"
