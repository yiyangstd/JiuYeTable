import sqlite3

class TableDao:

    def __init__(self):
        self.conn = sqlite3.connect('JiuYe.db')

    def __del__(self):
        if self.conn:
            self.conn.close()

    ##输入用户名，密码，判断是否合法
    def find_user(self, name, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='user';")
        if cursor.fetchall():
            cursor.execute("SELECT password FROM user WHERE name='" + name + "';")
            pd = cursor.fetchall()
            cursor.close()
            if pd:
                if pd[0].count(password) >= 1:
                    return True
                else:
                    return False
            return False
        else:
            cursor.execute("CREATE TABLE user (name varchar(20) primary key, password varchar(20))")
            cursor.execute("INSERT INTO user(name, password) values(\'admin\', \'3104794\')")
            self.conn.commit()
            print('Table Added and User inserted')
            self.findUser(name)
        cursor.close()



def main():
    dao = TableDao()
    print(dao.find_user('admin', '310d4794'))


if __name__ == '__main__':
    main()