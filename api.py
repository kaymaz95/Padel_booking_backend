from fastapi import FastAPI, HTTPException
from booking import get_booking

app = FastAPI()



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
