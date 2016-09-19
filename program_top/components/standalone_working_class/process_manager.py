# -*- coding: utf-8 -*-

from program_top.components.standalone_working_class import standalone_working_class
from program_top.utilities.csv_and_json_serialisation import temperarily_save_a_local_json

class process_manager(standalone_working_class):
	'''
	主进程的主要工作实例，接收外部tcp传入的消息，保存整个工作网络的参数和环境变量，当时间到时向订阅定时器事件的进程发出消息
	'''
	def __init__(self,environment_pack=None):#如有环境变量信息则传入
		super(process_manager, self).__init__(environment_pack)
		self.__address_table={}#地址表，各个类实例的名称，以及它们在本网络内的地址，地址格式以tcp://ip:port为准，接收到查询请求的时候返回当前的地址表给需要此表的工作实例
		self._inform_ready()
		pass

	def _inform_ready(self):
		'''当自己的初始化完成后，调用此函数，发现自己是进程经理，就把IP和端口号保存在内存，并且存入本地硬盘，以后其他类生成就从这个IP和端口读取，然后调用父类同名函数，通知自己，自己已经注册'''




		if self.__class__.__name__=='process_manager':
			config_filename=self._environment_pack['instance_config']['config_file_dir']+'lan_ip_config.json'
			ip_info={'process_manager':
						 {'lan_ip':self._io_gateway.lan_ip,
						  'listening_port':self._io_gateway.listening_port}
						 }
			temperarily_save_a_local_json(ip_info,config_filename)
			pass

		super(process_manager, self)._inform_ready()
		pass
	pass