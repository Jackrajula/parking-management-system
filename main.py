import sqlite3
from datetime import datetime
import math

DATABASE = "parking.db"
TOTAL_SLOTS = 10
HOURLY_RATE = 100


def connect_database():
    return sqlite3.connect(DATABASE)


def create_tables():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number INTEGER UNIQUE NOT NULL,
            status TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_number TEXT UNIQUE NOT NULL,
            vehicle_type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_records (
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id INTEGER NOT NULL,
            slot_id INTEGER NOT NULL,
            entry_time TEXT NOT NULL,
            exit_time TEXT,
            duration_hours REAL,
            amount_paid REAL,
            status TEXT NOT NULL,
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
            FOREIGN KEY (slot_id) REFERENCES parking_slots(slot_id)
        )
    """)

    # Create parking slots only if they don't already exist
    cursor.execute("SELECT COUNT(*) FROM parking_slots")
    count = cursor.fetchone()[0]

    if count == 0:
        for slot_number in range(1, TOTAL_SLOTS + 1):
            cursor.execute(
                "INSERT INTO parking_slots (slot_number, status) VALUES (?, ?)",
                (slot_number, "Available")
            )

    connection.commit()
    connection.close()


def show_availability():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM parking_slots
        WHERE status = 'Available'
    """)

    available = cursor.fetchone()[0]

    print("\n================================")
    print("       PARKING AVAILABILITY")
    print("================================")
    print(f"Total parking slots: {TOTAL_SLOTS}")
    print(f"Available slots:     {available}")
    print(f"Occupied slots:      {TOTAL_SLOTS - available}")
    print("================================\n")

    connection.close()


def park_vehicle():
    registration = input("Enter vehicle registration number: ").strip().upper()
    vehicle_type = input("Enter vehicle type (Car/Motorcycle/etc.): ").strip()

    connection = connect_database()
    cursor = connection.cursor()

    # Check whether a slot is available
    cursor.execute("""
        SELECT slot_id, slot_number
        FROM parking_slots
        WHERE status = 'Available'
        ORDER BY slot_number
        LIMIT 1
    """)

    slot = cursor.fetchone()

    if slot is None:
        print("\nParking is FULL. No vehicle can enter.\n")
        connection.close()
        return

    # Check if the vehicle is already inside
    cursor.execute("""
        SELECT vehicle_id
        FROM vehicles
        WHERE registration_number = ?
    """, (registration,))

    vehicle = cursor.fetchone()

    if vehicle:
        vehicle_id = vehicle[0]

        cursor.execute("""
            SELECT record_id
            FROM parking_records
            WHERE vehicle_id = ? AND status = 'Parked'
        """, (vehicle_id,))

        active_record = cursor.fetchone()

        if active_record:
            print("\nThis vehicle is already parked.\n")
            connection.close()
            return

    else:
        cursor.execute("""
            INSERT INTO vehicles (registration_number, vehicle_type)
            VALUES (?, ?)
        """, (registration, vehicle_type))

        vehicle_id = cursor.lastrowid

    slot_id = slot[0]
    slot_number = slot[1]

    entry_time = datetime.now()

    # Mark slot as occupied
    cursor.execute("""
        UPDATE parking_slots
        SET status = 'Occupied'
        WHERE slot_id = ?
    """, (slot_id,))

    # Create parking record
    cursor.execute("""
        INSERT INTO parking_records
        (vehicle_id, slot_id, entry_time, status)
        VALUES (?, ?, ?, ?)
    """, (
        vehicle_id,
        slot_id,
        entry_time.isoformat(),
        "Parked"
    ))

    connection.commit()
    connection.close()

    print("\nVehicle successfully parked.")
    print(f"Registration: {registration}")
    print(f"Parking slot: {slot_number}")
    print(f"Entry time:   {entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def exit_vehicle():
    registration = input(
        "Enter vehicle registration number: "
    ).strip().upper()

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            parking_records.record_id,
            parking_records.slot_id,
            parking_records.entry_time,
            parking_slots.slot_number
        FROM parking_records
        JOIN vehicles
            ON parking_records.vehicle_id = vehicles.vehicle_id
        JOIN parking_slots
            ON parking_records.slot_id = parking_slots.slot_id
        WHERE vehicles.registration_number = ?
          AND parking_records.status = 'Parked'
    """, (registration,))

    record = cursor.fetchone()

    if record is None:
        print("\nVehicle not found in the parking system.\n")
        connection.close()
        return

    record_id = record[0]
    slot_id = record[1]
    entry_time = datetime.fromisoformat(record[2])
    slot_number = record[3]

    exit_time = datetime.now()

    duration_seconds = (
        exit_time - entry_time
    ).total_seconds()

    duration_hours = duration_seconds / 3600

    # Minimum charge is one hour
    charged_hours = max(1, math.ceil(duration_hours))

    amount = charged_hours * HOURLY_RATE

    # Update parking record
    cursor.execute("""
        UPDATE parking_records
        SET exit_time = ?,
            duration_hours = ?,
            amount_paid = ?,
            status = 'Completed'
        WHERE record_id = ?
    """, (
        exit_time.isoformat(),
        duration_hours,
        amount,
        record_id
    ))

    # Release parking slot
    cursor.execute("""
        UPDATE parking_slots
        SET status = 'Available'
        WHERE slot_id = ?
    """, (slot_id,))

    connection.commit()
    connection.close()

    print("\n================================")
    print("         PARKING RECEIPT")
    print("================================")
    print(f"Vehicle:          {registration}")
    print(f"Parking slot:     {slot_number}")
    print(f"Entry time:       {entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Exit time:        {exit_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time spent:       {duration_hours:.2f} hours")
    print(f"Charged hours:    {charged_hours}")
    print(f"Amount payable:   KES {amount:.2f}")
    print("================================\n")


def view_parked_vehicles():
    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            vehicles.registration_number,
            vehicles.vehicle_type,
            parking_slots.slot_number,
            parking_records.entry_time
        FROM parking_records
        JOIN vehicles
            ON parking_records.vehicle_id = vehicles.vehicle_id
        JOIN parking_slots
            ON parking_records.slot_id = parking_slots.slot_id
        WHERE parking_records.status = 'Parked'
        ORDER BY parking_slots.slot_number
    """)

    vehicles = cursor.fetchall()

    print("\n================================")
    print("        PARKED VEHICLES")
    print("================================")

    if not vehicles:
        print("No vehicles are currently parked.")
    else:
        for vehicle in vehicles:
            registration = vehicle[0]
            vehicle_type = vehicle[1]
            slot = vehicle[2]
            entry = datetime.fromisoformat(vehicle[3])

            print(
                f"Vehicle: {registration} | "
                f"Type: {vehicle_type} | "
                f"Slot: {slot} | "
                f"Entry: {entry.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    print("================================\n")

    connection.close()


def main():
    create_tables()

    while True:
        print("================================")
        print("      PARKING MANAGEMENT SYSTEM")
        print("================================")
        print("1. Check parking availability")
        print("2. Park vehicle")
        print("3. Exit vehicle")
        print("4. View parked vehicles")
        print("5. Exit system")
        print("================================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_availability()

        elif choice == "2":
            park_vehicle()

        elif choice == "3":
            exit_vehicle()

        elif choice == "4":
            view_parked_vehicles()

        elif choice == "5":
            print("\nThank you for using the Parking Management System.")
            break

        else:
            print("\nInvalid choice. Please select 1-5.\n")


if __name__ == "__main__":
    main()
