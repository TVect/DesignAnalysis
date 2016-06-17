#coding:utf8
'''
@author: chin
@date: 2016年6月1日
'''

DB_KWARGS={
        'db': 'design',                      # Or path to database file if using sqlite3.
        'user': 'recommend',                      # Not used with sqlite3.
        'passwd': 'recommend',              # Not used with sqlite3.
        'host': '127.0.0.1',                 # Set to empty string for localhost. Not used with sqlite3.
        'port': 3306,  
        }

# target plugin keys
PLUGIN = {u'openings': [u'sOpeningNo', u'materialNo'],
          u'rooms': [u'skirtingMaterialNo', u'ceilingMaterialNo', u'floorMaterialNo'],
          u'walls': [u'forwardMaterialNo', u'backwardMaterialNo'],
          u'models': [u'sModelNo']}

PLUGIN_DIR = 'plugin/design'


import json

# de-weight the same name
def de_duplication(file_name):
    with open(file_name, 'r') as f:
        source_data = json.load(f)

    data = source_data[u'data']
    plugin_list = list()
    
    if data:
        for key, value in data.items():
            try:
                for son_key in PLUGIN[key]:
                    plugin_list += [item[son_key] for item in value]
            except KeyError:
                continue

    return set(plugin_list) - set([""])
