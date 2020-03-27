from os import getcwd
from os.path import join
import configparser
import socket
from threading import Thread

# 创建socket对象
# SOCK_DGRAM    udp模式
from configs.globConfig import parse_data

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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    config = configparser.ConfigParser()
    local_path = getcwd()
    config_path = join(local_path, 'configs', 'configs.ini')
    config.read(config_path)

    server_ip = config['Listen']['LOCALHOST']
    server_port = int(config['Listen']['LISTEN_PORT'])
    s.bind((server_ip, server_port))  # 绑定服务器的ip和端口
    print("监听{}:{}".format(server_ip, server_port))
    while 1:
        data = s.recv(65536)  # 一次接收1024字节
        _thread = Thread(target=parse_data, args=(data,))
        _thread.start()

