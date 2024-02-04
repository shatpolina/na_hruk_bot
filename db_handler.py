import sqlite3


class Database(object):
    def __init__(self, db: str):
        self.__connection = sqlite3.connect(db)
        self.cursor = self.__connection.cursor()

        self.create_basic_table()

    def __enter__(self):
        return self

    def __exit__(self, exc_value):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.__connection.rollback()
        else:
            self.__connection.commit()
        self.__connection.close()

    def execute(self, sql: str, data: str = None):
        if data:
            return self.cursor.execute(sql, data)
        else:
            return self.cursor.execute(sql)

    def select_random_gif(self):
        sql = "SELECT file_id FROM gifs WHERE rowid > (ABS(RANDOM()) % (SELECT max(rowid) FROM gifs)) LIMIT 1"
        return self.execute(sql).fetchone()[0]
        

    def insert(self, file_id: str, file_unique_id: str) -> bool:
        sql = '''
        INSERT INTO Gifs (file_id, file_unique_id) VALUES (?, ?)
        '''
        try:
            self.execute(sql, (file_id, file_unique_id))
            print('SUCCESSFUL INSERT')
            return True
        except Exception as e:
            print(e)
            return False

    def create_basic_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS gifs (
        id INTEGER PRIMARY KEY,
        file_id TEXT NOT NULL,
        file_unique_id TEXT NOT NULL,
        UNIQUE(file_unique_id)
        )
        ''')
    
    def delete(self, id: str):
        self.execute('DELETE FROM gifs WHERE file_unique_id=?', [id])
