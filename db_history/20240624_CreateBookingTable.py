import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_connect import get_db_connection

db = get_db_connection()
cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bookings (
        id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
        user_id INT NOT NULL,
        attraction_id INT NOT NULL,
        date TIMESTAMP NOT NULL,
        time ENUM('morning', 'afternoon') NOT NULL,
        price INT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (attraction_id) REFERENCES attractions(id)
    )
""")

db.commit()
cursor.close()
db.close()
