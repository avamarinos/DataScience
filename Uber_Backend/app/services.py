from sqlalchemy.orm import Session
from . import models,schemas

# service function to create new user in database

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def request_ride(db: Session, ride_request: schemas.RideRequest):
    ride = models.Ride(user_id = ride_request.user_id)
    db.add(ride)
    db.commit()
    db.refresh(ride)
    return ride
