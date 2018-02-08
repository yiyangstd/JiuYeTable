import sqlite3

class TableDao:

    def __init__(self):
        self.conn = sqlite3.connect('JiuYe.db')

    def __del__(self):
        if self.conn:
            self.conn.close()

    def findUser(self, name):
