# Python Padel Booking Core

A small Python learning project for creating, finding and cancelling padel court bookings. It combines in-memory booking rules with executable acceptance checks, with an initial FastAPI health endpoint. Booking operations remain Python functions; HTTP booking routes and persistent storage are not implemented yet.

## Run the acceptance checks

Requires Python 3. No third-party packages are needed; the booking module uses the standard-library `datetime` module.

Keep these files together under their original project names:

- `booking.py` — booking functions and in-memory state.
- `acceptance_check.py` — sequential acceptance checks.
- `main.py` — older practice script; currently not compatible with the updated function signature.

If downloaded filenames contain a suffix such as `(1)`, rename them to the names above. The acceptance script imports `booking`, so the module must be named `booking.py`.

From the project directory, run:

```bash
python3 acceptance_check.py
```

The script prints test labels and booking data. Success means it returns to the terminal prompt without an exception, with exit status 0. A failed assertion or unexpected exception stops execution and prints a traceback. Run in a fresh Python process each time: checks share state and depend on their order. Do not use Python's `-O` option, which disables assertions.

## Run the initial API

From the repository directory (Python 3.13.2 was used for the first local run):

```bash
python3 -m venv .venv
.venv/bin/python -m pip install "fastapi[standard]==0.150.0"
.venv/bin/python -m uvicorn api:app --reload
```

Create the environment once; reuse it on later sessions. The explicit interpreter path avoids accidentally using a global Python command. Stop the development server with Ctrl+C.

Open http://127.0.0.1:8000/health. The endpoint returns:

```json
{"status": "ok", "service": "padel-booking"}
```

`@app.get("/health")` registers the function below it for GET requests to that path. Renaming the Python function does not change the registered URL. This endpoint only proves that the application responds; it does not check dependencies or booking correctness. The development server is for local use.

The first local demonstration used FastAPI 0.150.0. A full dependency lock and automated API tests have not yet been added. `.gitignore` excludes the local virtual environment and Python caches.

## Booking functions

| Function | Behaviour |
|---|---|
| `create_booking(customer, court, start_time, duration)` | Validates the request, rejects same-court overlaps, appends a valid booking and returns its dictionary. |
| `get_booking(customer)` | Returns the first booking matching the exact customer name; raises `ValueError` if none exists. |
| `get_customer_bookings(customer)` | Returns a list of all exact-name matches, or `[]` if there are none. |
| `get_bookings_by_duration(duration)` | Returns all bookings with the exact duration, or `[]` if there are none. |
| `get_court_bookings(court)` | Returns a list of bookings for the court; raises `ValueError` if there are none. |
| `cancel_booking(customer)` | Removes and returns the first exact-name match; raises `ValueError` if none exists. |

The retrieval functions do not themselves change the stored list.

## Booking rules and data

For intended inputs, customer is a string, court is an integer from 1 to 3, start time is a 24-hour time string such as `"14:30"`, and duration is an integer from 1 to 60 minutes.

- Empty and whitespace-only customer names are rejected. Names are stored as supplied and matched exactly, including case and surrounding spaces.
- Court values outside 1–3 and durations outside 1–60 are rejected.
- `datetime.strptime(start_time, "%H:%M")` parses the start time and raises `ValueError` for invalid values such as `"25:00"`.
- The end time is calculated by adding the duration in minutes.
- Bookings overlap only if they use the same court and satisfy both comparisons below.

```python
start_time < existing_end and existing_start < end_time
```

A booking ending at 15:00 and another starting at 15:00 are allowed on the same court. Overlapping bookings on different courts are also allowed.

Each stored dictionary contains `customer`, `court`, `start_time`, `end_time`, `duration` and `confirmed`. Start and end times are `datetime` objects; duration remains a number of minutes. Newly created bookings have `confirmed=True`. Cancellation removes the dictionary rather than setting `confirmed=False`.

Validation, parsing and conflict checks happen before `bookings.append()`, so those rejected requests do not add a booking. An exception does not automatically undo a mutation that has already occurred.

## Acceptance coverage

| Section | Scenario checked |
|---|---|
| 1 | Create and retrieve two bookings. |
| 2 | Cancel a booking, verify it is no longer retrievable and retain the other customer. |
| 3 | Create a booking after cancellation. |
| 4 | Reject a same-court overlap and preserve existing bookings. |
| 5 | Retrieve bookings for a court and reject a lookup with no results. |
| 6 | Reject empty/whitespace names, court 4, and durations 0, 65 and -15 without changing state. |
| Cancellation challenge | Reject cancellation for an unknown customer without changing state. |
| 7 | Accept a booking immediately after an existing same-court booking. |
| 8 | Accept a later same-court booking with a gap. |
| 9 | Accept overlapping times on different courts and check their court assignments. |
| 10 | Reject `"25:00"` without changing state. |
| 11 | Return two bookings for Joey, check every result's customer name, return an empty list for an unknown name and preserve state during retrieval. |
| 12 | Return five 30-minute bookings, check every result's duration, return an empty list for duration 90 and preserve state during retrieval. |

Negative checks use `try` / `except ValueError` / `else` so unexpectedly accepted requests fail. Selected checks compare the current list with a snapshot made using `bookings.copy()`. This shallow copy detects additions and removals but does not independently copy the booking dictionaries or detect every possible in-place edit.

The checks cover these scenarios; they do not establish exhaustive correctness or production readiness.

## Current limitations

- All bookings live in a module-level list. They are lost when the Python process stops; a fresh process starts with an empty list.
- No booking dates are accepted. Parsing a time supplies the default date of 1 January 1900. Date-based scheduling and reliable cross-midnight conflict handling are not implemented.
- Customer names are not unique booking identifiers. A customer may have multiple bookings, but single-booking lookup and cancellation act on the first matching name.
- Input types are not explicitly enforced. Wrong types can cause exceptions other than `ValueError`, and numeric range checks do not enforce whole-number courts or durations.
- Returned dictionaries refer to the stored booking objects, and the global list is directly accessible. Callers can bypass validation by changing them.
- There is no database, booking HTTP API, user interface, authentication or concurrency protection. The initial HTTP endpoint is GET /health only.
- `main.py` still contains three-argument calls and requests without start times. It raises `TypeError` with the current booking module. Use the acceptance script to run the verified workflow.

## Learning and next steps

The project exercises functions, lists and dictionaries, loops, return placement, exceptions, time arithmetic, conflict detection and state-based assertions. It was developed with AI-assisted teaching and review; the customer-booking retrieval exercise also used guidance. Karl independently implemented the duration lookup and its acceptance checks, then corrected a test-variable mistake identified during review.

The FastAPI service is in progress: GET /health has been demonstrated locally. Next is a booking retrieval endpoint using the existing domain functions, followed by request validation, booking error mapping and pytest coverage. Those capabilities are not implemented yet.
