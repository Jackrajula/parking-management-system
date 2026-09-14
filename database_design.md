Database Design

The parking management system uses a relational SQLite database consisting of three main tables.

1. Parking Slots

Field| Data Type| Description
slot_id| INTEGER| Primary key
slot_number| INTEGER| Unique parking slot number
status| TEXT| Available or Occupied

2. Vehicles

Field| Data Type| Description
vehicle_id| INTEGER| Primary key
registration_number| TEXT| Unique vehicle registration
vehicle_type| TEXT| Type of vehicle

3. Parking Records

Field| Data Type| Description
record_id| INTEGER| Primary key
vehicle_id| INTEGER| Foreign key referencing Vehicles
slot_id| INTEGER| Foreign key referencing Parking Slots
entry_time| TEXT| Vehicle entry date and time
exit_time| TEXT| Vehicle exit date and time
duration_hours| REAL| Time spent in parking
amount_paid| REAL| Parking fee
status| TEXT| Parked or Completed

Relationships

A vehicle can have multiple parking records over time.

A parking slot can be associated with multiple parking records over time, although only one active parking record can occupy a slot at a given time.

The Parking Records table connects vehicles with parking slots and records each parking session.
