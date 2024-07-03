import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_connect import get_db_connection

db = get_db_connection()
cursor = db.cursor()

try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Payments (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            order_id INT NOT NULL,
            status INT NOT NULL DEFAULT 1,
            transaction_time_millis BIGINT NOT NULL,
            msg VARCHAR(100) NOT NULL,
            amount INT NOT NULL,
            currency VARCHAR(20) NOT NULL,
            rec_trade_id VARCHAR(50) NOT NULL,
            bank_transaction_id VARCHAR(50) NOT NULL,
            last_four INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES Orders(id)
        )
    """)
    db.commit()
    print("Payments table created successfully")
except Exception as e:
    print(f"Error creating Payments table: {e}")
    db.rollback()
finally:
    cursor.close()
    db.close()
