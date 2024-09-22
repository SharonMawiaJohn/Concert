from sqlalchemy import ForeignKey, Column, String, Integer, create_engine
from sqlalchemy.orm import relationship
from utils.tools import Base
from sqlalchemy import func

class Band(Base):
    __tablename__ = 'bands'
    
    # attributes , columns 
    id = Column(Integer,primary_key = True)
    name = Column(String, nullable=False,unique=True)
    hometown = Column(String,nullable=False)
    date = Column(String,nullable=False)

    
    # one to many : points to a list of concerts for this venue 
    # concerts plural attribute for mapping convention
    concerts = relationship('Concert', back_populates='band')
    
    # Object Relationship Methods
    def get_concerts(self):
        """Returns a collection of all concerts that the Band has played."""
        return self.concerts

    def get_venues(self, session):
        from models.venue import Venue
        from models.concert import Concert
        """Returns a collection of all venues where the Band has performed."""
        return session.query(Venue).join(Concert).filter(Concert.band_id == self.id).all()
    
    def play_in_venue(self, venue, date):
        """Creates a new concert for the band in the specified venue on the given date."""
        from models.concert import Concert
        from utils.tools import SessionLocal
        session = SessionLocal()
        # Check if a concert already exists for this band in the venue on the specified date
        existing_concert = session.query(Concert).filter_by(band_id=self.id, venue_id=venue.id, date=date).first()
        if existing_concert:
            print(f"Concert on {date} at {venue.title} already exists for this band.")
            return existing_concert

        # Create a new concert
        new_concert = Concert(band_id=self.id, venue_id=venue.id, date=date)
        session.add(new_concert)
        session.commit()
        print(f"Concert for band '{self.name}' at venue '{venue.title}' on {date} added successfully.")
        return new_concert

    def all_introductions(self):
        """Returns a list of all introductions for this band."""
        introductions = []
        for concert in self.concerts:
            venue = concert.get_venue()
            introduction = f"Hello {venue.city}!!!!! We are {self.name} and we're from {self.hometown}"
            introductions.append(introduction)
        return introductions


    @classmethod
    def most_performances(cls, session):
        """Returns a formatted string detailing the Band instance that has played the most concerts."""
        from models.concert import Concert
        # Subquery to count the number of concerts for each band
        subquery = session.query(
            Concert.band_id,
            func.count(Concert.id).label('performance_count')
        ).group_by(Concert.band_id).subquery()

        # Query to find the band with the maximum count of performances
        most_performances_band_id = session.query(
            subquery.c.band_id
        ).order_by(subquery.c.performance_count.desc()).limit(1).scalar()

        if not most_performances_band_id:
            return "No bands found."

        # Retrieve the band instance
        band = session.query(cls).filter_by(id=most_performances_band_id).first()
        
        if band:
            # Create a formatted string detailing the band
            performance_count = session.query(Concert).filter_by(band_id=band.id).count()
            return (f"Band with most performances:\n"
                    f"Name: {band.name}\n"
                    f"Hometown: {band.hometown}\n"
                    f"Date Formed: {band.date}\n"
                    f"Number of Concerts: {performance_count}")
        else:
            return "Band not found."
    
    
    
    
    
    
    