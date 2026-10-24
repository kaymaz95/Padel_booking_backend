from booking import bookings, create_booking
import pytest
@pytest.fixture(autouse=True)
def clear_bookings():
    bookings.clear()

def test_create_booking():
    function_under_test = create_booking("Karl",1,"14:00",30)
    assert function_under_test["customer"] == "Karl"
    
def test_create_booking_returns_duration():
    function_under_test = create_booking("Karl", 1, "14:00", 30)
    assert function_under_test["duration"] == 30

def test_create_booking_is_confirmed():
    function_under_test = create_booking("Karl", 1, "14:00", 30)
    assert function_under_test["confirmed"] == True

def test_create_booking_rejects_invalid_duration():
    with pytest.raises(ValueError):
        create_booking("paul",1,"14:00",70)
    assert len(bookings) == 0

def test_create_booking_rejects_invalid_court():
    with pytest.raises(ValueError):
        create_booking("paul",4,"14:00",60)
    assert len(bookings) == 0

def test_create_booking_rejects_overlap():
    create_booking("Karl",1,"14:00",60)
    with pytest.raises(ValueError):
        create_booking("Sarah",1,"14:00",60)
    assert len(bookings) == 1
    assert bookings[0]["customer"] == "Karl"