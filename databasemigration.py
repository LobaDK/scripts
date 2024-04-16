import sqlite3
from pydantic import BaseModel


class oldquantumkatdb:
    class authenticated_servers(BaseModel):
        id: int
        server_id: int
        server_name: str
        authenticated_by_id: int
        authenticated_by_name: str
        is_authenticated: int

    class chat(BaseModel):
        id: int
        user_id: int
        user_name: str
        server_id: int
        server_name: str
        user_message: str
        assistant_message: str
        shared_chat: int


class newquantumkatdb:
    class authenticated_servers(BaseModel):
        id: int
        server_id: int
        authenticated_by_id: int
        requested_by_id: int
        is_authenticated: int

    class chat(BaseModel):
        id: int
        user_id: int
        server_id: int
        user_message: str
        assistant_message: str
        shared_chat: int

    class users(BaseModel):
        user_id: int
        user_name: str
        agreed_to_tos: int
        is_banned: int

    class servers(BaseModel):
        server_id: int
        server_name: str


def read_db(db: sqlite3.Connection, table_name: str):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    return cursor.fetchall()


old_db = sqlite3.connect("./../oldquantumkat.db")
new_db = sqlite3.connect("./../quantumkat.db")

old_db_tables = ["authenticated_servers", "chat"]
new_db_tables = ["authenticated_servers", "chat", "users", "servers"]

for table in old_db_tables:
    old_data = read_db(old_db, table)
    new_data = []
    for row in old_data:
        if table == "authenticated_servers":
            new_data.append(
                newquantumkatdb.authenticated_servers(
                    id=row[0],
                    server_id=row[1],
                    authenticated_by_id=row[3],
                    requested_by_id=row[3],
                    is_authenticated=row[5],
                )
            )
        elif table == "chat":
            new_data.append(
                newquantumkatdb.chat(
                    id=row[0],
                    user_id=row[1],
                    server_id=row[3],
                    user_message=row[5],
                    assistant_message=row[6],
                    shared_chat=row[7],
                )
            )

    cursor = new_db.cursor()
    cursor.execute(f"DELETE FROM {table}")
    for row in new_data:
        cursor.execute(
            f"INSERT INTO {table} ({','.join(row.dict().keys())}) VALUES ({','.join(['?'] * len(row.dict().keys()))})",
            list(row.dict().values()),
        )
    new_db.commit()
