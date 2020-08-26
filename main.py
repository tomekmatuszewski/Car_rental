from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models.order import Orders
from models.car import CarItems, Cars
from models.client import Clients
from models import Base
from datetime import datetime

engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    client1 = Clients(first_name="Joe", last_name="Doe", pesel_number="91020516344",
                      address="Churchill street 2, London", email="joe.doe@yahoo.com", city_id=1)
    car = Cars(brand="Toyota", model="Corolla")
    car_item = CarItems(car_id=1, car_type_id=1, price_per_hour=20,
                    production_year='2016', engine="1.6 Turbo", fuel="petrol", availability=1)
    order1 = Orders(client_id=1, car_id=1)

    session.add(client1)
    session.add(car)
    session.add(car_item)
    session.add(order1)
    session.commit()
    print(session.query(Orders).all())
    print(session.query(Orders)[0].order_data_stop)
    session.query(Orders).filter_by(id=1).update({"payment_type": "card"})
    order1.set_order_status("finished")
    order1._order_data_stop = datetime(2020, 9, 2, 12, 0, 0)
    time = order1._order_data_stop - order1._order_data_start
    print(time)
    print(time.total_seconds() // 3600)
    session.commit()
    print(session.query(Orders)[0].order_data_stop)
    print(session.query(Orders)[0].price)



