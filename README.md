1.安装python
双击for-sissis\for_sissis\python-3.7.9.exe，安装python

2.安装依赖包
2.1在文件系统路径栏，输入cmd，打开命令行工具
![image](https://github.com/liuxin30/for-sissis/raw/feature/lx/for_sissis/images/Snipaste_2020-11-08_17-06-42.png)
![image](https://github.com/liuxin30/for-sissis/blob/feature/lx/for_sissis/images/Snipaste_2020-11-08_17-07-06.png)

2.2在命令行工具里输入pip install -r requirement.txt，点击回车，开始安装依赖包，结果里出现Successfully installed字样，表示安装成功
![image](https://github.com/liuxin30/for-sissis/blob/feature/lx/for_sissis/images/Snipaste_2020-11-08_17-08-53.png)

3.安装chormedriver
3.1 查看谷歌浏览器版本

![image](https://github.com/liuxin30/for-sissis/blob/feature/lx/for_sissis/images/Snipaste_2020-11-08_17-11-07.png)
![image](https://github.com/liuxin30/for-sissis/blob/feature/lx/for_sissis/images/Snipaste_2020-11-08_17-12-06.png)

在浏览器里输入http://chromedriver.storage.googleapis.com/index.html，根据上面查到的浏览器版本，下载相应的压缩包
![image](https://github.com/liuxin30/for-sissis/blob/feature/lx/for_sissis/images/Snipaste_2020-11-08_17-15-48.png)
![image](https://github.com/liuxin30/for-sissis/blob/feature/lx/for_sissis/images/Snipaste_2020-11-08_17-16-15.png)

4.把下载的chormedriver压缩包解压到for-sissis\for_sissis目录下，替换已有的chormedriver.exe

5.进入到for-sissis\for_sissis\whatsapp_plug\customer_file目录下，打开customer_info.xlsx表格，在第一列输入whatsapp联系人的备注名称，第二列输入客户名称。打开message.txt输入需要发送的文字，第一行不要修改。

6.进入到for-sissis\for_sissis\whatsapp_plug\whatsapp_plug目录下，双击whatsapp.py。在打开的浏览器页面扫描wahtsapp二维码，登录whatsapp，然后等待即可。
