import xlrd
import xlwt
import re


class ExcelReadWrite:

    def __init__(self):
        self.filename = "customer_information.xlsx"

    def read(self):
        workbook = xlrd.open_workbook(filename=self.filename)  # 打开文件
        sheet_obj = workbook.sheet_by_index(0)
        ncows = sheet_obj.nrows
        mail_list = sheet_obj.col_values(0, 0, ncows)

        return mail_list

    def write(self, info_list):
        # info_list = [("orders_num", "orders_date")]
        workbook = xlwt.Workbook()
        sheet_obj = workbook.add_sheet("information")
        for i in range(len(info_list)):
            sheet_obj.write(i, 0, info_list[i][0])
            sheet_obj.write(i, 1, info_list[i][1])
        workbook.save("info.xls")


if __name__ == '__main__':

    pattern = re.compile(r"\('下单时间：\\n(.*?) .*共(.*)条数据'\)")
    info_list = []

    with open("info.txt", 'r', encoding="utf-8") as f:
        for line in f.readlines():
            try:
                m = pattern.match(line)
                orders_date = m.group(1)
                orders_num = int(m.group(2))
            except Exception:
                orders_date = ""
                orders_num = 0
            info_list.append((orders_date, orders_num))

    excel_write = ExcelReadWrite().write(info_list)
