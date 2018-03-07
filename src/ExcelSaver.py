import xlwt

class ExcelSaver():

    @staticmethod
    def saveFile(filePath, headers, datas):
        workBook = xlwt.Workbook()
        sheet1 = workBook.add_sheet('导出结果')

        column = 0
        for header in headers:
            sheet1.write(0, column, header)
            column = column + 1

        row = 1
        for data in datas:
            column = 0
            for cell in data:
                sheet1.write(row, column, cell)
                column = column + 1
            row = row + 1

        workBook.save(filePath)