from sqlalchemy import Column ,String,Integer,Boolean
from src.utils.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__= 'Users'

    user_id = Column(Integer,primary_key=True,index=True)
    user_name = Column(String,unique=True)
    email= Column(String,unique=True)
    hash_password = Column(String)
    role = Column(String,default='user')

    is_active = Column(Boolean,default= False)
    bookings = relationship("Bookings", back_populates="user")