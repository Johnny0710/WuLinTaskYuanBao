import codecs
import socket
import configparser
from datetime import datetime


import pymysql
from configs.yuanbao import task_wing
from configs.tools import int_to_bit_set, parse_account_id

configs = configparser.ConfigParser()


def get_player_account_id(player_id):
    configs.read('configs/configs.ini')
    server_ip = configs['Server']['SERVER_IP']
    server_port = int(configs['Server']['GAMEDBD_PORT'])
    client = socket.socket()
    try:
        client.connect((server_ip, server_port))
    except Exception as err:
        print("【ERROR】[{}]:与服务器连接失败,请检查服务器是否开启\n".format(datetime.now()))
        with open('log.log', 'a+') as log:
            log.write("【ERROR】[{}]:与服务器连接失败,请检查服务器是否开启\n".format(datetime.now()))

    __send_tmp = [139, 197, 8, 128, 0, 0, 0]
    __send_tmp.extend(int_to_bit_set(int(player_id)))

    client.settimeout(2)
    client.send(bytes(__send_tmp))
    try:
        recv_data = client.recv(16384)

    except socket.timeout:
        print("【ERROR】[{}]:角色ID为:[{}]的玩家获取账号ID失败\n".format(datetime.now(), player_id))
        client.close()
        with open('log.log', 'a+') as log:
            log.write("【ERROR】[{}]:角色ID为:[{}]的玩家获取账号ID失败\n".format(datetime.now(), player_id))
    else:
        account_id = parse_account_id(recv_data)
        print("【INFO】[{}]:角色ID为:[{}]的玩家获取账号ID成功\n".format(datetime.now(), player_id))
        with open('log.log', 'a+') as log:
            log.write("【INFO】[{}]:角色ID为:[{}]的玩家获取账号ID[{}]成功\n".format(datetime.now(), player_id, account_id))
        return account_id


def pay(account_id, taskid):
    configs.read('configs/configs.ini')
    db_config = {
        'host': configs['Mysql']['MYSQL_SERVER'],
        'port': int(configs['Mysql']['MYSQL_PORT']),
        'user': configs['Mysql']['MYSQL_USER'],
        'password': configs['Mysql']['MYSQL_PASSWD'],
        'charset': 'utf8',
        'db': configs['Mysql']['MYSQL_DATABASE'],
    }
    conn_obj = pymysql.connect(**db_config)
    cur = conn_obj.cursor(cursor=pymysql.cursors.DictCursor)
    #    in userid1  INTEGER,
    #    in zoneid1  INTEGER,
    #    in sn1   INTEGER,
    #    in aid1    INTEGER,
    #    in point1     INTEGER,
    #    in cash1     INTEGER,
    #    in status1     INTEGER,
    #    out     error    INTEGER
    wing_num = int(task_wing.get(taskid))
    with open('log.log', 'a+') as log:
        print("【INFO】正在为账号ID:[{}]充值通过任务ID:[{}]获得的[{}]银元宝\n".format(account_id, taskid, wing_num))
        log.write("【INFO】正在为账号ID:[{}]充值通过任务ID:[{}]获得的[{}]银元宝\n".format(account_id, taskid, wing_num))
    cur.callproc('usecash', args=(account_id, int(configs['Mysql']['SERVER_ZONE_ID']), 0, 1, 0, wing_num, 1, 99))
    cur.execute(
        "select @_acquireuserpasswd_0,@_acquireuserpasswd_1,@_acquireuserpasswd_2,@_acquireuserpasswd_3,@_acquireuserpasswd_4,@_acquireuserpasswd_5,@_acquireuserpasswd_6,@_acquireuserpasswd_7")
    res1 = cur.fetchall()
    conn_obj.commit()
    cur.close()
    conn_obj.close()
    with open('log.log', 'a+') as log:
        print("【INFO】为账号ID:[{}]充值通过任务ID:[{}]获得的[{}]银元宝的操作已结束\n".format(account_id, taskid, wing_num))
        log.write("【INFO】为账号ID:[{}]充值通过任务ID:[{}]获得的[{}]银元宝的操作已结束\n".format(account_id, taskid, wing_num))


def parse_task_finish_data(task_data):
    __ = dict()
    task_list = task_data.split("gamed")[-2]
    task_list = task_list.split(":")[1:]

    for _tmp in task_list:
        __tmp = _tmp.split("=")
        __[__tmp[0].strip()] = __tmp[1].strip().split(",")[0]
    return __


def parse_data(data):
    try:
        __data_tmp = codecs.raw_unicode_escape_decode(data)[0]
        if "success" in __data_tmp:  # decode()解码收到的字节
            __parse_data_tmp = parse_task_finish_data(__data_tmp)
            if int(__parse_data_tmp['success']) == 1 and __parse_data_tmp['taskid'] in task_wing:
                account_id = get_player_account_id(int(__parse_data_tmp['roleid']))
                pay(account_id, __parse_data_tmp['taskid'])
    except Exception as err:
        with open('errlog.log', 'a+') as errlog:
            print("【ERROR】{}".format(errlog))
            errlog.write("【ERROR】{}".format(errlog))
