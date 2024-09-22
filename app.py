from utils.tools import create_db, SessionLocal
from models.band import Band
from models.concert import Concert
from models.venue import Venue
from sqlalchemy.exc import IntegrityError

session = SessionLocal()

def band_exists(session, name):
    return session.query(Band).filter_by(name=name).first() is not None

def venue_exists(session, title):
    return session.query(Venue).filter_by(title=title).first() is not None

def concert_exists(session, band_id, venue_id, date):
    return session.query(Concert).filter_by(band_id=band_id, venue_id=venue_id, date=date).first() is not None

def add_band(session, name, hometown, date):
    existing_band = session.query(Band).filter_by(name=name).first()
    if existing_band:
        print(f"Band '{name}' already exists in the database.")
        return existing_band
    try:
        new_band = Band(name=name, hometown=hometown, date=date)
        session.add(new_band)
        session.commit()
        print(f"Band '{name}' added successfully.")
        return new_band
    except Exception as e:
        session.rollback()
        print(f"Error adding band: {e}")
        return None

def add_venue(session, city, title):
    existing_venue = session.query(Venue).filter_by(title=title).first()
    if existing_venue:
        print(f"Venue '{title}' already exists in the database.")
        return existing_venue
    try:
        new_venue = Venue(city=city, title=title)
        session.add(new_venue)
        session.commit()
        print(f"Venue '{title}' added successfully.")
        return new_venue
    except Exception as e:
        session.rollback()
        print(f"Error adding venue: {e}")
        return None

def add_concert(session, band_id, venue_id, date):
    if concert_exists(session, band_id, venue_id, date):
        print(f"Concert on {date} with band ID {band_id} at venue ID {venue_id} already exists.")
        return None
    try:
        new_concert = Concert(band_id=band_id, venue_id=venue_id, date=date)
        session.add(new_concert)
        session.commit()
        print(f"Concert added successfully.")
        return new_concert
    except Exception as e:
        session.rollback()
        print(f"Error adding concert: {e}")
        return None

# Object relationship and concert aggregrated method check 
band1 = add_band(session=session, name="Hart the band", hometown="Nairobi", date="19/09/2024")
if band1:
    venue1 = add_venue(session=session, city="Nairobi", title="KICC")
    if venue1:
        concert1 = add_concert(session=session, band_id=band1.id, venue_id=venue1.id, date="19/09/2024")
        if concert1:
            # Debug print statements
            print(f"Concert 1: Band ID = {concert1.band_id}, Venue ID = {concert1.venue_id}, Date = {concert1.date}")
            print(f"Band: {concert1.get_band().name}, Venue: {concert1.get_venue().title}")
            print(concert1.hometown_show())
            print(concert1.introduction())

        else:
            print("Concert 1 could not be added.")

band2 = add_band(session=session, name="The Rolling Stones", hometown="London", date="20/09/2024")
if band2:
    venue2 = add_venue(session=session, city="London", title="O2 Arena")
    if venue2:
        concert2 = add_concert(session=session, band_id=band2.id, venue_id=venue2.id, date="20/09/2024")
        if concert2:
            # Debug print statements
            print(f"Concert 2: Band ID = {concert2.band_id}, Venue ID = {concert2.venue_id}, Date = {concert2.date}")
            print(f"Band: {concert2.get_band().name}, Venue: {concert2.get_venue().title}")
            print(concert2.hometown_show())
            print(concert2.introduction())
        else:
            print("Concert 2 could not be added.")
            

# aggregrate relationship tests for band
if band1:
   print(band1.all_introductions())
   print(band1.play_in_venue(venue1,"20/4/2024"))
   
# Band most peformances 
print(Band.most_performances(session=session))


## venues aggregrate relationship methods 
print(venue2.concert_on(date="20/09/2024",session=session))
print(venue2.most_frequent_band(session=session))

session.close()
