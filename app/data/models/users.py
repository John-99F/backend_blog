from sqlalchemy import Column, Integer, String
from app.data.database import Base


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    name =  Column(String(200))
    surname = Column(String(200))
    email = Column(String(120), unique= True)
    password = Column(String)

    def to_dict(self):
        return {
            "id":self.id, 
            "name": self.name,
            "surName": self.surname,
            "email": self.email,
            "password":self.password
        }

