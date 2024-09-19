# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Band(Base):
    __tablename__ = 'bands'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hometown = Column(String)
    
    # Relationship with Concert
    concerts = relationship('Concert', back_populates='band')

    def __repr__(self):
        return f"<Band(name={self.name}, hometown={self.hometown})>"

class Venue(Base):
    __tablename__ = 'venues'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    city = Column(String)
    
    # Relationship with Concert
    concerts = relationship('Concert', back_populates='venue')

    def __repr__(self):
        return f"<Venue(title={self.title}, city={self.city})>"

class Concert(Base):
    __tablename__ = 'concerts'
    
    id = Column(Integer, primary_key=True)
    date = Column(String)
    band_id = Column(Integer, ForeignKey('bands.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    
    # Relationships
    band = relationship('Band', back_populates='concerts')
    venue = relationship('Venue', back_populates='concerts')

    def __repr__(self):
        return f"<Concert(band={self.band.name}, venue={self.venue.title}, date={self.date})>"
