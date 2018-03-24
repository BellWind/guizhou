#__author__ = 'Administrator'
# -*- coding: utf-8 -*-

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


# 图片上传七牛云，向数据库插入图片地址
def upload_qiniu(image_tag, path):
    # 要上传的本地文件路径
    localPhoto = path
    if os.path.exists(localPhoto):
        # 上传到七牛后保存的文件名
        key = '%s.jps' % image_tag
        #生成上传Token,可以指定过期时间等
        token = q.upload_token(bucket_name,key,3600)
        ret,info = put_file(token,key,localPhoto)

    # image_url = 'http://ozwyjb3op.bkt.clouddn.com/%s.jps' % image_tag

with open('imgurllist.txt','w') as imglist:
    for i in range(1, 382):
        image_tag = '520000_%04d' % (i)
        print(image_tag)
        dirpath = 'photos/' + image_tag + '.jpg'
        upload_qiniu(image_tag, dirpath)
        image_url = ''
        if os.path.exists(dirpath):
            image_url = 'http://ozwyjb3op.bkt.clouddn.com/%s.jps' % image_tag
        imglist.write(image_url)
        imglist.write('\n')
imglist.close()


