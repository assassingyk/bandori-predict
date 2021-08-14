import os
from hoshino.config import RES_DIR

#默认图片资源路径
imgbasePath=os.path.join(os.path.expanduser(RES_DIR), 'img','bangdreampic','predict')

#默认数据缓存路径
basePath = os.path.join(os.path.abspath(os.path.realpath(os.path.dirname(__file__))), 'data')

#默认区服，0：日服，1：国际服，2：台服，3：国服，4：韩服
areacode = 3
