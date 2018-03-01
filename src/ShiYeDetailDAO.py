import sqlite3


class ShiYeDetailDao():

    def __init__(self, conn):
        self.conn = conn
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' and name='shiye_detail';")
        if not cursor.fetchall():
            cursor.execute("CREATE TABLE shiye_detail ("
                           "name VARCHAR(10), "
                           "sex VARCHAR(2), "
                           "id VARCHAR(20) primary key, "
                           "month INTEGER, "
                           "canbaoTime VARCHAR(10), "
                           "fafangTime VARCHAR(10), "
                           "endTime VARCHAR(10), "
                           "shiye FLOAT, "
                           "yiliao FLOAT, "
                           "shengyu FLOAT, "
                           "shangzhang FLOAT, "
                           "total FLOAT, "
                           "cunse VARCHAR(20), "
                           "zhanghao VARCHAR(50), "
                           "beizhu VARCHAR(30), "
                           "item VARCHAR(20) )")
            self.conn.commit()
            cursor.close()

    def add_person(self, name, sex, id, month, canbaoTime, fafangTime, endTime, shiye, yiliao, shengyu, shangzhang,
                   total, cunse, zhangbao, beizhu, item):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO shiye_detail"
                "(name, sex, id, month, canbaoTime, fafangTime, shiye, yiliao, shengyu, "
                "shangzhang, total, cunse, zhanghao, beizhu, item, endTime) "
                "VALUES('" + name + "','" + sex + "','" + id + "','" + id + "','" + month + "','" + canbaoTime + "','" +
                fafangTime + "','" + shiye + "','" + yiliao + "','" + shengyu + "','" + shangzhang + "','" + total + "','" +
                cunse + "','" + zhangbao + "','" + beizhu + "','" + item + "','" + endTime + "')")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    def delete_user(self, id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM shiye_detail WHERE id ='" + id + "'")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()
