#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import itchat
import json
import datetime
import os
import time
cmd_list = ['【发布/修正作业】','【查询作业】','【推送作业】','【推送消息】','【删除作业附图】','【测试管理员权限】','【获取帮助文档】']
def read_hw_file():
    file_obj = open('hw.txt')
    try:
        js = file_obj.read()
        return json.loads(js)
    finally:
        file_obj.close()
def save_hw_file(homework):
    js = json.dumps(homework)
    file_obj = open('hw.txt','w+')
    file_obj.truncate()
    file_obj.writelines(js)
    file_obj.close()
def is_user_admin(from_user_name):
    user_name=itchat.search_friends(userName=from_user_name)['RemarkName']
    if user_name=='admin':
        return True
    else:
        itchat.send('您无法进行此操作。',from_user_name)
        return False
def is_pic_exists():
    if os.path.exists('pic'):
        return True
    else:
        return False
def del_pic(from_user_name):
    if is_user_admin(from_user_name):
        if is_pic_exists():
            os.remove('pic')
            itchat.send('已删除作业附图。',from_user_name)
        else:
            itchat.send('作业附图不存在。',from_user_name)
def admin_test(from_user_name):
    itchat.send(str(is_user_admin(from_user_name)),from_user_name)
def get_doc(from_user_name):
    itchat.send('@fil@doc.txt',from_user_name)
def push_basic(content,with_pic):
    friend_list=itchat.search_friends(name='user')+itchat.search_friends(name='admin')
    for friend in friend_list:
        itchat.send('以下为推送消息：\n'+content,friend['UserName'])
        if with_pic==True:
            itchat.send('@img@pic',friend['UserName'])
        time.sleep(.5)
def push(cmd_list,from_user_name):
    if is_user_admin(from_user_name):
        itchat.send('开始尝试推送消息，可能耗费一定时间……',from_user_name)
        push_basic(cmd_list[1],False)
        itchat.send('消息已推送。',from_user_name)
def publish_homework(cmd_list,from_user_name):
    if is_user_admin(from_user_name):
        save_hw_file({'date':cmd_list[1],'content':cmd_list[2],'publisher':cmd_list[3]})
        itchat.send('作业已发布/修正。',from_user_name)
def get_homework(from_user_name):
    hw = read_hw_file()
    itchat.send(hw['date'] + '作业：\n' + hw['content'] + '\n发布者：' + hw['publisher'],from_user_name)
    if is_pic_exists:
        itchat.send('@img@pic',from_user_name)
def push_homework(from_user_name):
    if is_user_admin(from_user_name):
        hw = read_hw_file()
        itchat.send('开始尝试推送作业，可能耗费一定时间……',from_user_name)
        if is_pic_exists():
            push_basic(hw['date'] + '作业：\n' + hw['content'] + '\n发布者：' + hw['publisher'],True)
        else:
            push_basic(hw['date'] + '作业：\n' + hw['content'] + '\n发布者：' + hw['publisher'],False)
        itchat.send('作业已推送。',from_user_name)
def cmd_parse(cmd_list,from_user_name):
    if cmd_list[0] == '发布/修正作业':
        if len(cmd_list) >= 4:
            publish_homework(cmd_list,from_user_name)
        else:
            itchat.send('命令可能有误。',from_user_name)
    elif cmd_list[0] == '查询作业':
        get_homework(from_user_name)
    elif cmd_list[0] == '推送作业':
        push_homework(from_user_name)
    elif cmd_list[0] == '推送消息':
        if len(cmd_list) >= 2:
            push(cmd_list,from_user_name)
        else:
            itchat.send('命令可能有误。',from_user_name)
    elif cmd_list[0] == '删除作业附图':
        del_pic(from_user_name)
    elif cmd_list[0] == '测试管理员权限':
        admin_test(from_user_name)
    elif cmd_list[0] == '获取帮助文档':
        get_doc(from_user_name)
    else:
        wrong_cmd(from_user_name)
def wrong_cmd(from_user_name):
    cmd = ''
    for x in cmd_list:
        cmd += x + '\n'
    itchat.send('目前可用命令：\n' + cmd,from_user_name)
@itchat.msg_register(itchat.content.TEXT)
def cmd_split(msg):
    itchat.get_friends(update=True)
    user_name=itchat.search_friends(userName=msg.fromUserName)['RemarkName']
    if user_name=='admin' or user_name=='user':
        if msg.text.startswith('【') and msg.text.endswith('】'):
            if '‖' in msg.text.lstrip('【').rstrip('】'):
                cmd_parse(msg.text.lstrip('【').rstrip('】').split('‖'),msg.fromUserName)
            else:
                cmd_parse([msg.text.lstrip('【').rstrip('】')],msg.fromUserName)
        else:
            wrong_cmd(msg.fromUserName)
@itchat.msg_register(itchat.content.PICTURE)
def download_pic(msg):
    if is_user_admin(msg.fromUserName):
        msg.download('pic')
        itchat.send('图片已下载，将作为当前作业的补充说明图片。',msg.fromUserName)
@itchat.msg_register(itchat.content.FRIENDS)
def apply_friends(msg):
    if msg.content.find('十一班')!=-1:
        msg.user.verify()
        itchat.set_alias(msg.user['UserName'],'user')
        itchat.send('您好，欢迎您使用十一班作业查询机器人！\n我不能保证这个机器人在任何时间都正常工作，\n也不能保证推送的作业准确无误。\n请勿向我频繁发送大量消息！',msg.user['UserName'])
        wrong_cmd(msg.user['UserName'])
itchat.auto_login(hotReload=True,enableCmdQR=2)
itchat.run()
