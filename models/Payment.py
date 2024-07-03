from pydantic import BaseModel
from db_connect import get_db_connection

class Payment(BaseModel):
    order_id: int
    status: int
    transaction_time_millis: int
    msg: str
    amount: int
    currency: str
    rec_trade_id: str
    bank_transaction_id: str
    last_four: int

    @staticmethod
    def create(payment: 'Payment'):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                INSERT INTO Payments (order_id, status, transaction_time_millis, msg, amount, currency, rec_trade_id, bank_transaction_id, last_four)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                payment.order_id,
                payment.status,
                payment.transaction_time_millis,
                payment.msg,
                payment.amount,
                payment.currency,
                payment.rec_trade_id,
                payment.bank_transaction_id,
                payment.last_four
            ))
            db.commit()
            return cursor.lastrowid
        except Exception as e:
            db.rollback()
            print(f"Payment 建立失敗: {e}")
            return None
        finally:
            cursor.close()
            db.close()
