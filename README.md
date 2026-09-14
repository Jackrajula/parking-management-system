# parking-management-system
A Python-based parking management system that tracks parking availability, vehicles, parking duration and parking fees.
Parking Management System

Introduction

The Parking Management System is a Python application designed to manage vehicle parking in a parking facility.

The system allows users to check parking availability before entry, register vehicles, assign parking slots, record entry and exit times, calculate parking duration and calculate the amount payable.

Features

- Check available parking slots
- Register vehicles
- Automatically assign available parking slots
- Prevent a vehicle from being parked twice
- Record vehicle entry time
- Record vehicle exit time
- Calculate parking duration
- Calculate parking charges
- Release parking slots after vehicle exit
- Display currently parked vehicles
- Store information using an SQLite database

Technologies Used

- Python
- SQLite
- Git
- GitHub

Parking Fee

The system uses a rate of KES 100 per charged hour.

The minimum charge is one hour.

How to Run

Run the following command in the terminal:

python3 main.py

System Workflow

Entry

Vehicle → Check availability → Assign slot → Record entry → Mark slot occupied

Exit

Vehicle → Find parking record → Calculate duration → Calculate fee → Release slot

Database

The system contains three main tables:

1. Parking Slots
2. Vehicles
3. Parking Records

Conclusion

The system provides a basic computerized solution for managing parking availability, vehicle records, parking duration and payment calculation.
