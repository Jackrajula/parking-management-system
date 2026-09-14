Data Structures Used

1. Database Tables

Relational database tables are used to permanently store vehicles, parking slots and parking records.

2. Tuples

Python tuples are used to represent rows returned from SQLite queries. For example, a database query may return a tuple containing a slot ID and slot number.

3. Lists

Lists can be used when multiple records need to be temporarily stored and processed sequentially.

4. Dictionaries

Dictionaries can be used in an alternative in-memory implementation to associate a vehicle registration number with information about its parking session.

For example:

active_vehicles = {
    "KDA123A": {
        "slot": 1,
        "entry_time": "2026-09-14 08:00:00"
    }
}

This provides fast average-case lookup by vehicle registration number.

5. Database Indexes and Keys

Primary keys uniquely identify database records. Foreign keys establish relationships between tables.

The vehicle registration number is also defined as unique so that the same vehicle cannot be registered twice in the Vehicles table.
