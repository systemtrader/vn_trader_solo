# -*- coding: utf-8 -*-

'''事件系统使用以下字典来组合事件dict的各个字段，事件内不可包含，以下若干字段可以独一无二的指定一个事件'''

event_base={
	'event_type':None
}#事件基本字段：事件类别

sending_time={
	'sending_time':None
}#发送方发出事件的时间，设定成发送时刻datetime的字符串

sender_ip={
	'sender_ip':None
}#发送方的ip

receiver_ip={
	'receiver_ip':None
}#接收者的ip

receiver_port={
	'receiver_port':None
}#接收者的端口

#
