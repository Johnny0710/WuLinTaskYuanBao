from os import getcwd
from sys import exit
from os.path import join
import configparser
import socket
from threading import Thread
import pymysql

# 创建socket对象
# SOCK_DGRAM    udp模式
from configs.globConfig import parse_data
from configs.yuanbao import get_task_wing_num

if __name__ == '__main__':
    print("怀旧剑舞专用任务获取元宝插件程序已启动")
    print("""
    　　　｜｜｜　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜｜｜　　　　　｜｜　　　　　｜｜　　　　　　　　　
    　　　　｜　｜｜｜｜｜｜｜｜　　　｜｜｜　｜｜｜｜｜｜｜｜　　　　　｜｜｜｜　　　　｜｜　　　　｜｜｜　　　　　　｜　　
    　　　　｜｜｜　　｜｜　　　　　　｜｜　　｜｜　　　　｜｜　　　　｜｜｜｜｜｜｜｜　｜　　　　｜｜｜｜｜｜｜｜｜｜｜｜　
    　　｜｜｜｜｜　｜｜｜　　　　　　｜｜　　｜｜　　　　｜｜　　　｜｜｜　　｜｜｜｜　｜　　　　｜｜｜　｜　｜　　｜｜　　
    　　｜｜｜｜｜　｜｜　｜　　　　　｜｜　　｜｜　　　　｜｜　　｜｜｜｜｜｜｜　　｜　｜　　　　　｜｜｜｜｜｜｜｜｜｜｜　
    　｜｜｜｜｜｜｜｜｜｜｜｜　　　　｜｜　　｜｜｜｜｜｜｜｜　　　｜　　｜　｜｜　｜　｜　　　　｜　｜　｜　｜　　｜　｜　
    　｜｜　｜　　｜｜｜　｜｜｜　　　｜｜　　｜｜　　　　｜｜　　　｜｜｜｜　｜｜　｜　｜　　　｜｜｜｜｜｜｜｜｜｜｜｜｜｜
    　　　　｜　｜｜　｜　｜｜｜　　　｜｜　　｜｜　　　　｜｜　　　｜｜　｜｜｜｜　｜　｜　　　　　｜｜｜｜｜｜｜｜｜｜｜　
    　　　　｜｜｜｜　｜　　｜｜　　　｜｜　　｜｜　　　　｜｜　　　　｜｜｜｜｜　　｜　｜　　　　｜｜｜｜｜｜｜　｜｜｜｜　
    　　　　｜｜｜　　｜　　　　　　　｜｜　　｜｜　　　　｜｜　　　　｜｜　｜｜｜｜｜　｜　　　　｜｜｜｜｜｜｜　｜　｜　　
    　　　　｜｜　　　｜　　　　　　　｜｜　　｜｜｜｜｜｜｜｜　　　｜｜｜｜｜｜｜｜　　｜　　　　　　｜｜｜｜｜｜｜｜｜｜　
    　　　｜｜｜　　　｜｜　　　　　　｜｜｜　｜｜　　　　｜｜　　　｜｜｜｜｜｜　　　｜｜　　　　｜｜｜｜　　　　｜｜　　　
    　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　｜｜　　　　｜｜　　　　　　｜｜　　　
    """)
    config = configparser.ConfigParser()
    local_path = getcwd()
    config_path = join(local_path, 'configs', 'configs.ini')
    config.read(config_path)
    print("正在检测服务器连通情况")
    check_clienk = socket.socket()
    check_clienk.settimeout(5)
    try:
        check_clienk.connect((config['Server']['SERVER_IP'], int(config['Server']['GAMEDBD_PORT'])))
    except ConnectionRefusedError as err:
        print("与服务器29400端口连通失败,该端口为获取角色账户ID使用,请检查")
        exit(0)
    else:
        print("与服务器29400端口连接成功")
        check_clienk.close()
    print("检测数据库连通状态")

    db_config = {
        'host': config['Mysql']['MYSQL_SERVER'],
        'port': int(config['Mysql']['MYSQL_PORT']),
        'user': config['Mysql']['MYSQL_USER'],
        'password': config['Mysql']['MYSQL_PASSWD'],
        'charset': 'utf8',
        'db': config['Mysql']['MYSQL_DATABASE'],
    }

    try:
        conn_obj = pymysql.connect(**db_config)
    except pymysql.err.OperationalError as err:
        print("与数据库连接失败,请检查环境")
        exit(0)
    else:
        print("与数据库连接成功")
        conn_obj.close()


    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_ip = config['Listen']['LOCALHOST']
    server_port = int(config['Listen']['LISTEN_PORT'])
    s.bind((server_ip, server_port))  # 绑定服务器的ip和端口
    print("监听{}:{}".format(server_ip, server_port))
    while 1:
        data = s.recv(65536)  # 一次接收1024字节
        _thread = Thread(target=parse_data, args=(data,))
        _thread.start()

