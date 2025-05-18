from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    price_usd = Column(Integer, nullable=True)
    odometer = Column(Integer, nullable=True)
    username = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    images_count = Column(Integer, nullable=True)
    car_number = Column(String, nullable=True)
    car_vin = Column(String, unique=True)
    datetime_found = Column(DateTime(timezone=True), server_default=func.now())
