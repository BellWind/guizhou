#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib
import os
from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import os

#七牛云配置
#需要填写你的 Access Key 和 Secret Key
access_key = 'GLCCcNfZiqOx4pjL6SDZGRfDu-QMX6cYMB9Yupku'
secret_key = 'TOPsxBISmd091aVza3WNdiJwTPRtgHY_k8aWBOdj'
#构建鉴权对象
q = Auth(access_key, secret_key)
#要上传的空间
bucket_name = 'officer'

with open('tmp.txt', 'r') as f:
    lines = f.readlines()
    tot = len(lines)
    id = 1
    with open('imgurllist.txt','w') as imglist:
        for i in range(0, tot, 6):

            imgurl = lines[i+1].rstrip('\n')
            imgname = '520000_%04d' % (id)
            id += 1
            dirpath = 'photos/' + imgname + '.jpg'
            print(dirpath)
            if os.path.exists(dirpath):
                continue
            with open(dirpath, 'wb') as imgf:
                if len(imgurl):
                    print(imgurl)
                    try:
                        conn = urllib.request.urlopen(imgurl,timeout=10)
                        imgf.write(conn.read())
                    finally:
                        pass
            imgf.close()
    imglist.close()
