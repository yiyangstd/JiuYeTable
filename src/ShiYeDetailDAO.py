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
                           "item VARCHAR(20) , "
                           "stopFlag INT default 0,"
                           "shengyuFlag INT default 0,"
                           "shangzhangFlag INT default 0)")
            self.conn.commit()
            cursor.close()

    # 添加人员数据
    def add_person(self, name, sex, id, month, canbaoTime, fafangTime, endTime, shiye, yiliao, shengyu, shangzhang,
                   total, cunse, zhanghao, beizhu, item, stopFlag=0):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO shiye_detail"
                "(name, sex, id, month, canbaoTime, fafangTime, shiye, yiliao, shengyu, "
                "shangzhang, total, cunse, zhanghao, beizhu, item, endTime, stopFlag) "
                "VALUES('" + str(name) + "','" + str(sex) + "','" + id + "'," + str(month) + ",'" + str(canbaoTime) + "','" +
                str(fafangTime) + "','" + str(shiye) + "','" + str(yiliao) + "','" + str(shengyu) + "','" + str(shangzhang) + "','" + str(total) + "','" +
                cunse + "','" + zhanghao + "','" + beizhu + "','" + item + "','" + endTime + "','" + str(stopFlag) + "')")
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            self.conn.rollback()
            return False
        finally:
            cursor.close()

    # 根据id删除人员数据
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

    # 更新一个人员数据
    def update_person_by_id(self, id, newId, name = None, sex = None, month = None, canbaoTime = None, fafangTime = None,
               shiye = None, yiliao = None, shengyu = None, shangzhang = None, total = None, cunse = None,
               zhanghao = None, beizhu = None, item = None, endTime = None, stopFlag = None, shengyuFlag = None,
               shangzhangFlag = None):
        cursor = self.conn.cursor()
        updateSQL = "UPDATE shiye_detail SET "
        if name is not None:
            updateSQL = updateSQL + "name='" + name + "', "
        if sex is not None:
            updateSQL = updateSQL + "sex='" + sex + "', "
        if month is not None:
            updateSQL = updateSQL + "month=" + str(month) + ","
        if canbaoTime is not None:
            updateSQL = updateSQL + "canbaoTime='" + str(canbaoTime) + "',"
        if fafangTime is not None:
            updateSQL = updateSQL + "fafangTime='" + str(fafangTime) + "',"
        if shiye is not None:
            updateSQL = updateSQL + "shiye=" + str(shiye) + ","
        if yiliao is not None:
            updateSQL = updateSQL + "yiliao=" + str(yiliao) + ","
        if shengyu is not None:
            updateSQL = updateSQL + "shengyu=" + str(shengyu) + ","
        if shangzhang is not None:
            updateSQL = updateSQL + "shangzhang=" + str(shangzhang) + ","
        if total is not None:
            updateSQL = updateSQL + "total=" + str(total) + ","
        if cunse is not None:
            updateSQL = updateSQL + "cunse='" + cunse + "',"
        if zhanghao is not None:
            updateSQL = updateSQL + "zhanghao='" + zhanghao + "',"
        if beizhu is not None:
            updateSQL = updateSQL + "beizhu='" + beizhu + "',"
        if item is not None:
            updateSQL = updateSQL + "item='" + item + "',"
        if endTime is not None:
            updateSQL = updateSQL + "endTime='" + item + "',"
        if stopFlag is not None:
            updateSQL = updateSQL + "stopFlag=" + str(stopFlag) + ","
        if shangzhangFlag is not None:
            updateSQL = updateSQL + "shangzhangFlag=" + str(shangzhangFlag) + ","
        if shengyuFlag is not None:
            updateSQL = updateSQL + "shengyuFlag=" + str(shengyuFlag) + ", "
        updateSQL = updateSQL + "id = '" + newId + "' "
        updateSQL = updateSQL + "WHERE id ='" + id + "'"
        try:
            cursor.execute(updateSQL)
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

    # 根据id查询人员信息
    def find_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, sex, id, month, canbaoTime, fafangTime, shiye, yiliao, shengyu, "
                       "shangzhang, total, cunse, zhanghao, beizhu, item, endTime, stopFlag, shangzhangFlag,"
                       "shengyuFlag from shiye_detail where "
                       "id = '" + id + "'")
        result = cursor.fetchall()
        person = {}
        if result:
            onePerson = result[0]
            person['name'] = onePerson[0]
            person['sex'] = onePerson[1]
            person['id'] = onePerson[2]
            person['month'] = onePerson[3]
            person['canbaoTime'] = onePerson[4]
            person['fafangTime'] = onePerson[5]
            person['shiye'] = onePerson[6]
            person['yiliao'] = onePerson[7]
            person['shengyu'] = onePerson[8]
            person['shangzhang'] = onePerson[9]
            person['total'] = onePerson[10]
            person['cunse'] = onePerson[11]
            person['zhanghao'] = onePerson[12]
            person['beizhu'] = onePerson[13]
            person['item'] = onePerson[14]
            person['endTime'] = onePerson[15]
            person['stopFlag'] = onePerson[16]
            person['shangzhangFlag'] = onePerson[17]
            person['shengyuFlag'] = onePerson[18]
        cursor.close()
        return person

    # 查询所有的人员数据
    def find_persons(self, stopFlag = None):
        cursor = self.conn.cursor()
        findSql = "SELECT name, sex, id, month, canbaoTime, fafangTime, shiye, yiliao, shengyu," \
                  "shangzhang, total, cunse, zhanghao, beizhu, item, endTime, stopFlag, shangzhangFlag," \
                  " shengyuFlag from shiye_detail"

        if stopFlag:
            findSql = findSql + "where stopFlag=" + str(stopFlag)
        cursor.execute(findSql)
        result = cursor.fetchall()
        persons = []
        if result:
            for onePerson in result:
                person = {}
                person['name'] = onePerson[0]
                person['sex'] = onePerson[1]
                person['id'] = onePerson[2]
                person['month'] = onePerson[3]
                person['canbaoTime'] = onePerson[4]
                person['fafangTime'] = onePerson[5]
                person['shiye'] = onePerson[6]
                person['yiliao'] = onePerson[7]
                person['shengyu'] = onePerson[8]
                person['shangzhang'] = onePerson[9]
                person['total'] = onePerson[10]
                person['cunse'] = onePerson[11]
                person['zhanghao'] = onePerson[12]
                person['beizhu'] = onePerson[13]
                person['item'] = onePerson[14]
                person['endTime'] = onePerson[15]
                person['stopFlag'] = onePerson[16]
                person['shangzhangFlag'] = onePerson[17]
                person['shengyuFlag'] = onePerson[18]
                persons.append(person)
        return persons

def main():
    conn = sqlite3.connect('JiuYe.db')
    dao = ShiYeDetailDao(conn)
    dao.add_person('吴开文', '男', '510521196108236311', 24, '2018/2/1', '2018/3/1', '2018/12/1', 1104, 1104, 1104,
                   1104, 1104, '长河一组', '6214590482002637905', '信用社', '通滩人民医院消防站项目')
    dao.add_person('hahaha', '女', '510521196108236312', 24, '2018/2/1', '2018/3/1', '2018/12/1', 1104, 1104, 1104,
                   1104, 1104, '长河一组', '6214590482002637905', '信用社', '通滩人民医院消防站项目')
    print(dao.find_by_id("510521196108236311"))
    print(dao.find_persons())
    dao.update_person_by_id('510521196108236311', name='周杰伦', sex='男', cunse='台湾省')
    print(dao.find_persons())
    dao.delete_user('510521196108236312')
    print(dao.find_persons())




if __name__ == '__main__':
    main()

