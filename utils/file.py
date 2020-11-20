# -*- coding: utf-8 -*-
import os
import xlrd
import xlwt
import logging
import chardet

class ReadFile(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self, sheet_index=0, col_num=0):
        """
        读取表格文件
        :param sheet_index:  [int] 需要读取的sheet的序号
        :param col_num:      [int] 需要读取的列号
        :return: value_list  [list] 用户名称和邮箱对应的字典
        """
        workbook = xlrd.open_workbook(self.file_path)
        sheet_obj = workbook.sheet_by_index(sheet_index)
        rows_num = sheet_obj.nrows
        value_list = sheet_obj.col_values(col_num, 1, rows_num)
        return value_list

    def read_txt(self):
        """
        读取文本文件
        :return:
        """
        with open(self.file_path, 'rb') as f:
            out = f.read()
        str_code = chardet.detect(out)
        logging.info("文件：%s 的编码格式为：%s" % (self.file_path, str_code))
        ret = out.decode(str_code['encoding'])
        return ret

class WriteFile(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def wtite_excel(self, content_list, col_num=0):
        """
        写入表格文件
        :param content_list: [list]
        :return:
        """
        workbook = xlwt.Workbook()
        sheet_obj = workbook.add_sheet("fail_list")
        for i, value in enumerate(content_list):
            sheet_obj.write(i, col_num, value)
        workbook.save("fail.xlsx")

    def write_txt(self, content):
        """
        写入文本文件
        :param content: [str] 需要写入的内容
        :return:
        """
        with open(self.file_path, 'w') as f:
            f.write(content)
