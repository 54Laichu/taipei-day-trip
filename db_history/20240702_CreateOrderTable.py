import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_connect import get_db_connection

db = get_db_connection()
cursor = db.cursor()

try:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
            user_id INT NOT NULL,
            attraction_id INT NOT NULL,
            date DATE NOT NULL,
            time ENUM('morning', 'afternoon') NOT NULL,
            price INT NOT NULL,
            contact_name VARCHAR(100) NOT NULL,
            contact_email VARCHAR(100) NOT NULL,
            contact_phone VARCHAR(20) NOT NULL,
            status ENUM('unpaid', 'paid') NOT NULL DEFAULT 'unpaid',
            order_number VARCHAR(50) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (attraction_id) REFERENCES Attractions(id)
        )
    """)
    db.commit()
    print("Orders table created successfully")
except Exception as e:
    print(f"Error creating Orders table: {e}")
    db.rollback()
finally:
    cursor.close()
    db.close()
