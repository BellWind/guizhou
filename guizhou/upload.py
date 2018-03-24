#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
import math

try:
    conn = MySQLdb.Connect(
        host='111.205.121.93',
        user='user',
        passwd='g927@buaa',
        db='government',
        port=9002,
        charset="utf8"
    )
    cur = conn.cursor()
    head = "INSERT INTO officer(`id`,`code`,`index`,`name`,`image_url`,`profile`,`organization`,`position`,`info_url`) VALUES "
    id = 2560
    index = 1


    with open('imgurllist.txt', 'r') as f:
        imgurls = f.readlines()
    f.close()

    with open('tmp.txt','r') as f:
        lines = f.readlines()
        tot = len(lines)
        for i in range(0, tot, 6):
            name = lines[i].rstrip('\n')
            image_url = imgurls[math.floor(i/6)].rstrip('\n')
            profile = lines[i+2].rstrip('\n')
            organization = lines[i+3].rstrip('\n')
            position = lines[i+4].rstrip('\n')
            info_url = lines[i+5].rstrip('\n')
            print("--------------------------------")
            sql = head + "('%d','%s','%04d','%s','%s','%s','%s','%s','%s');" % (id,'520000', index, name, image_url, profile, organization, position, info_url)
            print(sql)
            cur.execute(sql)
            cur.nextset()
            id += 1
            index += 1
    conn.commit()
    conn.close()
except MySQLdb.Error as e:
    print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
