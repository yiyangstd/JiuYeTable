import sqlite3

class OperationLogDao():

    def __init__(self, conn):
        self.conn = conn
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='operation_log';")
        if not cursor.fetchall():
            cursor.execute("CREATE TABLE operation_log ("
                           "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "name VARCHAR(10),"
                           "time TIMESTAMP default (datetime('now', 'localtime')),"
                           "operation VARCHAR(100))")
            self.conn.commit()
            cursor.close()

    def addLog(self, name, operation):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT into operation_log(id, name, operation) "
                           "VALUES(null, '" + str(name) + "', '" + str(operation) + "')")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def findLog(self, name=None):
        sql = "SELECT id, name, time, operation FROM operation_log"
        if name:
            sql = sql + " WHERE name = '" + name + "'"
        cursor = self.conn.cursor()
        result = cursor.execute(sql)
        logs = []
        for item in result:
            logs.append({
                'id': item[0],
                'name': item[1],
                'time': item[2],
                'operation': item[3]
            })
        cursor.close()
        return logs
        

if __name__ == '__main__':
    conn = sqlite3.connect('JiuYe.db')
    operation = OperationLogDao(conn)
    operation.addLog("dtest", "testOpperation")
    print(operation.findLog())