# -*- coding: utf-8 -*-
import os
import xlrd

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

from log import LOG

path =os.path.join(BASE_PATH, "customer_file")
image_path = os.path.join(BASE_PATH, "images")


class ReadFile:

    def __init__(self):
        pass
        self.customer_info = path + "\\customer_info.xlsx"
        LOG.info("customer-info file path: %s" % self.customer_info)
        self.meassge_tmp = path + "\\message.txt"
        LOG.info("meassge-tmp file path: %s" % self.meassge_tmp)

    def get_mail_name_dict(self):
        """
        获取客户邮箱和客户名称的字典
        :return:
        """
        LOG.info("get mail name dict...")
        workbook = xlrd.open_workbook(filename=self.customer_info)  # 打开文件
        sheet_obj = workbook.sheet_by_index(0)
        ncows = sheet_obj.nrows
        mail_list = sheet_obj.col_values(0, 1, ncows)
        name_list = sheet_obj.col_values(1, 1, ncows)
        mail_name_dict = dict()
        for i, mail in enumerate(mail_list):
            mail_name_dict[mail] = name_list[i]

        return mail_name_dict

    def get_message(self):
        """
        获取需要发送的消息模板
        :return:
        """
        LOG.info("get message...")
        with open(self.meassge_tmp, 'r') as f:
            message = f.read()
        return message

    def get_images(self):
        """
        读取图片
        :return:
        """
        image_list = list()
        for image_name in os.listdir(image_path):
            # if os.path.basename(image_name):
            (filename, extension) = os.path.splitext(image_name)
            if extension in [".jpg", ".png", ".jpeg"]:
                image_p = os.path.join(image_path, image_name)
                image_list.append(image_p)
                # with open(image_p, "rb") as f:

        return image_list


if __name__ == '__main__':
    rf = ReadFile()
    print(rf.get_mail_name_dict())
    print(rf.get_message())
    print(rf.get_images())
