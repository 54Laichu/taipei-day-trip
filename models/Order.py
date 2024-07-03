from pydantic import BaseModel
from typing import Optional
from db_connect import get_db_connection
import random
import string
from datetime import datetime

class Contact(BaseModel):
    name: str
    email: str
    phone: str

class Attraction(BaseModel):
    id: int
    name: str
    address: str
    image: str

class Trip(BaseModel):
    attraction: Attraction
    date: str
    time: str

class Order(BaseModel):
    price: int
    trip: Trip
    contact: Contact
    status: Optional[str] = 'unpaid'
    user_id: Optional[int] = None
    order_number: Optional[str] = None

    @staticmethod
    def create(order: 'Order'):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            current_date = datetime.now().strftime('%Y%m%d')
            order_number = f"TPEGO{random_part}{current_date}"

            cursor.execute("""
                INSERT INTO Orders (user_id, attraction_id, date, time, price, contact_name, contact_email, contact_phone, status, order_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                order.user_id,
                order.trip.attraction.id,
                order.trip.date,
                order.trip.time,
                order.price,
                order.contact.name,
                order.contact.email,
                order.contact.phone,
                order.status,
                order_number
            ))
            db.commit()
            return [cursor.lastrowid, order_number]
        except Exception as e:
            db.rollback()
            print(f"Order 建立失敗: {e}")
            return None
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def update_status(order_id: int, status: str):
        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute("""
                UPDATE Orders
                SET status = %s
                WHERE id = %s
            """, (status, order_id))
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Order 更新失敗: {e}")
        finally:
            cursor.close()
            db.close()

    @staticmethod
    def find_by_number(order_number: str):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT o.*, a.name as attraction_name, a.address as attraction_address, a.images as attraction_image
                FROM Orders o
                JOIN Attractions a ON o.attraction_id = a.id
                WHERE o.order_number = %s
            """, (order_number,))
            order_data = cursor.fetchone()
            if order_data:
                return Order(
                    price=order_data['price'],
                    trip=Trip(
                        attraction=Attraction(
                            id=order_data['attraction_id'],
                            name=order_data['attraction_name'],
                            address=order_data['attraction_address'],
                            image=order_data['attraction_image'].split(',')[0]
                        ),
                        date=order_data['date'].strftime('%Y-%m-%d'),
                        time=order_data['time']
                    ),
                    contact=Contact(
                        name=order_data['contact_name'],
                        email=order_data['contact_email'],
                        phone=order_data['contact_phone']
                    ),
                    status=order_data['status'],
                    user_id=order_data['user_id'],
                    order_number=order_data['order_number']
                )
            return None
        except Exception as e:
            print(f"Error finding order: {e}")
            return None
        finally:
            cursor.close()
            db.close()

    def to_dict(self):
        return {
            "number": self.order_number,
            "price": self.price,
            "trip": {
                "attraction": {
                    "id": self.trip.attraction.id,
                    "name": self.trip.attraction.name,
                    "address": self.trip.attraction.address,
                    "image": self.trip.attraction.image
                },
                "date": self.trip.date,
                "time": self.trip.time
            },
            "contact": {
                "name": self.contact.name,
                "email": self.contact.email,
                "phone": self.contact.phone
            },
            "status": self.status
        }
