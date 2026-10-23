from fastapi import FastAPI, HTTPException
from booking import get_booking, create_booking
from pydantic import BaseModel

app = FastAPI()

class BookingRequest(BaseModel):
    customer: str
    court: int
    start_time: str
    duration: int


@app.get("/health")
def health():
    return {"status": "ok",
            "service": "padel-booking"
           }

@app.get("/bookings/{customer}")
def get_customer(customer: str):
    try: 
        booking = get_booking(customer)
        return booking
    except ValueError:
        raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/bookings")
def add_booking(request: BookingRequest):
    try:
        bookingreq = create_booking(
            request.customer, 
            request.court,
            request.start_time,
            request.duration
            )
        return bookingreq
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
