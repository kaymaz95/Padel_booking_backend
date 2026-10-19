
from booking import create_booking
from booking import bookings
from booking import get_booking
from booking import get_court_bookings
from booking import cancel_booking
from booking import get_customer_bookings
from booking import get_bookings_by_duration

print("Test 1 ")
print('-----------------------')
create_booking("Karl",1,"12:00",30)
create_booking("Sarah",2,"12:30",45)
assert len(bookings) == 2, "Expected two bookings"
assert get_booking('Karl') ["customer"] == "Karl", "booking not found"
assert get_booking('Sarah') ["customer"] == "Sarah", "booking not found"

print(bookings)

print('  ')
print("Test 2")
print('-----------------------')
cancel_booking("Karl")
try:
    get_booking('Karl')
except ValueError :
    assert True
else:
    assert False, "Karl's booking still exists"
assert get_booking('Sarah') ["customer"] == "Sarah", "booking not found"
    

print('  ')
print("Test 3")
print('-----------------------')
create_booking("Anaya",1,"14:00",60)
print(bookings)
assert len(bookings) == 2, "Expected two bookings"
assert get_booking('Anaya') ["customer"] == "Anaya", "booking not found"
assert get_booking('Sarah') ["customer"] == "Sarah", "booking not found"

print('  ')
print("Test 4")
print('-----------------------')
bookings_before = bookings.copy()

try:
    create_booking("Jack", 1, "14:30", 60)
except ValueError:
    pass
else:
    assert False, "Jack's booking was unexpectedly accepted"

assert bookings == bookings_before, "Bookings changed after rejection"
assert get_booking('Anaya') ["customer"] == "Anaya", "booking not found"
assert get_booking('Sarah') ["customer"] == "Sarah", "booking not found"

print('  ')
print("Test 5")
print('-----------------------')
court_booking_check = get_court_bookings(1)
print(court_booking_check)
assert len(court_booking_check) == 1, "Expected one bookings"
assert court_booking_check[0] ["customer"]== "Anaya", "customer not found"
assert court_booking_check[0] ["court"] == 1, "court not found"

try:
    court_booking_check_again = get_court_bookings(3)
except ValueError :
    pass
else:
    assert False, "There are no bookings for this court"

print('  ')
print("Test 6")
print('-----------------------')

bookings_before = bookings.copy()
epm_cust=[{
    "customer": "",
    "court": 2,
    "start_time":"16:00",
    "duration": 45,

},
{
    "customer": " ",
    "court": 3,
    "start_time":"16:00",
    "duration": 30,

},
{
    "customer": "tilly",
    "court": 4,
    "start_time":"16:00",
    "duration": 30,

},
{
    "customer": "Jordan ",
    "court": 3,
    "start_time":"16:00",
    "duration": 0,

},
{
    "customer": "Mamba",
    "court": 3,
    "start_time":"16:00",
    "duration": 65,

},
{
    "customer": "Mark",
    "court": 3,
    "start_time":"16:00",
    "duration": -15,

}

]
for empcust in epm_cust:
    try:
        create_booking(
            empcust["customer"],
            empcust["court"],
            empcust["start_time"],
            empcust["duration"]
        )
    except ValueError:
        pass
    else:
        assert False, f"{empcust['customer']}'s booking was unexpectedly accepted"

    assert bookings == bookings_before, " a booking slipped through the cracks"

bookings_before = bookings.copy()
print('  ')
print("The Challenge")
print('-----------------------')
bookings_before = bookings.copy()
try:
    cancel_booking('Zara')
except ValueError:
    pass
else:
    assert False, " this customer has no booking"
assert bookings == bookings_before, " a booking slipped through the cracks"


print('  ')
print("Test 7")
print('-----------------------')


create_booking("James", 1, "15:00", 30)
print(bookings)
assert len(bookings) == 3, "no new bookings"
assert get_booking('James') ["customer"] == "James", "booking not found"
assert get_booking('Anaya') ["customer"] == "Anaya", "booking not found"

print("Test 8")
print('-----------------------')


create_booking("Mark", 1, "16:00", 30)
print(bookings)
assert len(bookings) == 4, "no new bookings"
assert get_booking('Mark') ["customer"] == "Mark", "booking not found"
assert get_booking('James') ["customer"] == "James", "booking not found"
assert get_booking('Anaya') ["customer"] == "Anaya", "booking not found"

print("Test 9")
print('-----------------------')


create_booking("Ella", 2, "14:30", 30)
print(bookings)
assert len(bookings) == 5, "no new bookings"
assert get_booking('Ella') ["customer"] == "Ella", "booking not found"
assert get_booking('Ella') ["court"] == 2, "booking not found"
assert get_booking('Anaya') ["court"] == 1, "booking not found"

print("Test 10")
print('-----------------------')

bookings_before = bookings.copy()
try:
    create_booking("derkek", 1, "25:00", 30)
except ValueError :
    pass
else:
    assert False, " invalid time  was unexpectedly accepted"
assert bookings == bookings_before, " a booking slipped through the cracks"

print(" ")
print("Test 11")
print('-----------------------')

create_booking("Joey", 3, "11:00", 30)
create_booking("Joey", 3, "11:30", 30)
bookings_before = bookings.copy()

customerbooking = get_customer_bookings("Joey")
print(customerbooking)
assert len(customerbooking) == 2, "could not find the bookings"
for customerrtn in customerbooking:
    assert customerrtn['customer'] == "Joey", "Something went wrong "

epmcustomerbooking = get_customer_bookings("nobody")
print(epmcustomerbooking)
assert len(epmcustomerbooking) == 0, "we found something"

assert bookings == bookings_before, " a booking slipped through the cracks"

print("Test 12")
print('-----------------------')


bookings_before = bookings.copy()

bookingbyduration = get_bookings_by_duration(30)
#print(bookingbyduration)
#print(bookings_before)
assert len(bookingbyduration) == 5, "could not find the bookings"
for customerrtn in bookingbyduration:
    assert customerrtn['duration'] == 30, "Something went wrong "

invalidduration = get_bookings_by_duration(90)
assert len(invalidduration) == 0, "we found something"
assert bookings == bookings_before, " a booking slipped through the cracks"
