# -*- coding: utf-8 -*-
"""
 @Author: eric.zhong
 @Email: ericzhong2010@qq.com
 @Date: 2023/7/4
 @SoftWare: PyCharm
 @FileName: PermissionUtil.py
 @Description：
"""

# import library
import os, sys
from models.config import filter_invalid_content, simple_permissions, inheritRight_map, domain_map, inherit_map
from models.LoggerUtil import logger

class PermissionUtil():
    def __init__(self):
        # Todolist: 未来补充
        ...

    def validate_path_and_depth(self, directory, depth):
        if not os.path.exists(directory):
            logger.error("rootpath查询路径不存在, 请重新检查配置文件！")
            sys.exit(1)
        elif int != type(depth) or not str(depth).isdecimal() or not 0 <= depth < 6:
            logger.error("depht目录深度范围错误, 请重新检查配置文件！")
            sys.exit(1)

    def convert_path_slash(self, directory):
        # 判断末尾是否是斜杠
        if directory.endswith("\\") or directory.endswith("/"):
            # 剔除末尾的斜杠
            directory = directory.rstrip("\\/")
        # 单斜杠变双斜杠
        directory = directory.replace("\\", "\\\\")

        return directory

    def loop_get_permissions(self, directory, depth):
        # 1. 验证路径与遍历深度的正确性
        self.validate_path_and_depth(directory, depth)

        perm_id = 1
        perms_list = []
        # 2. 遍历根目录
        for root, dirs, files in os.walk(directory):
            logger.info("/* ------------------------------------------------------------")
            logger.info(f"/* 当前目录：{self.convert_path_slash(root)}")
            logger.info("/* ------------------------------------------------------------")
            # 3. 遍历子目录
            with os.popen("icacls \"{}\"".format(self.convert_path_slash(root)), 'r') as auths:
                for line in auths.readlines():
                    # 4. 行信息清洗与整理
                    root = root[:-1] if root[-2:] == '\\\\' else root
                    if root in line:
                        # 首行带文件夹的权限与末尾换行
                        line = line.replace('\n', '').replace(root, '').strip()
                    else:
                        # 其它行的末尾换行
                        line = line.replace('\n', '').strip()

                    # 跳过空行和文件处理信息行
                    if not line:
                        continue
                    # 检查每一行是否包含无效内容
                    is_invalid = False
                    for phrase in filter_invalid_content:
                        if phrase in line:
                            is_invalid = True
                            break
                    if is_invalid:
                        continue  # 跳过包含非法内容的行


                    # 日志输出记录
                    logger.info(f"/* 权限信息：{line}")

                    # 5. 权限信息拆解
                    # 权限所属
                    perm_domain = line[line[:line.rfind('\\')].rfind(' ') + 1:line.rfind('\\')] if line.rfind('\\') > 0 else ''

                    # 权限用户/组
                    perm_user = line[line.rfind('\\') + 1:line.rfind(':')]

                    # 完整权限信息
                    perm_fullAccessMask = line[line.rfind(':') + 1:]

                    # 权限集成信息
                    perm_inherit = str.join('', ['%s)' % v for v in ((perm_fullAccessMask.split(')')[:-3] if '(DENY)' in perm_fullAccessMask else perm_fullAccessMask.split(')')[:-2]) if len(
                            perm_fullAccessMask.split(')')) > 2 else perm_fullAccessMask.split(')')[:-2])
                                            ])

                    perm_parentInherit = 1 if '(I)' in perm_inherit else 0 # 是否从父级继承权限
                    #perm_propagateInherit = 0 if '(NP)' in perm_inherit else 1 # 是否传播继承权限
                    perm_inheritRight = [v for k, v in inheritRight_map.items() if k == perm_inherit.replace('(I)', '').replace('(NP)', '')][0] # 权限继承应用情况

                    # 简单权限匹配
                    permit_simple_permission = ""
                    deny_simple_permission = ""
                    if "(DENY)" in perm_fullAccessMask:
                        for permission in simple_permissions:
                            if permission in perm_fullAccessMask:
                                # 匹配到简单权限，执行相应操作
                                deny_simple_permission = simple_permissions[permission]
                    else:
                        for permission in simple_permissions:
                            if permission in perm_fullAccessMask:
                                # 匹配到简单权限，执行相应操作
                                permit_simple_permission = simple_permissions[permission]

                    # 高级权限匹配
                    # Todolist: 未来补充

                    # 生成json文件
                    perms_list.append({
                                    "序": perm_id,
                                    "权限路径": root,
                                    "作用域": domain_map.get(perm_domain, perm_domain),
                                    "用户/组": perm_user,
                                    "允许权限": permit_simple_permission,
                                    "拒绝权限": deny_simple_permission,
                                    # "Advance_permission": None,
                                    "从父级继承": inherit_map.get(perm_parentInherit),
                                    "继承应用于": perm_inheritRight,
                                    "文件数": len(files)
                                })
                    perm_id += 1

            # 统计当前目录深度
            current_depth = root[len(directory):].count(os.sep) + 1

            if current_depth > depth:
                # 超过指定深度，跳过该目录及其子目录
                dirs[:] = []
                continue

        return perms_list

permission = PermissionUtil()