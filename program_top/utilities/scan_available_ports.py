# -*- coding: utf-8 -*-
import os

def isInuseWindow(port):
	if os.popen('netstat -an | findstr :' + str(port)).readlines():
		portIsUse = True
		print '%d is inuse' % port
	else:
		portIsUse = False
		print '%d is free' % port
	return portIsUse

def isInuseLinux(port):
	#lsof -i:4906
	#not show pid to avoid complex
	if os.popen('netstat -na | grep :' + str(port)).readlines():
		portIsUse = True
		print '%d is inuse' % port
	else:
		portIsUse = False
		print '%d is free' % port
	return portIsUse

def scan_available_ports_then_return(platform_category):
	'''
	从65535开始向下扫描一个能用的端口，并返回
	'''

	if 'windows' in platform_category:
		port_judging=isInuseWindow
	else:
		port_judging=isInuseLinux

	for each_port in range(65535,0,-1):
		if not port_judging(each_port):
			return each_port
		else:
			continue
		pass
	pass