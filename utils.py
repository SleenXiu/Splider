# coding=utf-8
# author:xsl

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

secret_id = 'AKIDhHfrvu6Mn6DBwVDbP1QdhaGwRju847ED'      # 替换为用户的 secretId
secret_key = 'xiH6k9ORN8h4GI8rRp25xgGdrupZ7Ypx'      # 替换为用户的 secretKey
region = 'ap-beijing'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
#scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
# 2. 获取客户端对象
client = CosS3Client(config)

import hashlib

def getFileMD5(file):
    md5obj = hashlib.md5()
    md5obj.update(file)
    hash = md5obj.hexdigest()
    return str(hash)

baseUrl = 'http://shilin-1255431184.cos.ap-beijing.myqcloud.com/'

def upload_img(image, file_name, c_type):
    file_name = getFileMD5(image)
    print(file_name)
    response = client.put_object(
        Bucket='shilin-1255431184',
        Body=image,
        Key=file_name,
        StorageClass='STANDARD',
        ContentType=c_type
    )
    print(response['ETag'])
    return baseUrl + file_name
