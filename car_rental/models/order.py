from sqlalchemy import Column, String, INTEGER, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from car_rental.models import Base
from datetime import datetime


class Orders(Base):

    __tablename__ = "orders"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    client_id = Column(INTEGER, ForeignKey("clients.id"), nullable=False)
    car_id = Column(INTEGER, ForeignKey("car_items.id"), nullable=False)
    _order_data_start = Column(TIMESTAMP, default=datetime.now())
    _order_data_stop = Column(TIMESTAMP)
    order_status = Column(String(128), default="pending")
    payment_type = Column(String(128))

    car_item = relationship("CarItems", back_populates="order")
    client = relationship("Clients", back_populates="orders")

    @hybrid_property
    def order_data_start(self):
        return self._order_data_start.strftime("%d-%m-%Y %H:%M")

    @hybrid_property
    def order_data_stop(self):
        if self._order_data_stop:
            return self._order_data_stop.strftime("%d-%m-%Y %H:%M")

    @hybrid_property
    def price(self):
        if self.order_data_stop:
            order_time = self._order_data_stop - self._order_data_start
            return (order_time.total_seconds() // (3600*24)) * self.car_item.price_per_day

    @hybrid_property
    def columns(self):
        return [m.key for m in self.__table__.columns]

    @validates("order_status")
    def validate_status(self, key, value):
        assert value in ("pending", "finished")
        return value

    def set_order_data_stop(self):
        self._order_data_stop = datetime.now()

    def set_order_status(self, status):
        self.order_status = status

    def __repr__(self):

        return (
            f"Order: id {self.id}, client {self.client.full_name}, "
            f"data: {self.order_data_start}, rented car: {self.car_item.car.brand} {self.car_item.car.model}"
        )
