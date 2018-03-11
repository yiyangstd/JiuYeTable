import sqlite3

class ParamDao:

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='param';")
        if not cursor.fetchall():
            cursor.execute("CREATE TABLE param (key VARCHAR(20) primary key, value VARCHAR(50))")
            cursor.execute("INSERT INTO param(key, value) VALUES ('shiye', '1104')")
            cursor.execute("INSERT INTO param(key, value) VALUES ('yiliao', '359.1')")
            cursor.execute("INSERT INTO param(key, value) VALUES ('shengyu', '4.42')")
            cursor.execute("INSERT INTO param(key, value) VALUES ('shangzhang', '1.66')")
            self.conn.commit()
        cursor.close()

    def getValueByKey(self, key):
        cursor = self.conn.cursor()
        cursor.execute("SELECT value FROM param WHERE key = '" + key + "';")
        if cursor.fetchone:
            return cursor.fetchone()[0]
        return None

    def insert(self, key, value):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO param(key, value) VALUES('" + str(key) + "', '" + str(value) + "')")
        self.conn.commit()
        if self.conn.total_changes > 0:
            return True
        return False

    def update(self, key, value):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE param SET value='" + str(value) + "' WHERE key='" + str(key) + "';")
            self.conn.commit()
            if self.conn.total_changes > 0:
                return True
            return False
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()


if __name__ == '__main__':
    conn = sqlite3.connect('JiuYe.db')
    paramDao = ParamDao(conn)
    paramDao.insert('test', 123.0)
    print(paramDao.getValueByKey('test'))
    paramDao.update('test', 221.0)
    print(paramDao.getValueByKey('test'))