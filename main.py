from booking import create_booking
from booking import bookings
from booking import get_booking
from booking import get_court_bookings
from booking import cancel_booking


booking_requests = [
    {
        "customer": "Anaya",
        "court": 1,
        "start_time": "14:00",
        "duration": 45
    },
    {
        "customer": "Karl",
        "court": 1,
        "duration": 60
    },
    {
        "customer": "Sarah",
        "court": 2,
        "duration": 30
    },
    {
        "customer": "James",
        "court": 2,
        "duration": 60
    }
]

for bookingRequest in booking_requests:
    try:
        created_booking = create_booking(
            bookingRequest["customer"], 
            bookingRequest["court"],
            bookingRequest["duration"]
        )
    
    except ValueError as error:
        print(error)

result = get_booking("Anaya")

try:
    result = get_booking("Johnny")
    print(result)
except ValueError as error:
    print(error)


courtbookings = get_court_bookings(1)
print(courtbookings)
print('  ')
print('  ')


try:
    courtbookings = get_court_bookings(5)
    print(courtbookings)
except ValueError as error:
    print(error)

#cancelled_booking = cancel_booking('Karl')
#print(f'booking cancelled for {cancelled_booking['customer']} on court {cancelled_booking['court']}')
print('  ')
print('Confirmed bookings')
print('-----------------------')
print(bookings)
print('  ')
cancel_booking('Anaya')
print('  ')
print('Confirmed bookings at this point')
print(bookings)
print('  ')
try:
    create_booking("Karl",1, 60)
    print(bookings)
except ValueError as error:
    print(error)

print('-----------------------')

try:
    cancel_booking("Johnny")
    
except ValueError as error:
    print(error)
print(bookings)



print('-----------------------')
try:
    create_booking("",1,30)
except ValueError as error:
    print(error)

print('-----------------------')
print('current bookings list ')
print(bookings)









print("Program Finished")


