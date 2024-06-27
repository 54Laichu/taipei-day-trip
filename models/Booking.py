from pydantic import BaseModel
from typing import Optional
import datetime
from fastapi.responses import JSONResponse
from db_connect import get_db_connection

class Booking(BaseModel):
    user_id: Optional[int] = None
    attractionId: int
    date: datetime.date
    time: str  # enum morning or afternoon
    price: int

    @staticmethod
    def create(booking: 'Booking'):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                INSERT INTO Bookings (user_id, attraction_id, date, time, price)
                VALUES (%s, %s, %s, %s, %s)""",
                (booking.user_id, booking.attractionId, booking.date, booking.time, booking.price))

            db.commit()
            return "Booking created!"
        except Exception as e:
            db.rollback()
            return str(e)
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def find(user_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute(("""
                SELECT Attractions.id, Attractions.name, Attractions.address, Attractions.images, Bookings.date, Bookings.time, Bookings.price
                FROM Bookings
                INNER JOIN Attractions ON Attractions.id = Bookings.attraction_id
                WHERE Bookings.user_id = %s
                """), (user_id,))
            booking_data = cursor.fetchone()
            if booking_data:
                return_data = {
                    'attraction': {
                        'id': booking_data['id'],
                        'name': booking_data['name'],
                        'address': booking_data['address'],
                        'image': booking_data['images'].split(',')[0]
                    },
                    'date': booking_data['date'].strftime('%Y-%m-%d'),
                    'time': booking_data['time'],
                    'price': booking_data['price']
                }
                return return_data
            else:
                return None
        except Exception as e:
            db.rollback()
            return str(e)
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def destroy(user_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute(("DELETE FROM Bookings WHERE user_id = %s"), (user_id,))
            db.commit()
            if cursor.rowcount == 0:
                return "No data affected"
            return "Booking canceled!"
        except Exception as e:
            db.rollback()
            return str(e)
        finally:
            cursor.close()
            db.close()

