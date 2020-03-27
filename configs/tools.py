def int_to_bit_set(integer):

    int_hex = hex(integer)[2:]  # 将传入的整数转换为十六进制数据,切片取出需要的数据
    int_hex = int_hex.rjust(8, '0')  # 补全八位十六进制
    byte_int_list = [int(int_hex[x:x + 2], 16) for x in range(0, 8, 2)]
    return byte_int_list  # 将出来的数据返回


def parse_account_id(player_data):
    offset = 17
    human_num_length = player_data[offset:offset+1]
    offset += 22 + list(human_num_length)[0]
    config_data_length = list(player_data[offset:offset+1])[0]
    offset += 1
    if config_data_length == 128:
        config_data_length = list(player_data[offset:offset+1])[0]
        offset += 1
    elif config_data_length > 128:
        __tmp_length = (config_data_length-128) * 256
        config_data_length = __tmp_length + list(player_data[offset:offset+1])[0]
        offset += 1
    offset += config_data_length
    help_data_length = list(player_data[offset:offset+1])[0]
    offset += 1
    if help_data_length == 128:
        help_data_length = list(player_data[offset:offset+1])[0]
        offset += 1
    elif help_data_length > 128:
        __tmp_length = (help_data_length-128) * 256
        help_data_length = __tmp_length + list(player_data[offset:offset+1])[0]
        offset += 1
    offset += help_data_length + 9
    userid = int(player_data[offset:offset+4].hex(), 16)
    return userid









    #