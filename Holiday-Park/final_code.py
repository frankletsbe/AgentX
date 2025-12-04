
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class Booking:
    def __init__(self, user, arrival_date, departure_date, room_type):
        self.user = user
        self.arrival_date = arrival_date
        self.departure_date = departure_date
        self.room_type = room_type

class Hotel:
    def __init__(self):
        self.bookings = []
        self.users = []

    def add_user(self, name, email):
        user = User(name, email)
        self.users.append(user)
        return user

    def add_booking(self, user, arrival_date, departure_date, room_type):
        booking = Booking(user, arrival_date, departure_date, room_type)
        self.bookings.append(booking)

    def display_bookings(self):
        for i, booking in enumerate(self.bookings):
            print(f"Booking {i+1}:")
            print(f"User: {booking.user.name}, {booking.user.email}")
            print(f"Arrival Date: {booking.arrival_date}")
            print(f"Departure Date: {booking.departure_date}")
            print(f"Room Type: {booking.room_type}")
            print()

def main():
    hotel = Hotel()
    user1 = hotel.add_user("John Doe", "john@example.com")
    hotel.add_booking(user1, "2024-01-01", "2024-01-03", "Single")
    hotel.add_booking(user1, "2024-01-05", "2024-01-07", "Double")
    hotel.display_bookings()

main()
