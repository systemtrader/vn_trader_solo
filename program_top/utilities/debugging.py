# -*- coding: utf-8 -*-

'''
调试
'''

def callback_debug_start():
	try:#python解释器没有安装此包也可以调试，import时解释器提示没有此包不必理会，调试器pydevd在pycharm/eclipse调试时自带，如果ide也没有，则需要手动安装
		import pydevd
		pydevd.settrace(suspend=False, trace_only_current_thread=True)
	except:
		print("python解释器运行时无法跟踪断点调试")
		pass
	pass