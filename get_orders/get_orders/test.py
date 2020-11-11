import re

pattern = re.compile(r"\('下单时间：\\n(.*?) .*共(.*)条数据'\)")
line = '显示第1到第20条数据，共104条数据';



with open("info.txt", 'r', encoding="utf-8") as f:
    l = f.readline()
    print(l)
    m = pattern.match(l)
    print(m.group(0))
    print(m.group(1))
    print(m.group(2))
