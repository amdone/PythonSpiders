import platform
import sys
import shelve
from contextlib import closing

redstr = "\033[1;31;40m{}\033[0m"
uploadToCloud = True
path = ''
default_down_dir = '/home/share/abd/'
url_syntax = 'https://www.acfun.cn/v/{}'
# firstArgeement = sys.argv[1]
IsAcno = True
ac_no = ''
acer_no = ''
m3u8_full_url = ''
title = ''
ac_data = {}
# config_path = '/home/configs/acfun/acfun_data.json'
db_path = '/home/configs/acfun/acfun_data'
db_dir = '/home/configs/acfun'
wdb_path = './ac_data'
wdb_dir = './ac_data'

if platform.system() == 'Windows':
    db_path = wdb_path
    db_dir = wdb_dir
    print(db_path)
    pass
elif platform.system() == 'Linux':
    pass
else:
    print('Your system is not supported!!!')
    sys.exit(0)


def _read_ac_data():
    global ac_data
    with closing(shelve.open(db_path, 'r')) as sf:
        ac_data = sf['ac_data']
        print('Got {0} acer!'.format(len(ac_data.keys()), ))
        for i in ac_data.keys():
            print(i)


def _add_acer(_acer_no: str):
    ac_data[_acer_no] = {'name': '',
                         'date': '',
                         'vlist': {},
                         'aclist': []
                         }


def _remove_acer(_acer_no: str):
    ac_data.pop(_acer_no)


def _edit_acer_date(_acer_no: str, _acer_date: str):
    ac_data[_acer_no]['date'] = _acer_date


def _save_ac_data():
    with closing(shelve.open(db_path, 'n')) as sf:
        sf['ac_data'] = ac_data
        print('ac_data has saved!')


def _print_ac_data():
    for i in ac_data.keys():
        print(i + '\n|__>\t' + str(ac_data[i]))


if __name__ == '__main__':
    _read_ac_data()
    #_add_acer('110')
    #_edit_acer_date('110', '2010-10-20')
    _print_ac_data()
    _save_ac_data()
