# -*- coding: utf-8 -*-
import os
import xlrd
import xlwt
from xlutils.copy import copy
import logging
import chardet


def read_excel(file_path, sheet_index=0, start_row=0, rows=None, start_col=0, cols=None):
    """
    读取表格文件
    :param file_path:    [str] 需要读取的文件路径
    :param sheet_index:  [int] 需要读取的sheet的序号
    :param start_row:    [int] 需要读取的起始行号
    :param rows:         [int] 需要读取的行数
    :param start_col:    [int] 需要读取的结束行号
    :param cols:         [int] 需要读取的列数
    :return: value_list  [list] 用户名称和邮箱对应的字典
    """
    workbook = xlrd.open_workbook(file_path)
    sheet_obj = workbook.sheet_by_index(sheet_index)
    if not rows:
        rows = sheet_obj.nrows
    if not cols:
        cols = sheet_obj.ncols
    value_list = list()
    for i in range(cols):
        value_list.append(sheet_obj.col_values(start_col+i, start_row, rows))
    if not isinstance(value_list, list):
        value_list = [value_list]
    return value_list


def get_excel_rows(file_path, sheet_index=0):
    """
    获取表格的行数
    :param file_path:    [str] 需要读取的文件路径
    :param sheet_index:  [int] 需要读取的sheet的序号
    :return: nrows:      [int] 表格的行数
    """
    workbook = xlrd.open_workbook(file_path)
    sheet_obj = workbook.sheet_by_index(sheet_index)
    return sheet_obj.nrows


def read_txt(file_path):
    """
    读取文本文件
    :param file_path:    [str] 需要读取的文件路径
    :return:
    """
    with open(file_path, 'rb') as f:
        out = f.read()
    str_code = chardet.detect(out)
    logging.info("文件：%s 的编码格式为：%s" % (file_path, str_code))
    ret = out.decode(str_code['encoding'])
    return ret


def get_file_path_list(file_dir, file_types):
    """
    获取指定类型的文件路径
    :param file_dir:     [str]  需要获取的文件目录
    :param file_types:   [list/str]  需要获取的文件类型
    :return:
    """
    if not isinstance(file_types, list):
        file_types = [file_types]
    file_path_list = list()
    print(os.listdir(file_dir))
    for file_name in os.listdir(file_dir):
        name, ext = os.path.splitext(file_name)
        print(name, ext)
        if ext[1:] in file_types:
            file_path_list.append(os.path.abspath(os.path.join(file_dir, file_name)))
    return file_path_list


def write_excel(file_path, content_list):
    """
    写入表格文件
    :param file_path:    [str] 需要读取的文件路径
    :param content_list: [list]  需要写入的内容，是一个元组列表
    :return:
    """
    workbook = xlwt.Workbook()
    sheet_obj = workbook.add_sheet(file_path)
    for i, value in enumerate(content_list):
        for j in range(len(value)):
            sheet_obj.write(i, j + 1, value)
    workbook.save(file_path)


def write_exist_excel(file_path, content_list, sheet_index=0, start_row=0, start_col=0):
    """
    写入已经存在的表格文件
    :param file_path:    [str] 需要读取的文件路径
    :param content_list: [list]  需要写入的内容，是一个元组列表
    :param sheet_index:  [int]  需要写入的sheet的序号
    :param start_row:    [int]  需要写入列号
    :param start_col:    [int]  需要写入列号
    :return:
    """
    wb = xlrd.open_workbook(file_path)
    workbook = copy(wb)
    sheet_obj = workbook.get_sheet(sheet_index)
    for i, value in enumerate(content_list):
        for j in range(len(value)):
            sheet_obj.write(start_row + i, start_col + j, value[j])
    workbook.save(file_path)


def write_txt(file_path, content, mode='w'):
    """
    写入文本文件
    :param file_path:    [str] 需要读取的文件路径
    :param content:      [str] 需要写入的内容
    :param mode:         [str] 写入方式
    :return:
    """
    if not isinstance(content, list):
        content = content.split('\n')
    with open(file_path, mode) as f:
        for item in content:
            f.write(str(item) + '\n')
