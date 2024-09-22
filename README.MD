### Migrations 

'''
migrations steps 
1. Initialize alembic migrations  : alembic init migrations 
2. change sqlalchemy.url link : in alembic.ini

3. in .env set Base metadata for the target.none value = Base.metadata : ensure import of Base declaration.
and add the following environmental imports : 
### imports added
import sys 
import os 
### Make sure Alembic can find the models directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
### import your models
from models.band import Band
from models.concert import Concert 
from models.venue import Venue 
from utils.tools import Base

4. generation initial migration : alembic revision --autogenerate -m "Initial migration"
4. applying the migration : python -m alembic upgrade head 
5. to delete a migration then run : python -m alembic downgrade 
'''

- instances are created in the app.py file 
