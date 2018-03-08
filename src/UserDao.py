import sqlite3


class UserDao:

    def __init__(self, conn):
        self.conn = conn
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='user';")
        if not cursor.fetchall():
            cursor.execute("CREATE TABLE user (name varchar(20) primary key, password varchar(20), role varchar(20))")
            cursor.execute("INSERT INTO user(name, password, role) values('admin', '3104794', 'admin')")
            self.conn.commit()

    # 新增用户
    def add_user(self, name, password, role):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO user(name, password, role) values('" + name + "','" + password + "','" + role + "')")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    # 删除用户
    def delete_user(self, name):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM user where name='" + name + "'")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    # 输入用户名，密码，判断是否合法
    def find_user(self, name, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, role FROM user WHERE name=\'" + name + "\' and password=\'" + password + "\';")
        pd = cursor.fetchall()
        cursor.close()
        user = {}
        if pd:
            user['name'] = pd[0][0]
            user['role'] = pd[0][1]
        return user

    # 列出所有的用户名和角色
    def find_all_user(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, role FROM user")
        result = cursor.fetchall()
        users = []
        for item in result:
            user = {"name": item[0], "role": item[1]}
            users.append(user)
        cursor.close()
        return users

    # 修改用户密码和角色
    def modify_user_password_role(self, name, password, role):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE user SET password='" + password + "',role='" + role + "' WHERE name='" + name + "'")
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

    #  修改用户密码
    def modify_user_password(self, name, oldpassword, newpassword):
        cursor = self.conn.cursor()
        try:
            result = cursor.execute("UPDATE user SET password='" + newpassword + "' WHERE name='" + name + "' and password='" + oldpassword + "'")
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

    # 修改用户角色
    def modify_user_role(self, name, role):
        cursor = self.conn.cursor()
        try:
            cursor.execute("UPDATE user SET role='" + role + "' WHERE name='" + name + "'")
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


def main():
    conn = sqlite3.connect('JiuYe.db')
    dao = UserDao(conn)
    dao.modify_user_role("yangyi", "kk")
    dao.delete_user("yangyi")
    print(dao.find_all_user())


if __name__ == '__main__':
    main()
