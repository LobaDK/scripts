import sqlite3


class oldquantumkatdb:
    class authenticated_servers:
        id: int
        server_id: int
        server_name: str
        authenticated_by_id: int
        authenticated_by_name: str
        is_authenticated: int

    class chat:
        id: int
        user_id: int
        user_name: str
        server_id: int
        server_name: str
        user_message: str
        assistant_message: str
        shared_chat: int


class newquantumkatdb:
    class authenticated_servers:
        id: int
        server_id: int
        authenticated_by_id: int
        requested_by_id: int
        is_authenticated: int

    class chat:
        id: int
        user_id: int
        server_id: int
        user_message: str
        assistant_message: str
        shared_chat: int

    class users:
        user_id: int
        user_name: str
        agreed_to_tos: int
        is_banned: int

    class servers:
        server_id: int
        server_name: str


def read_db(db: sqlite3.Connection, table_name: str):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()


old_db = sqlite3.connect("oldquantumkat.db")
new_db = sqlite3.connect("quantumkat.db")

old_db_tables = ["authenticated_servers", "chat"]
new_db_tables = ["authenticated_servers", "chat", "users", "servers"]
