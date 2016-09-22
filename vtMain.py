# -*- coding: utf-8 -*-

import sys, ctypes, platform
from vtEngine import MainEngine
from uiMainWindow import *
from os import environ,path

#----------------------------------------------------------------------
def main():
	"""主程序入口"""
	# 重载sys模块，设置默认字符串编码方式为utf8
	reload(sys)
	sys.setdefaultencoding('utf8')
	
	# 设置Windows底部任务栏图标
	if 'Windows' in platform.uname() :
		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('vn.trader')

	# 初始化Qt应用对象
	app = QtGui.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon('vnpy.ico'))
	app.setFont(BASIC_FONT)
	
	# 设置Qt的皮肤
	try:
		f = file("VT_setting.json")
		setting = json.load(f)
		if setting['darkStyle']:
			import qdarkstyle
			app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))
	except:
		pass
	
	# 初始化主引擎和主窗口对象
	mainEngine = MainEngine()
	mainWindow = MainWindow(mainEngine, mainEngine.eventEngine)
	mainWindow.showMaximized()
	
	# 在主线程中启动Qt事件循环
	sys.exit(app.exec_())
	pass

from program_top.utilities.extensions_configuration import load_shared_objects
from program_top.utilities.environment_and_platform import get_current_environment_pack
from testing_funclet import testlet
	
if __name__ == '__main__':
	testlet()
	current_env=environ
	current_start_script=path.realpath(__file__)#取得当前main.py脚本的绝对路径
	current_environment_pack=get_current_environment_pack(start_script_absolute_filename=current_start_script)
	main_path=current_environment_pack['runtime_paths']['program_main_dir']
	load_shared_objects(extension_root_path=main_path,project_root_path=main_path)
	
	main()