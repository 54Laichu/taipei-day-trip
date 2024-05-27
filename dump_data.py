import os
import json
import mysql.connector
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 建立資料庫連線
db = mysql.connector.connect(
    host=os.environ['DB_HOST'],
    user=os.environ['DB_USER'],
    password=os.environ['DB_PASSWORD'],
    database=os.environ['DB_NAME']
)
cursor = db.cursor()

# 如果還沒有 attractions table，就建立一個
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attractions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        category VARCHAR(255),
        description TEXT,
        address VARCHAR(255),
        transport TEXT,
        mrt VARCHAR(255),
        latitude FLOAT,
        longitude FLOAT,
        images TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    )
""")

# 讀取 JSON 檔案
with open("data/taipei-attractions.json", 'r', encoding='utf-8') as file:
    data = json.load(file)

for item in data['result']['results']:
    name = item['name']
    category = item['CAT']
    description = item['description']
    address = item['address']
    transport = item['direction']
    mrt = item['MRT']
    latitude = float(item['latitude'])
    longitude = float(item['longitude'])

    # 只收檔名是jpg 或 png 結尾的 URL
    images = item['file'].split('https')
    filtered_images = ['https' + img for img in images if img.lower().endswith(('.jpg', '.png'))]
    images_str = ','.join(filtered_images)

    # 插入資料到資料庫
    cursor.execute("""
        INSERT INTO attractions (name, category, description, address, transport, mrt, latitude, longitude, images)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (name, category, description, address, transport, mrt, latitude, longitude, images_str))

db.commit()
cursor.close()
db.close()
