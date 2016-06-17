#coding:utf8
'''
@author: chin
@date: 2016年6月1日
'''

import MySQLdb
import config
import os


conn = MySQLdb.connect(**config.DB_KWARGS)

cursor = conn.cursor()

json_files = [os.path.join(config.PLUGIN_DIR, name) for name in os.listdir(config.PLUGIN_DIR)]

sql = "INSERT INTO design_object (create_date, design_id, object_no) VALUES ('%s', '%s', '%s' )"

for single in json_files:
    design_id, create_date = single.split(os.sep)[-1].split("_")
    create_date = create_date.split(".")[0]
    plugin_nos = config.de_duplication(single)
    for plugin_no in plugin_nos:
#         print sql % (create_date, design_id, plugin_no)
        cursor.execute(sql % (create_date, design_id, plugin_no))
    print "----------finish: ", design_id

# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
# print "Database version : %s " % data
conn.commit()
conn.close()