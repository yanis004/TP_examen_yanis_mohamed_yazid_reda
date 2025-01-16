from datetime import date
from app import models
from app.sqlite import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

def get_db():
    """
        Get the DB
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()



def age_from_birthdate(birthdate):
    """
        Return an age from a birthday
    """
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day)
        < (birthdate.month, birthdate.day))