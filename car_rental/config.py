import os


class Config:

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.dirname(__file__)}/car_rental.db"
