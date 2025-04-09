from pydantic import BaseModel

# schema for user creation requests
class UserCreate(BaseModel):
    name: str
    email: str

class DriverCreate(BaseModel):
    name: str
    email: str
    car_model: str

class RideRequest(BaseModel):
    user_id: int

class RideResponse(BaseModel):
    id: int
    status: str