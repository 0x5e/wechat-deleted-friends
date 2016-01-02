#!/usr/bin/env python
# coding=utf-8

import os
import urllib, urllib2
import re
import cookielib
import time
import xml.dom.minidom
import json

MAX_GROUP_NUM = 35 # 每组人数

QRImagePath = os.getcwd() + '/qrcode.jpg'

tip = 0
uuid = ''

redirect_uri = ''

skey = ''
wxsid = ''
wxuin = ''
pass_ticket = ''
deviceId = 'e000000000000000'

BaseRequest = {}

ContactList = []
My = []

def getUUID():
	global uuid

	url = 'http://login.weixin.qq.com/jslogin'
	params = {
		'appid': 'wx782c26e4c19acffb',
		'fun': 'new',
		'lang': 'zh_CN',
		'_': int(time.time()),
	}

	request = urllib2.Request(url = url, data = urllib.urlencode(params))
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	# window.QRLogin.code = 200; window.QRLogin.uuid = "oZwt_bFfRg==";
	regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
	pm = re.search(regx, data)

	code = pm.group(1)
	uuid = pm.group(2)

	if code == '200':
		return True

	return False

def showQRImage():
	global tip

	url = 'http://login.weixin.qq.com/qrcode/' + uuid
	params = {
		't': 'webwx',
		'_': int(time.time()),
	}

	request = urllib2.Request(url = url, data = urllib.urlencode(params))
	response = urllib2.urlopen(request)

	tip = 1

	f = open(QRImagePath, 'w')
	f.write(response.read())
	f.close()

	os.system('open %s' % QRImagePath)

	print '请使用微信扫描二维码以登录'

def waitForLogin():
	global tip, redirect_uri

	url = 'http://wx.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (tip, uuid, int(time.time()))

	request = urllib2.Request(url = url)
	response = urllib2.urlopen(request)
	data = response.read()
	
	# print data

	# window.code=500;
	regx = r'window.code=(\d+);'
	pm = re.search(regx, data)

	code = pm.group(1)

	if code == '201': #已扫描
		print '成功扫描,请在手机上点击确认以登录'
		tip = 0
	elif code == '200': #已登录
		print '正在登录...'
		regx = r'window.redirect_uri="(\S+?)";'
		pm = re.search(regx, data)
		redirect_uri = pm.group(1) + '&fun=new'
	elif code == '408': #超时
		pass
	# elif code == '400' or code == '500':

	return code

def login():
	global skey, wxsid, wxuin, pass_ticket, BaseRequest

	request = urllib2.Request(url = redirect_uri)
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	'''
		<error>
			<ret>0</ret>
			<message>OK</message>
			<skey>xxx</skey>
			<wxsid>xxx</wxsid>
			<wxuin>xxx</wxuin>
			<pass_ticket>xxx</pass_ticket>
			<isgrayscale>1</isgrayscale>
		</error>
	'''

	doc = xml.dom.minidom.parseString(data)
	root = doc.documentElement

	for node in root.childNodes:
		if node.nodeName == 'skey':
			skey = node.childNodes[0].data
		elif node.nodeName == 'wxsid':
			wxsid = node.childNodes[0].data
		elif node.nodeName == 'wxuin':
			wxuin = node.childNodes[0].data
		elif node.nodeName == 'pass_ticket':
			pass_ticket = node.childNodes[0].data

	# print 'skey: %s, wxsid: %s, wxuin: %s, pass_ticket: %s' % (skey, wxsid, wxuin, pass_ticket)

	if skey == '' or wxsid == '' or wxuin == '' or pass_ticket == '':
		return False

	BaseRequest = {
		'Uin': int(wxuin),
		'Sid': wxsid,
		'Skey': skey,
		'DeviceID': deviceId,
	}

	return True

def webwxinit():

	url = 'http://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?pass_ticket=%s&skey=%s&r=%s' % (pass_ticket, skey, int(time.time()))
	params = {
		'BaseRequest': BaseRequest
	}

	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	f = open(os.getcwd() + '/webwxinit.json', 'w')
	f.write(data)
	f.close()

	# print data

	global ContactList, My
	dic = json.loads(data)
	ContactList = dic['ContactList']
	My = dic['User']

def webwxgetcontact():
	
	url = 'http://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (pass_ticket, skey, int(time.time()))

	request = urllib2.Request(url = url)
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	f = open(os.getcwd() + '/webwxgetcontact.json', 'w')
	f.write(data)
	f.close()

	# print data

	dic = json.loads(data)

	'''
		[{
			"Uin": 0,
			"UserName": "@64086c01bd043b83b7f77e91a703f2bd",
			"NickName": "杭州出租车机场预约",
			"HeadImgUrl": "/cgi-bin/mmwebwx-bin/webwxgeticon?seq=620692776&username=@64086c01bd043b83b7f77e91a703f2bd&skey=@crypt_d04f2967_17b53247d86656e12ea420c7068b57ed",
			"ContactFlag": 3,
			"MemberCount": 0,
			"MemberList": [],
			"RemarkName": "",
			"HideInputBarFlag": 0,
			"Sex": 0,
			"Signature": "",
			"VerifyFlag": 24,
			"OwnerUin": 0,
			"PYInitial": "HZCZCJCYY",
			"PYQuanPin": "hangzhouchuzuchejichangyuyao",
			"RemarkPYInitial": "",
			"RemarkPYQuanPin": "",
			"StarFriend": 0,
			"AppAccountFlag": 0,
			"Statues": 0,
			"AttrStatus": 0,
			"Province": "浙江",
			"City": "杭州",
			"Alias": "hztaxijc",
			"SnsFlag": 0,
			"UniFriend": 0,
			"DisplayName": "",
			"ChatRoomId": 0,
			"KeyWord": "gh_",
			"EncryChatRoomId": ""
		}, ...]
	'''

	MemberList = dic['MemberList']

	# 倒序遍历,不然删除的时候出问题..
	for i in xrange(len(MemberList) - 1, -1, -1):
		Member = MemberList[i]
		if Member['AttrStatus'] == 0 or Member['AttrStatus'] == 4 or Member['UserName'] == My['UserName']: # 公众号/微信团队/自己
			MemberList.remove(Member)

	return MemberList

def createChatroom(UserNames):
	MemberList = []
	for UserName in UserNames:
		MemberList.append({'UserName': UserName})


	url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxcreatechatroom?pass_ticket=%s&r=%s' % (pass_ticket, int(time.time()))
	params = {
		'BaseRequest': BaseRequest,
		'MemberCount': len(MemberList),
		'MemberList': MemberList,
		'Topic': '',
	}

	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	dic = json.loads(data)
	ChatRoomName = dic['ChatRoomName']
	MemberList = dic['MemberList']
	DelectedList = []
	for Member in MemberList:
		if Member['MemberStatus'] == 4: #被对方删除了
			DelectedList.append(Member['UserName'])

	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print ErrMsg

	return (ChatRoomName, DelectedList)

def deleteMember(ChatRoomName, UserNames):
	url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxupdatechatroom?fun=delmember&pass_ticket=%s' % (pass_ticket)
	params = {
		'BaseRequest': BaseRequest,
		'ChatRoomName': ChatRoomName,
		'DelMemberList': ','.join(UserNames),
	}

	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	dic = json.loads(data)
	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print ErrMsg

	Ret = dic['BaseResponse']['Ret']
	if Ret != 0:
		return False
		
	return True

def addMember(ChatRoomName, UserNames):
	url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxupdatechatroom?fun=addmember&pass_ticket=%s' % (pass_ticket)
	params = {
		'BaseRequest': BaseRequest,
		'ChatRoomName': ChatRoomName,
		'AddMemberList': ','.join(UserNames),
	}

	request = urllib2.Request(url = url, data = json.dumps(params))
	request.add_header('ContentType', 'application/json; charset=UTF-8')
	response = urllib2.urlopen(request)
	data = response.read()

	# print data

	dic = json.loads(data)
	MemberList = dic['MemberList']
	DelectedList = []
	for Member in MemberList:
		if Member['MemberStatus'] == 4: #被对方删除了
			DelectedList.append(Member['UserName'])

	ErrMsg = dic['BaseResponse']['ErrMsg']
	if len(ErrMsg) > 0:
		print ErrMsg

	return DelectedList

def main():

	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
	urllib2.install_opener(opener)
	
	if getUUID() == False:
		print '获取uuid失败'
		return

	showQRImage()

	while waitForLogin() != '200':
		pass

	os.remove(QRImagePath)

	if login() == False:
		print '登录失败'
		return

	webwxinit()

	MemberList = webwxgetcontact()

	MemberCount = len(MemberList)
	print '通讯录共%s位好友' % MemberCount

	ChatRoomName = ''
	result = []
	for i in xrange(0, MemberCount / MAX_GROUP_NUM):
		UserNames = []
		NickNames = []
		DelectedList = ''
		for j in xrange(0, MAX_GROUP_NUM):
			if i * MAX_GROUP_NUM + j >= MemberCount:
				break

			Member = MemberList[i * MAX_GROUP_NUM + j]
			UserNames.append(Member['UserName'])
			NickNames.append(Member['NickName'].encode('utf-8'))

		print '第%s组...' % (i + 1)
		print ', '.join(NickNames)
		raw_input('回车键继续...')

		# 新建群组/添加成员
		if ChatRoomName == '':
			(ChatRoomName, DelectedList) = createChatroom(UserNames)
		else:
			DelectedList = addMember(ChatRoomName, UserNames)

		DelectedCount = len(DelectedList)
		if DelectedCount > 0:
			result += DelectedList

		print '找到%s个被删好友' % DelectedCount
		# raw_input()

		# 删除成员
		deleteMember(ChatRoomName, UserNames)

	# todo 删除群组


	resultNames = []
	for Member in MemberList:
		if Member['UserName'] in result:
			NickName = Member['NickName']
			if Member['RemarkName'] != '':
				NickName += '(%s)' % Member['RemarkName']
			resultNames.append(NickName.encode('utf-8'))

	print '---------- 被删除的好友列表 ----------\n'
	print '\n'.join(resultNames)

if __name__ == '__main__' :

	print '本程序的查询结果可能会引起一些心理上的不适,请小心使用...'
	raw_input('回车键继续...')

	main()
