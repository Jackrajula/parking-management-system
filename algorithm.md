Parking Management System Algorithm

Vehicle Entry Algorithm

1. Start the parking system.
2. Check the number of available parking slots.
3. If no slot is available, display "Parking Full" and reject the vehicle.
4. If a slot is available, request the vehicle registration number and vehicle type.
5. Check whether the vehicle is already parked.
6. If the vehicle is already parked, display an error message.
7. Otherwise, assign the first available parking slot.
8. Record the vehicle information.
9. Record the vehicle entry time.
10. Change the parking slot status from Available to Occupied.
11. Display the assigned parking slot.
12. End the entry operation.

Vehicle Exit Algorithm

1. Request the vehicle registration number.
2. Search for an active parking record belonging to the vehicle.
3. If the vehicle is not found, display "Vehicle not found".
4. If the vehicle is found, retrieve its entry time and assigned parking slot.
5. Record the current time as the exit time.
6. Calculate the parking duration.
7. Round the duration up to the next whole hour for billing purposes.
8. Multiply the charged hours by the hourly parking rate.
9. Record the exit time, duration and amount paid.
10. Change the parking record status to Completed.
11. Change the parking slot status from Occupied to Available.
12. Display the parking receipt and amount payable.
13. End the exit operation.

Availability Algorithm

1. Count all parking slots whose status is Available.
2. Display the number of available slots.
3. Display the number of occupied slots.
4. Return the availability information to the user.
