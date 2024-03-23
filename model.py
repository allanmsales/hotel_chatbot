from pydantic import BaseModel


class Message(BaseModel):
    message: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Hello! My name is Jhon"
            }
    }

class Database(BaseModel):
    name: str
    checkin: str
    checkout: str
    guesses: str
    room: str
    payment: str
    breakfast: str
    restrictions: str
    referral: str
    driver: str