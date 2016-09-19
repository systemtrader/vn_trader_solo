# -*- coding: utf-8 -*-

def merge_dicts(list_of_dicts_to_merge):
	'''合并所有dict'''
	empty_dict={}

	for each_dict in list_of_dicts_to_merge:
		empty_dict.update(each_dict)
		pass
	return empty_dict
	pass