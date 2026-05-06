import sqlite3
import os

class BaseDao:
    def __init__(self, db_path="db/database.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        # 增加 timeout 到 30 秒，应对并发
        return sqlite3.connect(self.db_path, timeout=30)

    def _init_db(self):
        """极致精简的表结构"""
        with self._get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            # 1. 身份档案表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS auth_profile (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    account TEXT, password TEXT, cookie TEXT, update_time DATETIME
                )
            """)

            # 2. 定价策略表 (现在包含：固定价、折扣、兜底价)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS price_strategies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    shop_id TEXT,
                    keyword TEXT,          -- 关键词
                    rule_value REAL,       -- 数值
                    rule_type TEXT,        -- 'fixed_price', 'discount', 'bottom_limit'
                    priority INTEGER DEFAULT 0
                )
            """)

            # 3. SKU 覆盖表 (特价)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sku_overrides (
                    product_id TEXT,
                    sku_id TEXT PRIMARY KEY,
                    shop_id TEXT,
                    special_price REAL,
                    update_time DATETIME
                )
            """)

            # 4. Webhook 配置表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS webhook_configs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    enabled INTEGER DEFAULT 1,
                    event_type TEXT DEFAULT 'all',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()