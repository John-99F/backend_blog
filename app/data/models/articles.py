from sqlalchemy import Column, Integer, String
from app.data.database import Base


class Article(Base):
    __tablename__ = "Article"


    id = Column(Integer, primary_key=True)
    title =  Column(String(200))
    description = Column(String(200))
    autor_id = Column(Integer)
    date_creation = Column(String(120))
    image_url = Column(String(120))


    def to_dict(self):
        return {
            "id":self.id, 
            "title": self.title,
            "description": self.description,
            "autor_id": self.autor_id,
            "image_url":self.image_url
        }

