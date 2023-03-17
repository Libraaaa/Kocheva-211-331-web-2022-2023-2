# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""
# new_list = []
# def convert_ranges_to_ip_list(addresses):
#     for address in addresses:
#         if address.find('-') == -1: 
#             new_list.append(address)
#         else:
#             count_point = address.count('.')
#             # print(count_point,' точки')
#             if count_point == 3:
#                 count_addresses = address[address.find('-')+1::]
#                 # print(count_addresses, 'колво')
#                 new_list.append(address)
#                 host = address[:address.find('-')].split('.')[-1]
#                 # print(host)
#                 for i in count_addresses:
#                     next_host = host + i
#                     print(host, i)
#                     # next_address = address.split('.')[0] + '.' + address.split('.')[1] + '.' + address.split('.')[3] + 
#             # else: 


# if __name__ == '__main__':
#     print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3']))



def convert_ranges_to_ip_list(ip_list):
    full_ip_list = []
    for ip in ip_list:
        octets = ip.split('.')
        if ip.find('-') != -1: 
            ip_start = 1
            ip_end = 1
            if len(octets) == 4:
                ip_range = octets[-1].split('-')
                ip_start = int(ip_range[0])
                ip_end = int(ip_range[-1])
            else:
                first_ip, second_ip = ip.split('-')
                ip_start = int(first_ip.split('.')[-1])
                ip_end = int(second_ip.split('.')[-1])
            for i in range(ip_start, ip_end + 1):
                full_ip_list.append('.'.join(octets[:3]) + '.' + str(i))
        else:
            full_ip_list.append(ip)
    return full_ip_list

if __name__ == '__main__':
    print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']))
