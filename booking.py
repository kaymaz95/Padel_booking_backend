from datetime import datetime, timedelta
bookings = []


def create_booking(customer, court, start_time, duration):
    if not customer.strip():
        raise ValueError("customer name can not be empty.")
    if duration <= 0 or duration > 60:
        raise ValueError("Invalid booking duration.")
    if court <=0 or court > 3:
        raise ValueError("Invalid court number")
    
    start_time = datetime.strptime(start_time, "%H:%M")
    duration_delta = timedelta(minutes=duration)
    end_time = start_time + duration_delta

    for booking in bookings:
        if booking['court'] == court:
            existing_start = booking["start_time"]
            existing_end = booking["end_time"]

            if start_time < existing_end and existing_start < end_time:
                raise ValueError("court already booked!")

    booking = {
            "customer": customer,
            "court": court,
            "start_time": start_time,
            "end_time": end_time,
            "duration": duration,
            "confirmed": True,
            
        } 
    
    bookings.append(booking)
    return booking

def get_booking(customer):
    
    for booking in bookings:
        if booking["customer"] == customer:
            return booking
    raise ValueError("customer not found")

def get_court_bookings(court):
     courtbookings =[]
     
     for booking in bookings:
          if booking['court'] == court:
           courtbookings.append(booking)
     if courtbookings:
       return courtbookings    
     raise ValueError("no bookings found")
          

def cancel_booking(customer):

    for booking in bookings:
        if booking["customer"] == customer:
           
            bookings.remove(booking)

            return booking
            
    raise ValueError("customer not found")


def get_customer_bookings(customer):
     customer_bookings =[]
     
     for booking in bookings:
          if booking['customer'] == customer:
           customer_bookings.append(booking)
     return customer_bookings    
     
def get_bookings_by_duration(duration):
     customer_bookings_byduration =[]
     
     for booking in bookings:
          if booking['duration'] == duration:
           customer_bookings_byduration.append(booking)
     return customer_bookings_byduration    

    
        
            
        

