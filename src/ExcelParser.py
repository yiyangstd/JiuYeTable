import xlrd
import datetime

class ExcelParser():

    def __init__(self):
        super().__init__()
        self.shiye = 1104
        self.yiliao = 359.1
        self.shengyu = 4.42
        self.shangzhang = 1.66
        self.item = None

    def parserFile(self, filePath):
        file = xlrd.open_workbook(filePath)
        table = file.sheet_by_index(0)
        self.item = table.cell(0, 0).value
        startRow = 4
        data = []
        while table.cell(startRow, 0).value:
            rowData = {}
            rowData['name'] = table.cell(startRow, 1).value
            rowData['sex'] = table.cell(startRow, 2).value
            rowData['birthday'] = table.cell(startRow, 3).value
            rowData['age'] = table.cell(startRow, 4).value
            rowData['id'] = table.cell(startRow, 5).value
            rowData['month'] = table.cell(startRow, 6).value
            rowData['canbaotime'] = table.cell(startRow, 7).value
            rowData['cunse'] = table.cell(startRow, 8).value
            rowData['zhanghao'] = table.cell(startRow, 9).value
            rowData['bank'] = table.cell(startRow, 10).value
            startRow = startRow + 1
            data.append(rowData)
        return data

    def computData(self, filePath):
        inputData = self.parserFile(filePath)
        datas = []
        for person in inputData:
            data = []
            data.append(person['name'])
            data.append(person['sex'])
            data.append(person['id'])
            # 计算应该享受待遇月数
            monthAge = self.computeMonthAge(person['birthday'])
            month = 0
            if person['sex'] == '男':
                if 720 - monthAge > 24:
                    month = 24
                else:
                    month = int(720 - monthAge)
            else:
                if 600 - monthAge > 24:
                    month = 24
                else:
                    month = int(600 - monthAge)
            data.append(month)
            data.append(person['canbaotime'])
            data.append(self.computStartTime(person['canbaotime']))
            data.append(self.computeEndTime(self.computStartTime(person['canbaotime']), month))
            data.append(round(self.shiye * month, 2))
            data.append(round(self.yiliao * month, 2))
            data.append(round(self.shengyu * month, 2))
            data.append(round(self.shangzhang * month, 2))
            data.append(round(self.shiye * month + self.yiliao * month + self.shengyu * month + self.shangzhang * month, 2))
            data.append(person['cunse'])
            data.append(person['zhanghao'])
            data.append(person['bank'])
            datas.append(data)
        return datas



    # 计算月龄
    def computeMonthAge(self, birthDay):
        now_year = datetime.datetime.now().year
        now_month = datetime.datetime.now().month
        birth_year = int(str(birthDay)[:4])
        birth_month = int(str(birthDay)[4:6])
        return (now_year - birth_year) * 12 + (now_month - birth_month)

    # 根据参保时间获得发放时间
    def computStartTime(self, canbao):
        canbao_year = str(canbao)[:4]
        canbao_month = str(canbao)[5:]
        if int(canbao_month) == 12:
            return str(int(canbao_year) + 1) + '.' + '1'
        return canbao_year + '.' + str(int(canbao_month) + 1)

    def computeEndTime(self, startTime, month):
        start_year = str(startTime)[:4]
        start_month = str(startTime)[5:]
        end_year = int(start_year) + (int(start_month) + int(month) - 1) // 12
        end_month = (int(start_month) + int(month) - 1) % 12
        return str(end_year) + '.' + str(end_month)


if __name__ == '__main__':
    parser = ExcelParser()
    # parser.computData("d://通滩人民医院、消防站失业保险人员名单 2018 .xlsx")
    print(parser.computeEndTime('2017.04', 24))