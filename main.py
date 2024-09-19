# main.py
from models import Base, Band, Venue, Concert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Step 1: Set up the SQLite database engine
engine = create_engine('sqlite:///concerts.db')

# Step 2: Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Step 3: Create all tables in the database (this is equivalent to running migrations)
Base.metadata.create_all(engine)

# Step 4: Add sample data (Bands, Venues, and Concerts)
band1 = Band(name="The Rolling Stones", hometown="London")
band2 = Band(name="The Beatles", hometown="Liverpool")

venue1 = Venue(title="Madison Square Garden", city="New York")
venue2 = Venue(title="Wembley Stadium", city="London")

concert1 = Concert(date="2023-09-15", band=band1, venue=venue1)
concert2 = Concert(date="2023-10-01", band=band2, venue=venue2)

# Step 5: Add the data to the session and commit the transaction
session.add_all([band1, band2, venue1, venue2, concert1, concert2])
session.commit()

# Step 6: Query the database to verify everything was added correctly
bands = session.query(Band).all()
venues = session.query(Venue).all()
concerts = session.query(Concert).all()

print("Bands:", bands)
print("Venues:", venues)
print("Concerts:", concerts)
