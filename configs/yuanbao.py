import os

task_wing = {
    "任务ID": "奖励的元宝数量",

}



with open("./configs/yuanbao.txt", "r") as file:
    data_list = file.read()

data_list = data_list.split("\n")
for data_lis in data_list:
    if '#' not in data_lis:
        __ = data_lis.split(',')
        task_wing[__[0]] = __[1]

