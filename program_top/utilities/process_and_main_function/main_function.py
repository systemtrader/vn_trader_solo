# -*- coding: utf-8 -*-
from zmq.eventloop import IOLoop

from program_top.utilities.environment_and_platform import get_current_environment_pack

def main(start_script_file,running_class_def=None):
	'''主函数，传入开始执行的主函数，然后以指定的类作为起始工作实例，为单实例机器的程序入口'''
	current_environment_pack=get_current_environment_pack(start_script_absolute_filename=start_script_file)
	if running_class_def:
		current_working_instance=running_class_def(current_environment_pack)
		#print id(current_working_engine),'这里是主进程'

	#local_working_processes=load_instances(current_environment_pack)

	IOLoop.instance().start()
	pass