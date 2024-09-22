from sqlalchemy import ForeignKey, Column, String, Integer, create_engine
from sqlalchemy import func
from sqlalchemy.orm import relationship,joinedload
from utils.tools import Base

class Venue(Base):
    __tablename__ = 'venues'
    
    # attributes , columns 
    id = Column(Integer,primary_key = True)
    city = Column(String)
    title = Column(String,unique=True)
    concert_id = Column(Integer, ForeignKey('concerts.id'))
    
    # one to many : points to a list of concerts for this venue 
    # Relationship to concerts, specify the foreign key to avoid ambiguity
    concerts = relationship("Concert", back_populates="venue", foreign_keys="[Concert.venue_id]")
    
    #object relationship methods 
    # Object Relationship Methods
    def get_concerts(self):
        """Returns a collection of all concerts for the Venue."""
        return self.concerts

    def get_bands(self, session):
        from models.band import Band
        from models.concert import Concert
        """Returns a collection of all bands who performed at the Venue."""
        return session.query(Band).join(Concert).filter(Concert.venue_id == self.id).all()

    def concert_on(self, date, session):
        """Finds and returns the first concert on a given date at this venue as a formatted string."""
        from models.concert import Concert
        concert = session.query(Concert).filter_by(venue_id=self.id, date=date).first()
        if concert:
            # Format and return the concert details as a string
            band_name = concert.band.name if concert.band else "Unknown Band"
            concert_date = concert.date
            return f"Concert Details: Band: {band_name}, Date: {concert_date}, Venue: {self.title}, City: {self.city}"
        return f"No concert found on {date} at {self.title}, {self.city}."

    def most_frequent_band(self, session):
        """Finds and returns the band that has performed the most frequently at this venue as a formatted string."""
        from models.band import Band
        from models.concert import Concert
        # Subquery to count the number of concerts for each band at this venue
        subquery = session.query(
            Concert.band_id,
            func.count(Concert.id).label('performance_count')
        ).filter_by(venue_id=self.id).group_by(Concert.band_id).subquery()
        
        # Query to find the band with the maximum count of performances
        most_performances_band_id = session.query(
            subquery.c.band_id
        ).order_by(subquery.c.performance_count.desc()).limit(1).scalar()
        
        # Retrieve the band instance
        band = session.query(Band).filter_by(id=most_performances_band_id).first()
        
        if band:
            # Format and return the band details as a string
            return f"Band with most performances at {self.title}, {self.city}: Name: {band.name}, Hometown: {band.hometown}, Date: {band.date}"
        
        return f"No bands have performed at {self.title}, {self.city}."