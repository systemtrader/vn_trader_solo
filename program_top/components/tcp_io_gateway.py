# -*- coding: utf-8 -*-
from tornado.tcpserver import TCPServer
from program_top.utilities.ip_and_socket import get_local_ip
from program_top.components import component_base

class tcp_gateway(component_base):
	def __init__(self, in_port, callback_entrance=None, binding_instance=None):
		'''指定输入端口号，整数
		指定回调函数入口
		指定持有这个端口的实例
		'''
		super(tcp_gateway, self).__init__(binding_instance)
		
		platform_category=binding_instance._environment_pack['current_platform_info']['current_system_category']
		self.lan_ip=get_local_ip(platform_category)
		self.listening_port=in_port
		if callback_entrance:
			self.listener=tcp_intrance(in_port, callback_entrance)
		pass
	pass

class tcp_sender(object):
	pass

class tcp_intrance(TCPServer):
	'''
	tcpip消息入口服务器，iostream默认缓冲区100mb
	'''
	def __init__(self, in_port, callback_entrance=None):
		super(tcp_intrance, self).__init__()#注意此处tcpserver可以有出入缓冲区大小的设置
		self.callback_entry=callback_entrance
		pass
	
	def handle_stream(self, stream, address):
		'''
		客户端连入时触发的回调
		'''
		stream.read_until_close(self.callback_entry)
		pass
	pass