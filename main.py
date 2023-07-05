# -*- coding: utf-8 -*-
"""
 @Author: eric.zhong
 @Email: ericzhong2010@qq.com
 @Date: 2023/7/4
 @SoftWare: PyCharm
 @FileName: main.py
 @Description：
"""

# import library
import traceback, json
from models.config import *
from configparser import ConfigParser
from models.PermissionUtil import *
from models.WriteExcelUtil import *
from models.LoggerUtil import logger

def main():
    # 1. 简要程序信息
    print("{title} - {version}\n{autor} {email}\n".format(title=version['title'], version=version['version'],
                                                          autor=version['autor'], email=version['email']))

    # 2. 读取参数 ini -> json格式转换
    config = ConfigParser()
    config.read(ini_config_path, encoding="UTF-8-sig")

    rootpath = config.get("SEARCH", "rootpath")
    depth = int(config.get("SEARCH", "depth"))
    savepath = config.get("SEARCH", "savepath")
    savetype = config.get("SEARCH", "savetype")

    """
    config_json = {}
    for ini in config.sections():
        config_json[ini.lower()] = dict(config.items(ini))
    """

    # 3. 验证与处理参数
    # Todolist: 未来补充

    # 4. 获取路径权限
    auths_json = permission.loop_get_permissions(rootpath, depth)

    # 5. 输出格式报告
    if savetype.lower() == 'xlsx':
        writeexcel.write_data_to_excel(savepath, auths_json)
    elif savetype.lower() == 'json':
        computerName = os.environ.get('computername')
        with open('{}\{}_{}.json'.format(savepath, computerName, time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))), 'w', encoding="utf-8") as write_f:
            write_f.write(json.dumps(auths_json, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error("程序存在Bug，错误日志：%s" % e)
        sys.exit(1)
