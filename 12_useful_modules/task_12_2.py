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
new_list = []
def convert_ranges_to_ip_list(addresses):
    for address in addresses:
        if address.find('-') == -1: 
            new_list.append(address)
        else:
            count_point = address.count('.')
            if count_point == 3:
                count_addresses = address[address.find('-')+1::]
                new_list.append(address[:address.find('-')])
                host = int(address[:address.find('-')].split('.')[-1])
                network_address = address[:address.find('-')].split('.')[0] + '.' + address[:address.find('-')].split('.')[1] + '.' + address[:address.find('-')].split('.')[2] + '.' 
                for i in range(host, int(count_addresses)):
                    next_host = str(host + i)
                    next_address = network_address + next_host
                    new_list.append(next_address)
            else: 
                end_ip = address[address.find('-')+1::]
                new_list.append(address[:address.find('-')])
                host = int(address[:address.find('-')].split('.')[-1])
                network_address = address[:address.find('-')].split('.')[0] + '.' + address[:address.find('-')].split('.')[1] + '.' + address[:address.find('-')].split('.')[2] + '.' 
                for i in range(int(host+1), int(end_ip.split('.')[-1])+1):
                    next_host = str(i)
                    next_address = network_address + next_host
                    new_list.append(next_address)
    return new_list


if __name__ == '__main__':
    print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']))
