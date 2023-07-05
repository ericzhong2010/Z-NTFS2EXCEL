# -*- coding: utf-8 -*-
"""
 @Author: eric.zhong
 @Email: ericzhong2010@qq.com
 @Date: 2023/7/4
 @SoftWare: PyCharm
 @FileName: config.py
 @Description：
"""

# import library
import os

# Global variables
## ini 配置文件路径
ini_config_path = "./config.ini"

## 程序信息
version = {
    "title": "Z-NTFS2Excel",
    "version": "1.0.0",
    "autor": "Eric.zhong",
    "email": "ericzhong2010@qq.com"
}

## 过滤icacls无效输出信息
filter_invalid_content = {
    "Successfully processed": True,
    "已成功处理": True
}

## 定义作用域列表
domain_map = {
    "AUTHORITY": "NT AUTHORITY",
    "BUILTIN": os.environ.get('computername')
}

## 定义简单权限列表
simple_permissions = {
    "(F)": "完全控制",
    "(M)": "修改权限",
    "(RX)": "读取和执行权限",
    "(R)": "只读权限",
    "(W)": "只写权限",
    "(RX,W)": "读写权限"
}

## 继承关系映射
inherit_map = {
    0: "√",
    1: "×"
}

# 权限继承应用映射
inheritRight_map = {
    "": "只有该文件夹",
    "(CI)(IO)": "只有子文件夹",
    "(OI)(IO)": "只有文件",
    "(CI)": "此文件夹和子文件夹",
    "(OI)": "此文件夹和文件",
    "(OI)(CI)(IO)": "仅子文件夹和文件",
    "(OI)(CI)": "此文件夹、子文件夹和文件"
}