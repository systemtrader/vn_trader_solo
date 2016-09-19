# -*- coding: utf-8 -*-
from multiprocessing import Process
from zmq.eventloop import IOLoop

class my_engine(Process):
	'''
	进程引擎，接受socket监听作为事件循环，发出请求的时候发起连接
	初始化确定本进程的执行参数，包括平台，python版本
	'''
	def __init__(self,working_type,current_envinroment):
		super(my_engine, self).__init__()
		self.__environments=current_envinroment
		self.__working_type=working_type
		self.__working_instance=None
		self.start()
		pass

	def __self_register_from_hub(self):

		pass

	def run(self):
		#print id(self),'这里是子进程'

		self.__working_instance=self.__working_type(self.__environments)

		IOLoop.instance().start()
		pass
	pass