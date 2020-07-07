# -*- coding: utf-8 -*-
# =============================================================================
# Copyright (c) 2018-, pyLeo Developer. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================
"""The scraper is use for website process interaction."""
from accessor.request_worker import RequestWorker
from accessor.request_crawler import RequestCrawler
from booster.aes_formatter import AESFormatter
from booster.basic_formatter import BasicFormatter
from booster.basic_parser import BasicParser
from booster.callback_formatter import CallBackFormatter
from booster.callin_parser import CallInParser
from booster.date_formatter import DateFormatter
from booster.dom_parser import DomParser
from collector.pers5j_mirror import Pers5JMirror


class Pers5JScraper(RequestWorker):
	"""5J采集器，行李价格抓取
    """
	
	def __init__(self):
		RequestWorker.__init__(self)
		self.RCR = RequestCrawler()  # 请求爬行器。
		self.AFR = AESFormatter()  # AES格式器。
		self.BFR = BasicFormatter()  # 基础格式器。
		self.BPR = BasicParser()  # 基础解析器。
		self.CFR = CallBackFormatter()  # 回调格式器。
		self.CPR = CallInParser(False)  # 接入解析器。
		self.DFR = DateFormatter()  # 日期格式器。
		self.DPR = DomParser()  # 文档解析器。
		self.PMR = Pers5JMirror()
	
	def init_to_assignment(self) -> bool:
		"""Assignment to logger. 赋值logger。

		Returns:
			bool
		"""
		self.RCR.logger = self.logger
		self.AFR.logger = self.logger
		self.BFR.logger = self.logger
		self.BPR.logger = self.logger
		self.CFR.logger = self.logger
		self.CPR.logger = self.logger
		self.DFR.logger = self.logger
		self.DPR.logger = self.logger
		self.PMR.logger = self.logger
		return True
	
	def process_to_main(self, process_dict: dict = None) -> dict:
		"""Main process. 主程序入口。

		Args:
			process_dict (dict): Parameters. 传参。

		Returns:
			dict
		"""
		task_id = process_dict.get("task_id")
		log_path = process_dict.get("log_path")
		source_dict = process_dict.get("source_dict")
		enable_proxy = process_dict.get("enable_proxy")
		address = process_dict.get("address")
		self.retry_count = process_dict.get("retry_count")
		if not self.retry_count:
			self.retry_count = 1
		# # # 初始化日志。
		self.init_to_logger(task_id, log_path)
		self.init_to_assignment()
		# # # 同步返回参数。
		self.callback_data = self.CFR.format_to_sync()
		# # # 解析接口参数。
		if not self.CPR.parse_to_interface(source_dict):
			self.callback_data['msg'] = "请通知技术检查接口数据参数。"
			return self.callback_data
		self.logger.info(source_dict)
		# # # 启动爬虫，建立header。
		self.RCR.set_to_session()
		self.RCR.set_to_proxy(enable_proxy, address)
		self.user_agent, self.init_header = self.RCR.build_to_header("none")
		# # # 主体流程。
		for i in self.PMR.currency_route.items():
			# 判断货币，
			if i[0] == self.CPR.currency:
				self.dep = i[1][0]  # 第一程 出发地
				self.arr = i[1][1]  # 第一程 到达地
		self.baggage_data = []
		
		if self.set_to_proxy():
			if self.query_from_home():
				if self.query_from_detail():
					if self.submit_passenger():
						if self.collect_to_luggage():
							if self.return_to_data():
								self.logger.removeHandler(self.handler)
								return self.callback_data
		
		self.callback_data['msg'] = self.callback_msg
		self.logger.removeHandler(self.handler)
		return self.callback_data
	
	def set_to_proxy(self, count: int = 0, max_count: int = 3) -> bool:
		"""切换代理
        :param count:  重试次数
        :param max_count:  重试最大次数
        :return:  bool
        """
		if count >= max_count:
			return False
		else:
			# 获取代理， 并配置代理
			self.RCR.url = 'http://cloudmonitorproxy.51kongtie.com/Proxy/getProxyByServiceType?proxyNum=1&serviceType=4'
			self.RCR.header = self.BFR.format_to_same(self.init_header)
			self.RCR.param_data = None
			if self.RCR.request_to_get('json'):
				for ip in self.RCR.page_source:
					if ip.get('proxyIP'):
						proxy = "http://yunku:123@" + str(ip.get('proxyIP')) + ":" + str(ip.get('prot'))
						self.RCR.set_to_proxy(enable_proxy=True, address=proxy)
						return True
					else:
						self.logger.info("请求代理有问题")
			else:
				self.logger.info("请求代理有问题")
			
			self.logger.info(f"代理第{count + 1}次超时或者错误(*>﹏<*)【proxy】")
			self.callback_msg = f"代理第{count + 1}次超时或者错误"
			return self.set_to_proxy(count + 1, max_count)
	
	def query_from_home(self, count: int = 0, max_count: int = 3) -> bool:
		"""首页查询航班流程
        :param count:  重试次数
        :param max_count:  重试最大次数
        :return:  bool
        """
		if count >= max_count:
			self.callback_msg = "首页超时或者错误"
			return False
		else:
			# # # # 爬取首页
			self.RCR.url = "https://book.cebupacificair.com/"
			self.RCR.param_data = None
			self.RCR.header = self.BFR.format_to_same(self.init_header)
			self.RCR.header.update({
				# "Host": "book.cebupacificair.com",
				'Upgrade-Insecure-Requests': '1',
			})
			if self.RCR.request_to_get(is_redirect=True):
				self.RCR.url = "https://book.cebupacificair.com/Flight/QueueItRedirect"
				self.RCR.param_data = None
				self.RCR.header = self.BFR.format_to_same(self.init_header)
				self.RCR.header.update({
					# "Host": "book.cebupacificair.com",
					'Referer': 'https://book.cebupacificair.com/',
					'Upgrade-Insecure-Requests': '1',
				})
				if self.RCR.request_to_get(is_redirect=True):
					self.RCR.url = "https://book.cebupacificair.com/"
					self.RCR.param_data = None
					self.RCR.header = self.BFR.format_to_same(self.init_header)
					self.RCR.header.update({
						# "Host": "book.cebupacificair.com",
						'Upgrade-Insecure-Requests': '1',
					})
					if self.RCR.request_to_get(is_redirect=True):
						self.RCR.url = "https://book.cebupacificair.com/Flight/QueueItRedirect"
						self.RCR.param_data = None
						self.RCR.header = self.BFR.format_to_same(self.init_header)
						self.RCR.header.update({
							# "Host": "book.cebupacificair.com",
							'Referer': 'https://book.cebupacificair.com/',
							'Upgrade-Insecure-Requests': '1',
						})
						if self.RCR.request_to_get(is_redirect=True):
							self.RCR.url, temp = self.BPR.parse_to_regex('window\.location\=\'(.*?)\'\}\)',
							                                             self.RCR.page_source)
							print(self.RCR.url)
							if self.RCR.url:
								self.RCR.param_data = None
								self.RCR.header = self.BFR.format_to_same(self.init_header)
								self.RCR.header.update({
									# "Host": "cebupacificair.queue-it.net",
									'Upgrade-Insecure-Requests': '1',
								})
								if self.RCR.request_to_get(is_redirect=True):
									if "QueueItRedirect" in self.RCR.page_source:
										if self.redirect():
											return True
				self.set_to_proxy()
				return self.query_from_home(count + 1, max_count)
	
	def query_from_detail(self, count: int = 0, max_count: int = 4) -> bool:
		"""查询详情信息流程
        :param count:  重试次数
        :param max_count:  重试最大次数
        :return:  bool
        """
		if count >= max_count:
			self.callback_msg = f"查询详情信息流程失败【{self.RCR.url}】"
			return False
		else:
			if self.select():
				if "/Flight/Select" in self.RCR.page_source:
					self.RCR.url = "https://book.cebupacificair.com/Flight/Select"
					flight_date = self.DFR.format_to_transform(self.CPR.flight_date, "%Y%m%d")
					flight_date = flight_date.strftime("%Y-%m-%d")
					self.RCR.param_data = (
						('o1', self.dep),  # 第一程航线 规定货币
						('d1', self.arr),
						('o2', self.CPR.departure_code),  # 指定行李航线
						('d2', self.CPR.arrival_code),
						('dd1', flight_date),  # 第一程航线时间
						('dd2', flight_date),  # 指定行李航线日期
						('ADT', '1'),
						('CHD', '0'),
						('INF', '0'),
						('inl', '0'),
						('pos', 'cebu.us'),
						('culture', ''),
						('p', ''),
					)
					self.RCR.header = self.BFR.format_to_same(self.init_header)
					self.RCR.header.update({
						# "Host": "book.cebupacificair.com",
						'Referer': 'https://www.cebupacificair.com/en-us',
						'Upgrade-Insecure-Requests': '1',
					})
					if self.RCR.request_to_get(is_redirect=True):
						if len(self.RCR.page_source) > 10000:
							pass
						else:
							return self.query_from_detail(count + 1, max_count)
				# self.RCR.url = "https://book.cebupacificair.com/Flight/InternalSelect"
				# self.RCR.param_data = (
				#     ('o1', self.depart_col_dep),  # 第一程航线 规定货币
				#     ('d1', self.depart_col_arr),
				#     ('o2', self.dep),  # 指定行李航线
				#     ('d2', self.arr),
				#     ('dd1', self.depart_col_date),  # 第一程航线时间
				#     ('p', ''),
				#     ('dd2', self.return_col_date),  # 指定行李航线日期
				#     ('ADT', '1'),
				#     ('CHD', '0'),
				#     ('INF', '0'),
				#     ('s', 'true'),
				#     ('mon', 'true'),
				# )
			if self.page_verify(str(self.RCR.page_source)):
				self.callback_msg = "出现验证码"
				self.logger.info(self.callback_msg)
				self.set_to_proxy()
				return self.query_from_detail(count + 1, max_count)
			else:
				self.RCR.url = "https://book.cebupacificair.com/Flight/Select"
				self.RCR.param_data = None
				self.RCR.header = self.BFR.format_to_same(self.init_header)
				self.RCR.header.update({
					# "Host": "book.cebupacificair.com",
					'Referer': "https://book.cebupacificair.com/Flight/InternalSelect",
					'Upgrade-Insecure-Requests': '1',
				})
				if self.RCR.request_to_get():
					if self.page_verify(str(self.RCR.page_source)):
						self.callback_msg = "出现验证码"
						self.logger.info(self.callback_msg)
						self.set_to_proxy()
						return self.query_from_detail(count + 1, max_count)
					# 第一程是否有航班， 如果有航班，则跳过，
					# 否则提取第一程航班的日期， 判断哪一天有航班，进行重新搜索
					exit_fligth, exit_fligth_list = self.DPR.parse_to_attributes(
						"text", "css", '[id="depart-table"] [class="avail-info-no-flights"] h3',
						self.RCR.page_source)
					if "flights for this day are either sold out or unavailable" in str(
							exit_fligth_list):
						return False
					# 第二程是否有有航班
					exit_fligth, exit_fligth_list = self.DPR.parse_to_attributes(
						"text", "css", '[id="return-table"] [class="avail-info-no-flights"] h3',
						self.RCR.page_source)
					# 判断第二程  (指定行李航线) ， 当前日期是否有航班
					if "flights for this day are either sold out or unavailable" in str(
							exit_fligth_list):
						return False
					# 第一程 航班   # 选择第一程航班
					self.dep_key, dep_key_list = self.DPR.parse_to_attributes("value", "css",
					                                                          '[id*="trip_0_date_0_flight"]',
					                                                          self.RCR.page_source)
					# 第二程（行李行程）   # 选择第二程航班
					self.return_key, return_key_list = self.DPR.parse_to_attributes("value", "css",
					                                                                '[id*="trip_1_date_0_flight"]',
					                                                                self.RCR.page_source)
					bookingkey, bookingkey_list = self.DPR.parse_to_attributes("value", "css",
					                                                           '[class="bookingKey"][name="bookingKey"]',
					                                                           self.RCR.page_source)
					if dep_key_list and return_key_list:
						self.RCR.url = "https://book.cebupacificair.com/Flight/Select"
						self.RCR.header = self.BFR.format_to_same(self.init_header)
						self.RCR.post_data = {
							'cebSellBundleSsrs.BundleTypeSelectionDepart': '',
							'cebSellBundleSsrs.BundleTypeSelectionDepart': '',
							'cebSellBundleSsrs.BundleTypeSelectionReturn': '',
							'cebSellBundleSsrs.BundleTypeSelectionReturn': '',
							'cebAvailability.MarketFareKeys[0]': self.dep_key,
							'cebAvailability.MarketFareKeys[1]': self.return_key,
							'bookingKey': bookingkey,
						}
						self.RCR.header.update({
							'Upgrade-Insecure-Requests': '1',
							# "Host": "book.cebupacificair.com",
							'Origin': 'https://book.cebupacificair.com',
							'Content-Type': 'application/x-www-form-urlencoded',
							'Referer': 'https://book.cebupacificair.com/Flight/Select',
						})
						if self.RCR.request_to_post():
							self.RCR.url = "https://book.cebupacificair.com/Passengers/Edit"
							self.RCR.header = self.BFR.format_to_same(self.init_header)
							self.RCR.post_data = None
							self.RCR.header.update({
								'Upgrade-Insecure-Requests': '1',
								# "Host": "book.cebupacificair.com",
								'Referer': 'https://book.cebupacificair.com/Flight/Select',
							})
							if self.RCR.request_to_get():
								if self.page_verify(str(self.RCR.page_source)):
									self.callback_msg = f"出现验证码【{self.RCR.url}】"
									self.set_to_proxy()
									# self.ssh.get_server_ip()
									# self.RCR.set_to_proxy(enable_proxy=True,
									#                       address='http://yunku:123@{}:3138'.format(
									#                           self.ssh.proxy_ip))
									return self.query_from_detail(count + 1, max_count)
								self.temp_source = self.BFR.format_to_same(self.RCR.page_source)
								return True
					else:
						# 切换日期，重新搜索
						return self.query_from_detail(count + 1, max_count)
				else:
					return self.query_from_detail(count + 1, max_count)
		self.callback_msg = "获取航班信息失败"
		return False
	
	def select(self, count: int = 0, max_count: int = 2):
		if count >= max_count:
			return False
		self.RCR.set_to_cookies(is_domain=False,
		                        cookie_list=[{"name": 'rxvt', "value": '1571913336109|1571911126551'},
		                                     {"name": 'dtPC',
		                                      "value": '3$511318414_538h-vDEEMKMFPGMMCLFJGJJNIGHOALCGAADKN'},
		                                     {"name": 'dtCookie',
		                                      "value": '3$213E3E4F4BA7C4D180DA7585F275723D|b471fd2b229e5313|1'},
		                                     {"name": 'bid_cap9kylkxexvqbwfljqctlwjpvukqvde',
		                                      "value": '6d2a3485-58de-4e02-8eac-f5a73468a9e4'},
		                                     ])
		self.RCR.url = "https://book.cebupacificair.com/Flight/InternalSelect"
		flight_date = self.DFR.format_to_transform(self.CPR.flight_date, "%Y%m%d")
		flight_date = flight_date.strftime("%Y-%m-%d")
		self.RCR.param_data = (
			('o1', self.dep),  # 第一程航线 规定货币
			('d1', self.arr),
			('o2', self.CPR.departure_code),  # 指定行李航线
			('d2', self.CPR.arrival_code),
			('dd1', flight_date),  # 第一程航线时间
			('p', ''),
			('dd2', flight_date),  # 指定行李航线日期
			('ADT', '1'),
			('CHD', '0'),
			('INF', '0'),
			('s', 'true'),
			('mon', 'true'),
		)
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			# "Host": "book.cebupacificair.com",
			'Referer': "https://book.cebupacificair.com/",
			'Upgrade-Insecure-Requests': '1',
			
		})
		if self.RCR.request_to_get(is_redirect=False):
			if "Flight/Select" in self.RCR.page_source:
				return True
			else:
				return self.select(count + 1, max_count)
	
	def redirect(self):
		self.RCR.url = "https://book.cebupacificair.com/Flight/QueueItRedirect"
		self.RCR.param_data = None
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			# 'Host': 'book.cebupacificair.com',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Upgrade-Insecure-Requests': '1',
			'Accept': 'text/plain, */*; q=0.01',
			'Referer': 'https://book.cebupacificair.com/',
		})
		if self.RCR.request_to_get(is_redirect=True):
			return True
	
	def submit_passenger(self, count: int = 0, max_count: int = 3):
		if count >= max_count:
			return False
		else:
			bookingkey, bookingkey_list = self.DPR.parse_to_attributes("value", "css",
			                                                           'input[name="bookingKey"]',
			                                                           self.temp_source)
			if not bookingkey:
				self.callback_msg = f"bookingkey 获取失败"
				return self.submit_passenger(count + 1, max_count)
			PaxSSRNotes, PaxSSRNotes_list = self.DPR.parse_to_attributes("value", "css",
			                                                             '[id*="firstSpecialAssistanceId0_"] option:nth-child(2)',
			                                                             self.temp_source)
			if not PaxSSRNotes:
				self.callback_msg = f"PaxSSRNotes 获取失败"
				return self.submit_passenger(count + 1, max_count)
			self.RCR.timeout = 20
			self.RCR.url = "https://book.cebupacificair.com/Passengers/Update"
			self.RCR.header = self.BFR.format_to_same(self.init_header)
			self.RCR.post_data = {
				'cebPassengers.travelSureRefund': 'False',
				'cebPassengers[0].PassengerNumber': '0',
				'cebPassengers[0].Name.Title': 'MR',
				'cebPassengers[0].Info.Gender': '1',
				'cebPassengers[0].Name.First': 'Shi',
				'cebPassengers[0].Name.Last': 'San',
				'cebPassengers[0].date_of_birth_month_0': '1',
				'cebPassengers[0].date_of_birth_day_0': '4',
				'cebPassengers[0].date_of_birth_year_0': '1996',
				'cebPassengers[0].TypeInfo.DateOfBirth': '1996-01-04',
				'cebPassengers[0].Info.Nationality': 'CN',
				'cebGetGoNumber.DocNumbers[0]': 'E834751327',
				'cebGetGoNumber.DocTypeCode': 'OAFF',
				'cebGetGoQuickRegistration.EmailAddresses[0]': '',
				'cebGetGoQuickRegistration.PassengerNumbers': '0',
				'cebPassengers[0].TypeInfo.PaxType': 'ADT',
				'cebPassengers[0].TypeInfo.PaxType': 'ADT',
				'cebOEC.DocNumbers[0]': '',
				'cebOEC.IssuedByCode[0]': 'PH',
				'cebOEC.DocTypeCode': 'OEC',
				'cebPassengers[0].Info.ResidentCountry': 'CN',
				'cebPassengers[0].RepresentationAgreement': 'on',
				'cebPassport.DocNumbers[0]': '',
				'cebPassport.IssuedByCode[0]': '',
				'cebPassport.date_of_expiration_month_0': '',
				'cebPassport.date_of_expiration_day_0': '',
				'cebPassport.date_of_expiration_year_0': '',
				'cebPassport.ExpirationDate[0]': '',
				'cebPassport.DocTypeCode': 'P',
				'specialAssistance': '0',
				'Please select': '',
				'Please select': '',
				'cebSpecialAssistance.PaxSSRNotes[{}]'.format(PaxSSRNotes_list[0]): '',
				'cebGdpr.Accept': 'true',
				'bookingKey': bookingkey,
			}
			if len(PaxSSRNotes_list) == 2:
				self.RCR.post_data['cebSpecialAssistance.PaxSSRNotes[{}]'.format(PaxSSRNotes_list[1])] = ""
			self.RCR.header.update({
				# 'Host': 'book.cebupacificair.com',
				'Origin': 'https://book.cebupacificair.com',
				'Upgrade-Insecure-Requests': '1',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Referer': 'https://book.cebupacificair.com/Passengers/Edit',
			})
			if self.RCR.request_to_post():
				self.RCR.url = "https://book.cebupacificair.com/Extras/Add"
				self.RCR.header = self.BFR.format_to_same(self.init_header)
				self.RCR.header.update({
					# 'Host': 'book.cebupacificair.com',
					'Upgrade-Insecure-Requests': '1',
					'Referer': 'https://book.cebupacificair.com/Passengers/Edit',
				})
				if self.RCR.request_to_get():
					if self.page_verify(str(self.RCR.page_source)):
						self.callback_msg = f"出现验证码 【 {self.RCR.url} 】"
						self.set_to_proxy()
						# self.ssh.get_server_ip()
						# self.RCR.set_to_proxy(enable_proxy=True,
						#                       address='http://yunku:123@{}:3138'.format(self.ssh.proxy_ip))
						return self.submit_passenger(count + 1, max_count)
					if "bag-weight-label" in self.RCR.page_source:
						return True
					else:
						self.callback_msg = "行李获取失败"
						return self.submit_passenger(count + 1, max_count)
			else:
				self.callback_msg = f"【 Update 】请求失败 【 {self.RCR.url} 】"
				return self.submit_passenger(count + 1, max_count)
	
	def collect_to_luggage(self, count: int = 0, max_count: int = 1) -> bool:
		"""收集行李信息
        :return:  bool
        """
		luggage_weight, luggages_weight_list = self.DPR.parse_to_attributes("text", "css",
		                                                                    "div[class='addons-passenger-flight-content'][data-flight-index='1'] span[class='bag-weight-label']",
		                                                                    str(self.RCR.page_source))
		luggages_price, luggages_price_list = self.DPR.parse_to_attributes("text", "css",
		                                                                   "div[class='addons-passenger-flight-content'][data-flight-index='1'] div[class='bag-details-amount']",
		                                                                   str(self.RCR.page_source))
		luggage_currency, temp_list = self.BPR.parse_to_regex("([A-Za-z]{1,})", str(luggages_price))
		if len(luggages_weight_list) == len(luggages_price_list):
			for i in range(len(luggages_price_list)):
				price, price_list = self.BPR.parse_to_regex("([^A-Za-z]{1,})", str(luggages_price_list[i]))
				try:
					dict_temp = {}
					dict_temp['departure_aircode'] = self.CPR.departure_code
					dict_temp['arrival_aircode'] = self.CPR.arrival_code
					dict_temp['luggages_weight'] = luggages_weight_list[i].replace(" ", '')  # 行李重量
					dict_temp['luggage_currency'] = luggage_currency  # 原始货币
					dict_temp['foreign_price'] = price.replace(" ", '')  # 行李价格
					dict_temp['carrier'] = "5J"  # 行李获取的日期
					# dict_temp['rmb_price'] = rmb_price                       # 人民币价格
					self.baggage_data.append(dict_temp)
				
				except Exception as ex:
					self.callback_msg = ex
					self.logger.info(self.callback_msg)
					return False
			self.callback_msg = "行李抓取成功"
			return True
		self.callback_msg = "行李数据有误"
		return False
	
	def page_verify(self, result):
		# 判断是否出现验证码
		if "data:image/png;base64" in result:
			verify_code, temp_list = self.DPR.parse_to_attributes(
				"src", "css", "img", self.RCR.page_source)
			self.callback_msg = "出现验证码 【{}】".format(str(temp_list).split(',')[0])
			# self.ssh.get_server_ip()
			self.set_to_proxy()
			return True
		else:
			return False
	
	def return_to_data(self) -> bool:
		"""返回结果数据
        :return:  bool
        """
		self.callback_data["success"] = "true"
		self.callback_data['msg'] = "更新成功"
		self.callback_data["baggage"] = self.baggage_data  # 行李数据
		self.logger.info(self.callback_data)
		return True