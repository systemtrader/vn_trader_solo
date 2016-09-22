# -*- coding: utf-8 -*-

'''
本文件包含了CTA引擎中的策略开发用模板，开发策略时需要继承CtaTemplate类。
'''

from ctaBase import *
from vtConstant import *
import thread
########################################################################
class CtaTemplate(object):
	"""CTA策略模板"""
	
	#----------------------------------------------------------------------
	def __init__(self, ctaEngine, setting):
		"""Constructor"""
		self.ctaEngine = ctaEngine
		
		# 策略的基本变量，由引擎管理
		self.inited=False                 # 是否进行了初始化
		self.trading=False                # 是否启动交易，由引擎管理
		self.pos=0                        # 持仓情况
		
		# 本策略自己的order字典，自己发过的单就存入这个字典中，当回报返回时匹配就做处理，否则忽略，键是tuple,(strategy_name,frontID,sessionID,vt_orderID)，其中vt_orderID为报单时返回的值
		self.order_map={}
		self.dynamic_monitored={}#动态监控的变量，当想要在界面上显示什么变量时就使用dict来update此字典
		
		
		try:#记录柜台ID和会话ID
			self.sessionID=self.ctaEngine.mainEngine.gatewayDict['CTP'].tdApi.sessionID#本策略的会话编号，用于跟界面终端或者其他终端的区分，只限于CTP可用，其他接口时将显示报错信息
			self.frontID=self.ctaEngine.mainEngine.gatewayDict['CTP'].tdApi.frontID#本策略的柜台编号
			#在CTP中以上两者外加OrderRef可以标注一笔唯一的订单，vtOrderId是比如CTP.OrderRef
			
			
			
		except Exception, current_exception:
			print current_exception
			pass

		# 设置策略的参数
		if setting:
			self.__dict__.update(setting)
		
		# MongoDB数据库的名称，K线数据库默认为1分钟
		self.tickDbName=TICK_DB_NAME
		self.barDbName=MINUTE_DB_NAME
		
		self.productClass=EMPTY_STRING    # 产品类型（只有IB接口需要）
		self.currency=EMPTY_STRING        # 货币（只有IB接口需要）
		
		pass
	
	#----------------------------------------------------------------------
	def onInit(self):
		"""初始化策略（必须由用户继承实现）"""
		raise NotImplementedError
	
	#----------------------------------------------------------------------
	def onStart(self):
		"""启动策略（必须由用户继承实现）"""
		raise NotImplementedError
	
	#----------------------------------------------------------------------
	def onStop(self):
		"""停止策略（必须由用户继承实现）"""
		raise NotImplementedError

	#----------------------------------------------------------------------
	def onTick(self, tick):
		
		#print tick.symbol,thread.get_ident() #打印线程ID
		pass

	#----------------------------------------------------------------------
	def onOrder(self, order):
		"""收到委托变化推送（必须由用户继承实现）"""
		raise NotImplementedError
	
	#----------------------------------------------------------------------
	def onTrade(self, trade):
		"""收到成交推送（必须由用户继承实现）"""
		raise NotImplementedError
	
	#----------------------------------------------------------------------
	def onBar(self, bar):
		"""收到Bar推送（必须由用户继承实现）"""
		raise NotImplementedError
	
	#----------------------------------------------------------------------
	def buy(self, price, volume, stop=False):
		"""买开"""
		return self.sendOrder(CTAORDER_BUY, price, volume, stop)
	
	#----------------------------------------------------------------------
	def sell(self, price, volume, stop=False):
		"""卖平"""
		return self.sendOrder(CTAORDER_SELL, price, volume, stop)

	#----------------------------------------------------------------------
	def short(self, price, volume, stop=False):
		"""卖开"""
		return self.sendOrder(CTAORDER_SHORT, price, volume, stop)
 
	#----------------------------------------------------------------------
	def cover(self, price, volume, stop=False):
		"""买平"""
		return self.sendOrder(CTAORDER_COVER, price, volume, stop)
		
	#----------------------------------------------------------------------
	def sendOrder(self, orderType, price, volume, stop=False):
		"""发送委托"""
		if self.trading:
			# 如果stop为True，则意味着发本地停止单
			if stop:
				vtOrderID = self.ctaEngine.sendStopOrder(self.vtSymbol, orderType, price, volume, self)
			else:
				vtOrderID = self.ctaEngine.sendOrder(self.vtSymbol, orderType, price, volume, self)
			
			current_order_key=(self.name,self.frontID,self.sessionID,vtOrderID)
			
			order_dict={'strategy_name':self.name,
			            'frontID':self.frontID,
			            'sessionID':self.sessionID,
			            'vtOrderID':vtOrderID,
			            'order_type':orderType,
			            'price':price,
			            'volume':volume
			}
			
			self.order_map[current_order_key]=order_dict#记录当前自己发出去的订单
			
			return vtOrderID
		else:
			# 交易停止时发单返回空字符串
			return ''
		
	#----------------------------------------------------------------------
	def cancelOrder(self, vtOrderID):
		"""撤单"""
		# 如果发单号为空字符串，则不进行后续操作
		if not vtOrderID:
			return
		
		if STOPORDERPREFIX in vtOrderID:
			self.ctaEngine.cancelStopOrder(vtOrderID)
		else:
			self.ctaEngine.cancelOrder(vtOrderID)
	
	#----------------------------------------------------------------------
	def insertTick(self, tick):
		"""向数据库中插入tick数据"""
		self.ctaEngine.insertData(self.tickDbName, self.vtSymbol, tick)
	
	#----------------------------------------------------------------------
	def insertBar(self, bar):
		"""向数据库中插入bar数据"""
		self.ctaEngine.insertData(self.barDbName, self.vtSymbol, bar)
		
	#----------------------------------------------------------------------
	def loadTick(self, days):
		"""读取tick数据"""
		return self.ctaEngine.loadTick(self.tickDbName, self.vtSymbol, days)
	
	#----------------------------------------------------------------------
	def loadBar(self, days):
		"""读取bar数据"""
		return self.ctaEngine.loadBar(self.barDbName, self.vtSymbol, days)
	
	#----------------------------------------------------------------------
	def writeCtaLog(self, content):
		"""记录CTA日志"""
		content = self.name + ':' + content
		self.ctaEngine.writeCtaLog(content)
		
	#----------------------------------------------------------------------
	def putEvent(self):
		"""发出策略状态变化事件"""
		self.ctaEngine.putStrategyEvent(self.name)
		
	#----------------------------------------------------------------------
	def getEngineType(self):
		"""查询当前运行的环境"""
		return self.ctaEngine.engineType
	
