import sqlite3


class UserDao:

    def __init__(self, conn):
        self.conn = conn


    #输入用户名，密码，判断是否合法
    def find_user(self, name, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='user';")
        if cursor.fetchall():
            cursor.execute("SELECT name, role FROM user WHERE name=\'" + name + "\' and password=\'" + password + "\';")
            pd = cursor.fetchall()
            cursor.close()
            user = {}
            if pd:
                user['name'] = pd[0][0]
                user['role'] = pd[0][1]
            return user
        else:
            cursor.execute("CREATE TABLE user (name varchar(20) primary key, password varchar(20), role varchar(20))")
            cursor.execute("INSERT INTO user(name, password, role) values(\'admin\', \'3104794\', \'admin\')")
            self.conn.commit()
            return self.find_user(name, password)
        cursor.close()



def main():
    conn = sqlite3.connect('JiuYe.db')
    dao = UserDao(conn)
    print(dao.find_user('admin', '3104794'))


if __name__ == '__main__':
    main()