# -*- coding: utf-8 -*-
"""
 @Author: eric.zhong
 @Email: ericzhong2010@qq.com
 @DateTime: 2023/6/22 20:42
 @SoftWare: PyCharm
 @FileName: LoggerUtil.py
 @Description：
"""

# import library
import os
import time
import logging
from logging import handlers


class GetLogger(object):
    """ 日志封装类 """

    @classmethod
    def get_logger(cls):
        # log = logging.getLogger(__name__) # 不会打印 HTTP General 信息
        log = logging.getLogger(__name__)
        level_relations = {
            'NOTSET': logging.NOTSET,
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }  # 日志级别关系映射

        # 创建日志存放的目录
        project_path = "./"
        logs_dir = project_path + "logs"
        if os.path.exists(logs_dir) and os.path.isdir(logs_dir):
            pass
        else:
            os.mkdir(logs_dir)
        # 日志文件以日期命名
        log_file_name = '%s.log' % time.strftime("%Y-%m-%d", time.localtime())
        log_file_path = os.path.join(logs_dir, log_file_name)

        rotating_file_handler = handlers.TimedRotatingFileHandler(filename=log_file_path,
                                                                  when='D',  # 按天分隔，一天一个文件
                                                                  interval=30,
                                                                  encoding='utf-8')

        # 日志输出格式
        fmt = "%(asctime)s %(levelname)s %(message)s"
        formatter = logging.Formatter(fmt)
        rotating_file_handler.setFormatter(formatter)

        # 加上判断，避免重复打印日志
        if not log.handlers:
            # 控制台输出
            console = logging.StreamHandler()
            console.setLevel(level_relations["NOTSET"])
            console.setFormatter(formatter)
            # 写入日志文件
            log.addHandler(rotating_file_handler)
            log.addHandler(console)
            log.setLevel(level_relations['DEBUG'])
        return log

logger = GetLogger().get_logger()

'''
调用方法参考
from logger import logger
from model.LoggerUtil import logger

正常信息记录
logger.info(str)

错误信息记录
except Exception as err:
   logger.error(err)

告警信息记录
logger.WARNING()
'''