from sqlalchemy import ForeignKey, Column, String, Integer, create_engine
from sqlalchemy.orm import relationship
from utils.tools import Base

class Concert(Base):
    __tablename__ = 'concerts'
    
    # attributes , columns 
    id = Column(Integer,primary_key = True)
    band_id = Column(Integer, ForeignKey('bands.id'),nullable=False)
    venue_id = Column(Integer, ForeignKey('venues.id'),nullable=False)
    date = Column(String,nullable=False)
    
    # many to many 
    band = relationship("Band", back_populates="concerts")
    venue = relationship("Venue", back_populates="concerts", foreign_keys=[venue_id])  # Specify the foreign key
    
    # object relationship methods
    def get_band(self):
        """Returns the Band instance for this Concert."""
        return self.band

    def get_venue(self):
        """Returns the Venue instance for this Concert."""
        return self.venue
    
    def hometown_show(self):
        """
        Returns True if the concert is in the band's hometown, otherwise False.
        """
        # Check if the band and venue are set
        if self.band and self.venue:
            return self.venue.city.lower() == self.band.hometown.lower()
        return False

    def introduction(self):
        """
        Returns a string with the band's introduction for this concert.
        """
        # Check if the band and venue are set
        if self.band and self.venue:
            return (f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}")
        return "Introduction details are missing."
