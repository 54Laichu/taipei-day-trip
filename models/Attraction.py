from db_connect import get_db_connection

class Attraction:
    @staticmethod
    def all(page, keyword):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM attractions"
        params = []

        if keyword:
            query += " WHERE name LIKE %s OR mrt = %s"
            keyword_param = f"%{keyword}%"
            params.extend([keyword_param, keyword])

        query += " LIMIT %s OFFSET %s"
        limit = 12
        offset = page * limit
        params.extend([limit, offset])

        cursor.execute(query, tuple(params))
        attractions = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) as total FROM attractions")
        total_records = cursor.fetchone()["total"]
        total_pages = (total_records + limit - 1) // limit
        next_page = page + 1 if len(attractions) == limit and page + 1 < total_pages else None

        cursor.close()
        db.close()

        return {
            "nextPage": next_page,
            "data": attractions
        }

    @staticmethod
    def find(attraction_id):
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM attractions WHERE id = %s", (attraction_id,))
        attraction = cursor.fetchone()
        cursor.close()
        db.close()

        if attraction:
            attraction['images'] = attraction['images'].split(',')
        return attraction

    @staticmethod
    def get_mrt_list():
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
        SELECT mrt
        FROM attractions
        GROUP BY mrt
        ORDER BY COUNT(*) DESC
        """)
        mrt_tuple = cursor.fetchall()
        cursor.close()
        db.close()

        mrt_list = [mrt[0] for mrt in mrt_tuple if mrt[0] is not None]
        return mrt_list
