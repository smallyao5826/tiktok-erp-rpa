from .base_dao import BaseDao
from datetime import datetime

class AuthDao(BaseDao):
    def save_profile(self, account, password, cookie):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO auth_profile (id, account, password, cookie, update_time)
                VALUES (1, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET 
                    account=excluded.account, password=excluded.password,
                    cookie=excluded.cookie, update_time=excluded.update_time
            """, (account, password, cookie, now))

    def get_profile(self):
        with self._get_connection() as conn:
            row = conn.execute("SELECT account, password, cookie FROM auth_profile WHERE id = 1").fetchone()
            return {"account": row[0], "password": row[1], "cookie": row[2]} if row else None