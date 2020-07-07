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
from collector.persvy_mirror import PersVYMirror


class PersVYScraper(RequestWorker):
	"""VY采集器，VY网站流程交互，5分钟刷abck，10分钟封禁解禁。"""
	
	def __init__(self) -> None:
		RequestWorker.__init__(self)
		self.RCR = RequestCrawler()  # 请求爬行器。
		self.AFR = AESFormatter()  # AES格式器。
		self.BFR = BasicFormatter()  # 基础格式器。
		self.BPR = BasicParser()  # 基础解析器。
		self.CFR = CallBackFormatter()  # 回调格式器。
		self.CPR = CallInParser(False)  # 接入解析器。
		self.DFR = DateFormatter()  # 日期格式器。
		self.DPR = DomParser()  # 文档解析器。
		self.PMR = PersVYMirror()  # VY镜像器。
		# # # 返回中用到的变量。
		self.return_baggage: list = []  # 行李数据。
	
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
		# # # 启动爬虫，建立header，更新联系电话。
		self.RCR.set_to_session()
		self.RCR.set_to_proxy(enable_proxy, address)
		self.user_agent, self.init_header = self.RCR.build_to_header("none")
		self.CPR.currency = "EUR"
		# # # 主体流程。
		if self.process_to_query(max_count=self.retry_count):
			if self.process_to_passenger(max_count=self.retry_count):
				self.process_to_return()
				self.logger.removeHandler(self.handler)
				return self.callback_data
		# # # 错误返回。
		self.callback_data['msg'] = self.callback_msg
		# self.callback_data['msg'] = "解决问题中，请手工支付。"
		self.logger.info(self.callback_data)
		self.logger.removeHandler(self.handler)
		return self.callback_data
	
	def process_to_query(self, count: int = 0, max_count: int = 1) -> bool:
		"""Query process. 查询过程。

		Args:
		    count (int): 累计计数。
		    max_count (int): 最大计数。

		Returns:
		    bool
		"""
		if count >= max_count:
			return False
		else:
			# # # 更新超时时间。
			self.RCR.timeout = 10
			# # # 请求接口服务。
			self.RCR.url = 'http://45.81.129.1:33334/produce/vy/'
			self.RCR.param_data = None
			self.RCR.header = None
			self.RCR.post_data = {"vy": "abck"}
			if not self.RCR.request_to_post("json", "json"):
				self.logger.info(f"请求刷值地址失败(*>﹏<*)【45.81.129.1:33334】")
				self.callback_msg = "请求刷值地址失败，请通知技术检查程序。"
				return self.process_to_query(count + 1, max_count)
			# # # 获取abck。
			cookie = self.RCR.page_source.get("value")
			if not cookie:
				self.logger.info(f"刷值数量不够用(*>﹏<*)【45.81.129.1:33334】")
				self.callback_msg = "刷值数量不够用，请通知技术检查程序。"
				return self.process_to_query(count + 1, max_count)
			# # # 设置cookie。
			cookies = [{'domain': 'vueling.com', 'name': '_abck', 'path': '/', 'value': cookie}]
			self.RCR.set_to_cookies(True, cookies)
			# # # 更新超时时间。
			self.RCR.timeout = 40
			# # # 生成header, 获取首页。
			self.RCR.url = "https://tickets.vueling.com/"
			self.RCR.param_data = (
				("culture", "en-GB"),
			)
			self.RCR.header = self.BFR.format_to_same(self.init_header)
			self.RCR.header.update({
				"Host": "tickets.vueling.com",
				"Upgrade-Insecure-Requests": "1",
			})
			if self.RCR.request_to_get(is_redirect=True):
				# # # 转换接口日期和7天后日期，出发地到达地名字。
				flight_date = self.DFR.format_to_transform(self.CPR.departure_date, "%Y%m%d")
				future_date = self.DFR.format_to_now(custom_days=7)
				departure = self.PMR.select_to_name(self.CPR.departure_code)
				arrival = self.PMR.select_to_name(self.CPR.arrival_code)
				# # # 继承header, 点击查询航班数据。
				self.RCR.url = "https://tickets.vueling.com/"
				self.RCR.header.update({
					"Content-Type": "application/x-www-form-urlencoded",
					"Origin": "https://tickets.vueling.com",
					"Referer": "https://tickets.vueling.com/?culture=en-GB",
				})
				# # # 基础参数。
				param_batch = [
					("__EVENTTARGET", False, "AvailabilitySearchInputSearchView$LinkButtonNewSearch"),
					("__EVENTARGUMENT", True, "#eventArgument"), ("__VIEWSTATE", True, "#viewState"),
					("pageToken", True, "input[name=pageToken]"),
					("AvailabilitySearchInputSearchView$RadioButtonMarketStructure", False, "OneWay"),
					("AvailabilitySearchInputSearchView$TextBoxMarketOrigin1", False, departure),
					("AvailabilitySearchInputSearchView$TextBoxMarketDestination1", False, arrival),
					("date_picker", False, flight_date.strftime("%Y-%m-%d")),
					("AvailabilitySearchInputSearchView$DropDownListMarketDay1", False, flight_date.strftime("%d")),
					("AvailabilitySearchInputSearchView$DropDownListMarketMonth1",
					 False, flight_date.strftime("%Y-%m")),
					("date_picker", False, flight_date.strftime("%Y-%m-%d")),
					("AvailabilitySearchInputSearchView$DropDownListMarketDay2", False, flight_date.strftime("%d")),
					("AvailabilitySearchInputSearchView$DropDownListMarketMonth2",
					 False, flight_date.strftime("%Y-%m")),
					("AvailabilitySearchInputSearchView$TextBoxMarketOrigin2", False, "From"),
					("AvailabilitySearchInputSearchView$TextBoxMarketDestination2", False, "Destination"),
					("AvailabilitySearchInputSearchView$DropDownListPassengerType_ADT", False, "1"),
					("AvailabilitySearchInputSearchView$DropDownListPassengerType_CHD", False, "0"),
					("AvailabilitySearchInputSearchView$DropDownListPassengerType_INFANT", False, "0"),
					("AvailabilitySearchInputSearchView$ResidentFamNumSelector", False, ""),
					("AvailabilitySearchInputSearchView$ExtraSeat", False, ""),
					("AvailabilitySearchInputSearchView$DropDownListSearchBy", False, "columnView"),
					("departureStationCode1", False, self.CPR.departure_code),
					("arrivalStationCode1", False, self.CPR.arrival_code),
					("ErroneousWordOrigin1", False, ""), ("SelectedSuggestionOrigin1", False, ""),
					("ErroneousWordDestination1", False, ""), ("SelectedSuggestionDestination1", False, ""),
					("versionTd", False, ""), ("departureStationCode2", False, ""), ("arrivalStationCode2", False, ""),
					("ErroneousWordOrigin2", False, ""), ("SelectedSuggestionOrigin2", False, ""),
					("ErroneousWordDestination2", False, ""), ("SelectedSuggestionDestination2", False, ""),
					("stvMonetateExperiment", False, ""), ("stvVersion", False, ""),
				]
				# # # 生成请求参数。
				self.RCR.post_data = self.DPR.parse_to_batch("value", "css", param_batch, self.RCR.page_source)
				if self.RCR.request_to_post(is_redirect=True):
					# # # 查询封禁信息。
					error, temp_list = self.DPR.parse_to_attributes("text", "css", "title", self.RCR.page_source)
					if error and "Access Denied" in error:
						self.logger.info("abck遭到封禁，需要查看刷值服务(*>﹏<*)【query】")
						self.callback_msg = "遭到封禁，请通知技术检查程序。"
						return self.process_to_query(count + 1, max_count)
					# # # 解析航班数据。
					table, temp_list = self.DPR.parse_to_attributes(
						"id", "css", "#availabilityTable0", self.RCR.page_source)
					table_new, temp_list = self.DPR.parse_to_attributes(
						"id", "css", "#flightCardsContainer", self.RCR.page_source)
					# # # 设置匹配航班标识和坐席标识。
					key = ""
					seats_list = []
					if table:
						key_temp, key_list = self.DPR.parse_to_attributes(
							"value", "css",
							f"#availabilityTable0 #marketOption input[name='ControlGroupScheduleSelectView"
							f"$AvailabilityInputScheduleSelectView$market1']", self.RCR.page_source)
						for i in key_list:
							if "^" in i:
								continue
							else:
								seats_list.append(i)
					elif table_new:
						key_temp, key_list = self.DPR.parse_to_attributes(
							"basicsellkey", "css",
							f"#flightCardsContainer #flightCardInfo input[idcard]", self.RCR.page_source)
						for i in key_list:
							if "^" in i:
								continue
							else:
								seats_list.append(i)
					else:
						self.logger.info(
							f"获取不到航线数据(*>﹏<*)【{self.CPR.departure_code}】【{self.CPR.arrival_code}】")
						self.callback_msg = "该航线航班已售完。"
						return False
					
					if not seats_list:
						self.logger.info(f"该航班座位已售完(*>﹏<*)【】")
						self.callback_msg = "该航班座位已售完。"
						return False
					
					for i in seats_list:
						if "PB01" in i:
							key = i
							break
					if not key:
						self.logger.info(f"最低价座位已售完(*>﹏<*)【】")
						self.callback_msg = "最低价座位已售完。"
						return False
					print(key)
					# # # 继承header, 选完航班点击跳过查询。
					self.RCR.url = "https://tickets.vueling.com/ScheduleSelect.aspx"
					self.RCR.header.update({"Referer": "https://tickets.vueling.com/ScheduleSelect.aspx"})
					# # # 基础参数。
					param_batch = [
						("__EVENTTARGET", False,
						 "ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView$LinkButtonSubmit"),
						("__EVENTARGUMENT", True, "#eventArgument"), ("__VIEWSTATE", True, "#viewState"),
						("pageToken", True, "input[name=pageToken]"),
						("monetateFilterExperiment", False, ""),
						("ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView"
						 "$PromoCodeScheduleSelectView$inputSelectedMarkets0", False, ""),
						("ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView"
						 "$PromoCodeScheduleSelectView$inputSelectedMarkets1", False, ""),
						("ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView"
						 "$PromoCodeScheduleSelectView$textBoxPromoVYCode", False, ""),
						("dateselected0", False, flight_date.strftime("%m/%d/%Y")),
						("ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView"
						 "$HiddenFieldTabIndex1", False, "4"),
						("ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView$market1",
						 False, key),
						("ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView"
						 "$AgreementInputScheduleSelectView$CheckBoxAgreement", False, "on"),
						("ControlGroupScheduleSelectView$AvailabilityInputScheduleSelectView"
						 "$PromoUniversalMarkCustomControlScheduleSelectView$PromoUniversalhiddenField", False, ""),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$RadioButtonMarketStructure", False, "OneWay"),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$TextBoxMarketOrigin1", False, departure),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$TextBoxMarketDestination1", False, arrival),
						("date_picker", False, flight_date.strftime("%Y-%m-%d")),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListMarketDay1", False, flight_date.strftime("%d")),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListMarketMonth1", False, flight_date.strftime("%Y-%m")),
						("date_picker", False, future_date.strftime("%Y-%m-%d")),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListMarketDay2", False, future_date.strftime("%d")),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListMarketMonth2", False, future_date.strftime("%Y-%m")),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$TextBoxMarketOrigin2", False, "From"),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$TextBoxMarketDestination2", False, "Destination"),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListPassengerType_ADT", False, "1"),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListPassengerType_CHD", False, "0"),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListPassengerType_INFANT", False, "0"),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$ResidentFamNumSelector", False, ""),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$ExtraSeat", False, ""),
						("CONTROLGROUPAVAILABILTYSEARCHINPUTSCHEDULESELECTVIEW$AvailabilityScheduleSelectView"
						 "$DropDownListSearchBy", False, "columnView"),
						("departureStationCode1", False, self.CPR.departure_code),
						("arrivalStationCode1", False, self.CPR.arrival_code),
						("ErroneousWordOrigin1", False, ""), ("SelectedSuggestionOrigin1", False, ""),
						("ErroneousWordDestination1", False, ""), ("SelectedSuggestionDestination1", False, ""),
						("versionTd", False, ""), ("departureStationCode2", False, ""),
						("arrivalStationCode2", False, ""), ("ErroneousWordOrigin2", False, ""),
						("SelectedSuggestionOrigin2", False, ""), ("ErroneousWordDestination2", False, ""),
						("SelectedSuggestionDestination2", False, ""), ("stvMonetateExperiment", False, ""),
						("stvVersion", False, ""),
						("SBSidebarScheduleSelectView$CurrencyConverterScheduleSelectView"
						 "$DropDownListConversionCurrency:", False, self.CPR.currency),
					]
					# # # 生成请求参数。
					self.RCR.post_data = self.DPR.parse_to_batch("value", "css", param_batch, self.RCR.page_source)
					if self.RCR.request_to_post(is_redirect=True):
						# # # 查询封禁信息。
						error, temp_list = self.DPR.parse_to_attributes("text", "css", "title", self.RCR.page_source)
						if error and "Access Denied" in error:
							self.logger.info("abck遭到封禁，需要查看刷值服务(*>﹏<*)【query】")
							self.callback_msg = "遭到封禁，请通知技术检查程序。"
							return self.process_to_query(count + 1, max_count)
						# # # 安全通过。
						self.RCR.copy_source = self.BFR.format_to_same(self.RCR.page_source)
						return True
			# # # 错误重试。
			self.logger.info(f"提交查询第{count + 1}次超时(*>﹏<*)【query】")
			self.callback_msg = f"提交查询第{count + 1}次超时，请重试。"
			return self.process_to_query(count + 1, max_count)
	
	def process_to_passenger(self, count: int = 0, max_count: int = 1) -> bool:
		"""Passenger process. 乘客过程。

		Args:
			count (int): 累计计数。
			max_count (int): 最大计数。

		Returns:
			bool
		"""
		if count >= max_count:
			return False
		else:
			# # # 生成header, 添加乘客信息。
			self.RCR.url = "https://tickets.vueling.com/PassengersInformation.aspx"
			self.RCR.header = self.BFR.format_to_same(self.init_header)
			self.RCR.header.update({
				"Content-Type": "application/x-www-form-urlencoded",
				"Origin": "https://tickets.vueling.com",
				"Referer": "https://tickets.vueling.com/PassengersInformation.aspx",
				"Upgrade-Insecure-Requests": "1"
			})
			# # # 基础参数。
			param_batch = [
				("__EVENTTARGET", False,
				 "ContactViewControlGroupMainContact$LinkButtonSubmit"),
				("__EVENTARGUMENT", True, "#eventArgument"), ("__VIEWSTATE", True, "#viewState"),
				("pageToken", True, "input[name=pageToken]"),
				("DropDownListAviosLogin", True, "#DropDownListAviosLogin"),
				("ContactViewControlGroupMainContact$ContactViewMemberLoginAndSliderPwAContactView"
				 "$ContactViewMemberLoginContactView$TextBoxUserID", False, ""),
				("ContactViewControlGroupMainContact$ContactViewMemberLoginAndSliderPwAContactView"
				 "$ContactViewMemberLoginContactView$PasswordFieldPassword", False, ""),
				
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$ContactViewControlGroupMainContact_BoxPassengerInformationView_"
				 "BoxContactInformationViewHtmlInputHiddenAntiForgeryTokenField", True,
				 "#ContactViewControlGroupMainContact_BoxPassengerInformationView_BoxContactInformationView"
				 "_ContactViewControlGroupMainContact_BoxPassengerInformationView_"
				 "BoxContactInformationViewHtmlInputHiddenAntiForgeryTokenField"),
				
				("contact-info", False, "on"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$TextBoxFirstName", False, "hao"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$TextBoxLastName", False, "li"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$DropDownListCountry", False, "BZ"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$TextBoxCity", False, "beijing"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$DropDownListPrefix", False, "+501"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$PrefixCountryCode", False, "BZ"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$TextBoxHomePhone", False, "18613381111"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView$BoxContactInformationView"
				 "$TextBoxEmailAddress", False, "abc123@163.com"),
				("ContactViewControlGroupMainContact$BoxPassengerInformationView"
				 "$ContactViewItineraryDistributionInputViewCustomerContactViewHidden$Distribution", False, "2")
			]
			# # # 追加每个成人具体的参数。
			for n, v in enumerate(["1个人参数"]):
				adult_batch = [
					(f"ContactViewControlGroupMainContact$BoxPassengerInformationView$DropDownListTitle_{n}",
					 False, "MR"),
					(f"ContactViewControlGroupMainContact$BoxPassengerInformationView$TextBoxFirstName_{n}",
					 False, "hao"),
					(f"ContactViewControlGroupMainContact$BoxPassengerInformationView$TextBoxLastName_{n}",
					 False, "li"),
					(f"radioIsPMR_WCADT{n + 1}", False, "WCHC"),
					(f"radioGuideDogADT{n + 1}", False, "false"),
					(f"ContactViewControlGroupMainContact$BoxPassengerInformationView$TextBoxProgramNumber_{n}",
					 False, "")
				]
				# # # 追加每个成人具体的参数。
				param_batch.extend(adult_batch)
			# # # 生成请求参数。
			self.RCR.post_data = self.DPR.parse_to_batch("value", "css", param_batch, self.RCR.copy_source)
			if self.RCR.request_to_post(is_redirect=True):
				baggage_value, baggage_list = self.DPR.parse_to_attributes(
					"weight", "css", "span[id*='addWeightedBag']", self.RCR.page_source)
				for i in baggage_list:
					# # # 解析行李价格，按公斤比数取价格。
					kilogram = self.BFR.format_to_int(i)
					if kilogram < 20:
						continue
					price, temp_list = self.DPR.parse_to_attributes(
					"price", "css", f"#addWeightedBag{kilogram}Outbound", self.RCR.page_source)
					price = self.BFR.format_to_float(2, price)
					
					self.return_baggage.append({
						"carrier": "VY",
						"departure_aircode": self.CPR.departure_code,
						"arrival_aircode": self.CPR.arrival_code,
						"baggage_weight": kilogram,
						"foreign_currency": self.CPR.currency,
						"foreign_price": price,
					})

				return True
			# # # 错误重试。
			self.logger.info(f"添加乘客第{count + 1}次超时(*>﹏<*)【passenger】")
			self.callback_msg = f"添加乘客第{count + 1}次超时，请重试。"
			return self.process_to_passenger(count + 1, max_count)
	
	def process_to_return(self) -> bool:
		"""Return process. 返回过程。

		Returns:
			bool
		"""
		self.callback_data["success"] = "true"
		self.callback_data['msg'] = "更新成功"
		self.callback_data["baggages"] = self.return_baggage
		self.logger.info(self.callback_data)
		return True
