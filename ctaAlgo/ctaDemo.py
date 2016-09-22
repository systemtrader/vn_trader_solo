# -*- coding: utf-8 -*-

"""
这里的Demo是一个最简单的策略实现，并未考虑太多实盘中的交易细节，如：
1. 委托价格超出涨跌停价导致的委托失败
2. 委托未成交，需要撤单后重新委托
3. 断网后恢复交易状态
4. 等等
这些点是作者选择特意忽略不去实现，因此想实盘的朋友请自己多多研究CTA交易的一些细节，
做到了然于胸后再去交易，对自己的money和时间负责。
也希望社区能做出一个解决了以上潜在风险的Demo出来。
"""

from ctaBase import *
from ctaTemplate import CtaTemplate

class atr_break(CtaTemplate):
	
	def __parameter_initialisation(self):
		'''
		参数初始化比较多，因此包装在这一个成员函数里面一次性加载
		'''
		self.className=self.__class__.__name__#python内置的读取类名方法
		self.paramList=["band_range",
		"stop_when_profiting",
		"stop_when_loss"]#策略参数表
		
		self.varList = ['inited',
			   'trading',
			   'pos']
		
		self.trading_snapshot={}#创建字典保存交易时各种临时算出来的变量快照
		self.positions_info={}#空字典，存储持仓记录，主要是成交后记录持仓成交价格等信息
		
		pass
	
	def __init__(self,cta_engine,settings):
		super(atr_break, self).__init__(cta_engine,settings)
		
		self.__parameter_initialisation()
		pass
	
	def onInit(self):
		"""初始化策略（必须由用户继承实现）"""
		
		#这里要读取一次持仓，如果
		self.writeCtaLog(u'atr_breaking策略初始化')
		pass
	
	def onStart(self):
		"""启动策略（必须由用户继承实现）"""
		self.writeCtaLog(u'atr_breaking策略启动')
		self.putEvent()
	
	def onTrade(self, trade):
		'''成交回报，必须继承实现'''
		
		session_instrument_key=(self.sessionID,trade.symbol)#成交的标的

		# 本订单的键是tuple,(strategy_name,frontID,sessionID,vt_orderID)，其中vt_orderID为报单时返回的值
		current_order_key=(self.name,self.frontID,self.sessionID,trade.vtOrderID)
		if not self.order_map.__contains__(current_order_key):#如果本成交不是由本策略在此次登录会话中发出去的订单产生，直接返回
			return
		
		if self.pos==0:#如果此时已没有净持仓(说明本次成交的是平仓单)
			self.positions_info.pop(session_instrument_key)#删除此前的开仓记录
			return #直接返回
		
		self.positions_info[session_instrument_key]=trade.__dict__#直接留下成交记录作为持仓信息，对于单标的只有多空无三种持仓状态(不加减仓)，并且不留隔夜仓位的策略才能这样直接用
		
		#计算止盈止损价格
		
		price_of_intry=self.positions_info[session_instrument_key]['price']#入场价格
		
		if self.pos>0:#目前持有多仓
			stop_loss_price=price_of_intry*(1-self.stop_when_loss)
			stop_profiting_price=price_of_intry*(1+self.stop_when_profiting)
		
		else:#目前持有空仓
			stop_profiting_price=price_of_intry*(1-self.stop_when_profiting)
			stop_loss_price=price_of_intry*(1+self.stop_when_loss)
			pass
		
		#记录止盈止损价格，不分多空
		self.positions_info[session_instrument_key]['stop_loss_price']=stop_loss_price
		self.positions_info[session_instrument_key]['stop_profiting_price']=stop_profiting_price
		
		print '委托已成交'
		
		self.dynamic_monitored.update(self.positions_info)#持仓信息字典更新到界面动态监控
		
		pass
	
	def onStop(self):
		"""停止策略（必须由用户继承实现）"""
		self.writeCtaLog(u'atr_breaking策略停止')
		self.putEvent()
	
	def onTick(self, tick):
		"""收到行情TICK推送（必须由用户继承实现）"""
		# 计算K线
		super(atr_break, self).onTick(tick)#调用父类的ontick
		
		if not self.trading_snapshot.has_key("open_today"):#如果之前没有记录开盘价，则记录今日的开盘价和张跌停价格
			self.trading_snapshot['open_today']=tick.openPrice
			self.trading_snapshot["upper_limit"]=tick.upperLimit
			self.trading_snapshot["lower_limit"]=tick.lowerLimit
			self.dynamic_monitored.update(self.trading_snapshot)#更新到界面监控
			pass
		
				
		'''
		if tick.datetime.minute#取得当前tick所在的分钟
			self.open_today=tick.open
			open("buffer_of_tick.csv")
			'''
		
		tickMinute=tick.datetime.minute#取得当前tick所在的分钟
		
		if (not hasattr(self,'barMinute')) or(tickMinute!=self.barMinute):#当tick是新一分钟的tick，或者之前没有产生过tick
			if hasattr(self,'bar'):#如果之前已经有过缓存的上一根bar，将上一根bar传入onBar
				self.onBar(self.bar)
			
			bar=CtaBarData()
			bar.vtSymbol=tick.vtSymbol
			bar.symbol=tick.symbol
			bar.exchange=tick.exchange
			
			bar.open=tick.lastPrice
			bar.high=tick.lastPrice
			bar.low=tick.lastPrice
			bar.close=tick.lastPrice
			
			bar.date=tick.date
			bar.time=tick.time
			bar.datetime=tick.datetime    # K线的时间设为第一个Tick的时间
			
			# 实盘中用不到的数据可以选择不算，从而加快速度
			#bar.volume = tick.volume
			#bar.openInterest = tick.openInterest
			
			self.bar=bar                  # 这种写法为了减少一层访问，加快速度
			self.barMinute=tickMinute     # 更新当前的分钟
		
		else:                               # 否则继续累加新的K线
			bar=self.bar                  # 写法同样为了加快速度
			
			bar.high=max(bar.high, tick.lastPrice)
			bar.low=min(bar.low, tick.lastPrice)
			bar.close=tick.lastPrice
			
		pass
		
		
	def onOrder(self, order):
		'''
		委托已发出的回报，必须实现
		'''
		print "委托已发出"
		
		
		pass
	
	def onBar(self, bar):
		"""收到Bar推送（必须由用户继承实现）"""
		#计算策略指标
		# 发出状态更新事件
		
		if not self.trading_snapshot.has_key('upper_band'):#如果盘中缓存没有记录过本日开盘价的上band
			self.trading_snapshot['upper_band']=self.trading_snapshot['open_today']*(1+self.band_range)
			self.trading_snapshot['lower_band']=self.trading_snapshot['open_today']*(1-self.band_range)
			pass#计算上下band
		
		###接下来判断策略条件
			
		if self.pos==0:#如果目前没有持仓
			try:#尝试报单，如果不成则显示异常信息
				whether_open_long=self.trading_snapshot['upper_band']<=bar.close#布尔值，是否开多
				whether_open_short=self.trading_snapshot['lower_band']>=bar.close#布尔值，是否开空
				if whether_open_long:
					self.buy(self.trading_snapshot["upper_limit"], 1)#市价买多一手(以涨停价格委托)
				if whether_open_short:
					self.short(self.trading_snapshot["lower_limit"], 1)#市价卖空一手(以跌停价格委托)
			
			except Exception, current_exception:
				print u'显示报单异常信息:', current_exception
				pass
		else:#如果有持仓
			current_session_instrument_key=(self.sessionID,bar.vtSymbol)
			
			current_position=self.positions_info[current_session_instrument_key]#取得持仓信息
			
			if self.pos>0:#如果持有多仓，判断止盈止损
				got_to_stop_loss=bar.close<current_position['stop_loss_price']
				got_to_stop_profiting=bar.close>current_position['stop_profiting_price']
				if got_to_stop_loss or got_to_stop_profiting:#如果要止盈或者止损，卖出
					self.sell(self.trading_snapshot["lower_limit"], 1)
			else:#空仓的情况
				got_to_stop_loss=bar.close>current_position['stop_loss_price']
				got_to_stop_profiting=bar.close<current_position['stop_profiting_price']
				if got_to_stop_loss or got_to_stop_profiting:#如果要止盈或者止损，买入
					self.cover(self.trading_snapshot["upper_limit"], 1)
				pass
			pass
		
		
		self.putEvent()
	pass

########################################################################
class DoubleEmaDemo(CtaTemplate):
	"""双指数均线策略Demo"""
	className = 'DoubleEmaDemo'
	author = u'用Python的交易员'
	
	# 策略参数
	fastK = 0.9	 # 快速EMA参数
	slowK = 0.1	 # 慢速EMA参数
	initDays = 10   # 初始化数据所用的天数
	
	# 策略变量
	bar = None
	barMinute = EMPTY_STRING
	
	fastMa = []			 # 快速EMA均线数组
	fastMa0 = EMPTY_FLOAT   # 当前最新的快速EMA
	fastMa1 = EMPTY_FLOAT   # 上一根的快速EMA

	slowMa = []			 # 与上面相同
	slowMa0 = EMPTY_FLOAT
	slowMa1 = EMPTY_FLOAT
	
	# 参数列表，保存了参数的名称
	paramList = ['name',
				 'className',
				 'author',
				 'vtSymbol',
				 'fastK',
				 'slowK']
	
	# 变量列表，保存了变量的名称
	varList = ['inited',
			   'trading',
			   'pos',
			   'fastMa0',
			   'fastMa1',
			   'slowMa0',
			   'slowMa1']

	#----------------------------------------------------------------------
	def __init__(self, ctaEngine, setting):
		"""Constructor"""
		super(DoubleEmaDemo, self).__init__(ctaEngine, setting)
		
		# 注意策略类中的可变对象属性（通常是list和dict等），在策略初始化时需要重新创建，
		# 否则会出现多个策略实例之间数据共享的情况，有可能导致潜在的策略逻辑错误风险，
		# 策略类中的这些可变对象属性可以选择不写，全都放在__init__下面，写主要是为了阅读
		# 策略时方便（更多是个编程习惯的选择）
		self.fastMa = []
		self.slowMa = []
		pass
		
	#----------------------------------------------------------------------
	def onInit(self):
		"""初始化策略（必须由用户继承实现）"""
		self.writeCtaLog(u'双EMA演示策略初始化')
		
		initData = self.loadBar(self.initDays)
		for bar in initData:
			self.onBar(bar)
		
		self.putEvent()
		
	#----------------------------------------------------------------------
	def onStart(self):
		"""启动策略（必须由用户继承实现）"""
		self.writeCtaLog(u'双EMA演示策略启动')
		self.putEvent()
	
	#----------------------------------------------------------------------
	def onStop(self):
		"""停止策略（必须由用户继承实现）"""
		self.writeCtaLog(u'双EMA演示策略停止')
		self.putEvent()
		
	#----------------------------------------------------------------------
	def onTick(self, tick):
		"""收到行情TICK推送（必须由用户继承实现）"""
		# 计算K线
		super(DoubleEmaDemo, self).onTick(tick)
		
		tickMinute = tick.datetime.minute
		
		if tickMinute != self.barMinute:
			if self.bar:
				self.onBar(self.bar)
			
			bar = CtaBarData()
			bar.vtSymbol = tick.vtSymbol
			bar.symbol = tick.symbol
			bar.exchange = tick.exchange
			
			bar.open = tick.lastPrice
			bar.high = tick.lastPrice
			bar.low = tick.lastPrice
			bar.close = tick.lastPrice
			
			bar.date = tick.date
			bar.time = tick.time
			bar.datetime = tick.datetime	# K线的时间设为第一个Tick的时间
			
			# 实盘中用不到的数据可以选择不算，从而加快速度
			#bar.volume = tick.volume
			#bar.openInterest = tick.openInterest
			
			self.bar = bar				  # 这种写法为了减少一层访问，加快速度
			self.barMinute = tickMinute	 # 更新当前的分钟
			
		else:							   # 否则继续累加新的K线
			bar = self.bar				  # 写法同样为了加快速度
			
			bar.high = max(bar.high, tick.lastPrice)
			bar.low = min(bar.low, tick.lastPrice)
			bar.close = tick.lastPrice
		
	#----------------------------------------------------------------------
	def onBar(self, bar):
		"""收到Bar推送（必须由用户继承实现）"""
		# 计算快慢均线
		if not self.fastMa0:
			self.fastMa0 = bar.close
			self.fastMa.append(self.fastMa0)
		else:
			self.fastMa1 = self.fastMa0
			self.fastMa0 = bar.close * self.fastK + self.fastMa0 * (1 - self.fastK)
			self.fastMa.append(self.fastMa0)
			
		if not self.slowMa0:
			self.slowMa0 = bar.close
			self.slowMa.append(self.slowMa0)
		else:
			self.slowMa1 = self.slowMa0
			self.slowMa0 = bar.close * self.slowK + self.slowMa0 * (1 - self.slowK)
			self.slowMa.append(self.slowMa0)
			
		# 判断买卖
		crossOver = self.fastMa0>self.slowMa0 and self.fastMa1<self.slowMa1	 # 金叉上穿
		crossBelow = self.fastMa0<self.slowMa0 and self.fastMa1>self.slowMa1	# 死叉下穿
		
		# 金叉和死叉的条件是互斥
		# 所有的委托均以K线收盘价委托（这里有一个实盘中无法成交的风险，考虑添加对模拟市价单类型的支持）
		if crossOver:
			# 如果金叉时手头没有持仓，则直接做多
			if self.pos == 0:
				self.buy(bar.close, 1)
			# 如果有空头持仓，则先平空，再做多
			elif self.pos < 0:
				self.cover(bar.close, 1)
				self.buy(bar.close, 1)
		# 死叉和金叉相反
		elif crossBelow:
			if self.pos == 0:
				self.short(bar.close, 1)
			elif self.pos > 0:
				self.sell(bar.close, 1)
				self.short(bar.close, 1)
				
		# 发出状态更新事件
		self.putEvent()
		
	#----------------------------------------------------------------------
	def onOrder(self, order):
		"""收到委托变化推送（必须由用户继承实现）"""
		# 对于无需做细粒度委托控制的策略，可以忽略onOrder
		pass
	
	#----------------------------------------------------------------------
	def onTrade(self, trade):
		"""收到成交推送（必须由用户继承实现）"""
		# 对于无需做细粒度委托控制的策略，可以忽略onOrder
		pass
	
	
########################################################################################
class OrderManagementDemo(CtaTemplate):
	"""基于tick级别细粒度撤单追单测试demo"""
	
	className = 'OrderManagementDemo'
	author = u'用Python的交易员'
	
	# 策略参数
	initDays = 10   # 初始化数据所用的天数
	
	# 策略变量
	bar = None
	barMinute = EMPTY_STRING
	
	
	# 参数列表，保存了参数的名称
	paramList = ['name',
				 'className',
				 'author',
				 'vtSymbol']
	
	# 变量列表，保存了变量的名称
	varList = ['inited',
			   'trading',
			   'pos']

	#----------------------------------------------------------------------
	def __init__(self, ctaEngine, setting):
		"""Constructor"""
		super(OrderManagementDemo, self).__init__(ctaEngine, setting)
				
		self.lastOrder = None
		self.orderType = ''
		
	#----------------------------------------------------------------------
	def onInit(self):
		"""初始化策略（必须由用户继承实现）"""
		self.writeCtaLog(u'双EMA演示策略初始化')
		
		initData = self.loadBar(self.initDays)
		for bar in initData:
			self.onBar(bar)
		
		self.putEvent()
		
	#----------------------------------------------------------------------
	def onStart(self):
		"""启动策略（必须由用户继承实现）"""
		self.writeCtaLog(u'双EMA演示策略启动')
		self.putEvent()
	
	#----------------------------------------------------------------------
	def onStop(self):
		"""停止策略（必须由用户继承实现）"""
		self.writeCtaLog(u'双EMA演示策略停止')
		self.putEvent()
		
	#----------------------------------------------------------------------
	def onTick(self, tick):
		"""收到行情TICK推送（必须由用户继承实现）"""

		# 建立不成交买单测试单
		if self.lastOrder == None:
			self.buy(tick.lastprice - 10.0, 1)

		# CTA委托类型映射
		if self.lastOrder != None and self.lastOrder.direction == u'多' and self.lastOrder.offset == u'开仓':
			self.orderType = u'买开'

		elif self.lastOrder != None and self.lastOrder.direction == u'多' and self.lastOrder.offset == u'平仓':
			self.orderType = u'买平'

		elif self.lastOrder != None and self.lastOrder.direction == u'空' and self.lastOrder.offset == u'开仓':
			self.orderType = u'卖开'

		elif self.lastOrder != None and self.lastOrder.direction == u'空' and self.lastOrder.offset == u'平仓':
			self.orderType = u'卖平'
				
		# 不成交，即撤单，并追单
		if self.lastOrder != None and self.lastOrder.status == u'未成交':

			self.cancelOrder(self.lastOrder.vtOrderID)
			self.lastOrder = None
		elif self.lastOrder != None and self.lastOrder.status == u'已撤销':
		# 追单并设置为不能成交
			
			self.sendOrder(self.orderType, self.tick.lastprice - 10, 1)
			self.lastOrder = None
			
	#----------------------------------------------------------------------
	def onBar(self, bar):
		"""收到Bar推送（必须由用户继承实现）"""
		pass
	
	#----------------------------------------------------------------------
	def onOrder(self, order):
		"""收到委托变化推送（必须由用户继承实现）"""
		# 对于无需做细粒度委托控制的策略，可以忽略onOrder
		self.lastOrder = order
	
	#----------------------------------------------------------------------
	def onTrade(self, trade):
		"""收到成交推送（必须由用户继承实现）"""
		# 对于无需做细粒度委托控制的策略，可以忽略onOrder
		pass
