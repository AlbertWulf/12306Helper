# coding: utf-8 
"""Train tickets query from CLI.



Usage:

    tickets [-dgktz] <from> <to> <date>


Options:

    -h, --help    显示帮助菜单

    -d            动车

    -g            高铁

    -k            快速

    -t            特快

    -z            直达
Example:
     tickets 北京 上海 2018-01-13
     tickets -dg 成都 南京 2018-01-13

"""

import requests

from stations import stations

from datetime import datetime

import json

from docopt import docopt

from prettytable import PrettyTable

from colorama import Fore

from requests.packages.urllib3.exceptions import InsecureRequestWarning



requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



new_stations = {v : k for k,v in stations.items()}

def cli():
     """command-line interface"""
     arguments = docopt(__doc__)
     # python3 tickets.py -dg 合肥 天柱山 2018-01-13
     #{’-d':True,
     #'-g':True,
     #'-k':False,
     #'-t':False,
     #'-z':False,
     #'<date>':'2018-01-13',
     #'<from>':'合肥',
     #'<to>':'天柱山'}打印arguments得到一个字典
     #print(arguments)
     from_station = stations.get(arguments['<from>'])
     to_station = stations.get(arguments['<to>'])
     date = arguments['<date>']
     url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(date, from_station, to_station)
     
     info_list = get_train_info(url)
     print(','.join(info_list))
     


def get_train_info(url):
    info_list = []
    
    try:
            resp = requests.get(url,verify=False)
            raw_trains = resp.json()['date']['result']
            
            for raw_train in raw_trains:
                    data_list  = raw_train.split('|')
                    train_no = data_list[3]
                    #tart
                    from_station_code = data_list[6]
                    from_station_name = new_stations.get(from_station_code)
                    #end
                    to_station_code = data_list[7]
                    to_station_name = new_stations.get(to_station_code)
                    
                    start_time = data_list[8]
                    
                    arrive_time = data_list[9]
                    
                    time_fucked_up = data_list[10]
                    
                    first_class_seat = data_list[31] or'--'
                    
                    second_class_seat = data_list[30] or '--'
                    
                    soft_sleeper = data_list[23] or '--'
                    
                    hard_sleeper = data_list[28] or '--'
                    
                    hard_seat = data_list[29] or '--'
                    
                    no_seat = data_list[26] or '--'
                    
                    info = '车次：{}，出发站：{}，目的地：{}，出发时间：{}，到达时间：{}，历时：{}，一等座：{}，二等座：{}，软卧：{}，硬卧：{}，硬座：{}，无座：{}\n\n'.format(

			           train_no, from_station_name, to_station_name, start_time, arrive_time, time_fucked_up, first_class_seat,

				       second_class_seat, soft_sleeper, hard_sleeper, hard_seat, no_seat)

			         
                    info_list.append(info)
                      
            return info_list
    except:
            return '请再次输入！！'
            
if __name__ == '__main__':
    cli()
            

 
     
    