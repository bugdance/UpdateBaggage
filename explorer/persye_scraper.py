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
import time


class PersYEScraper(RequestWorker):
    """MM采集器, 5分钟刷abck，10分钟封禁解禁

    """
    
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
        if self.CPR.carrier == "ALL":
            self.CPR.carrier = ""
        # # # 主体流程。
        if self.process_to_login(max_count=self.retry_count):
            self.process_to_return()
            self.logger.removeHandler(self.handler)
            return self.callback_data
        # # # 错误返回。
        self.callback_data['msg'] = self.callback_msg
        # self.callback_data['msg'] = "解决问题中，请手工更新行李。"
        self.logger.info(self.callback_data)
        self.logger.removeHandler(self.handler)
        return self.callback_data

    def process_to_login(self, count: int = 0, max_count: int = 1) -> bool:
        """Login process. 登录过程。

		Returns:
			bool
		"""
        if count >= max_count:
            return False
        else:
            # # # 生成header，获取首页。
            self.RCR.url = 'http://flight.yeebooking.com/common/login'
            self.RCR.param_data = None
            self.RCR.header = self.BFR.format_to_same(self.init_header)
            self.RCR.header.update({
                "Host": "flight.yeebooking.com",
                "Upgrade-Insecure-Requests": "1"
            })
            if self.RCR.request_to_get():
                # # # 继承header，请求登录。
                self.RCR.url = 'http://flight.yeebooking.com/common/validate'
                self.RCR.header.update({
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Origin": "http://flight.yeebooking.com",
                    "Referer": "http://flight.yeebooking.com/common/login",
                })
                # # # 基础参数。
                self.RCR.post_data = [
                    ("companyFlag", "zouba"),
                    ("loginName", "lihao"),
                    ("password", "lihao_159753"),
                ]
                if self.RCR.request_to_post(status_code=302):
                    # # # 生成header，获取登陆后首页。
                    self.RCR.url = 'http://flight.yeebooking.com/common/index'
                    self.RCR.param_data = None
                    self.RCR.header = self.BFR.format_to_same(self.init_header)
                    self.RCR.header.update({
                        "Host": "flight.yeebooking.com",
                        "Referer": "http://flight.yeebooking.com/common/login",
                        "Upgrade-Insecure-Requests": "1"
                    })
                    if self.RCR.request_to_get():
                        # # # 继承header，请求航线列表页。
                        self.RCR.url = 'http://flight.yeebooking.com/yfp/routing-delivery/list'
                        self.RCR.header.update({
                            "Content-Type": "application/x-www-form-urlencoded",
                            "Origin": "http://flight.yeebooking.com",
                        })
                        self.RCR.post_data = [
                            ("departureAircode", ""),
                            ("arrivalAircode", ""),
                            ("airNameCode", self.CPR.carrier),
                            ("crawlerType", ""),
                            ("crawlerStatus", ""),
                            ("currentPage", "1"),
                            ("pageSize", "100"),
                        ]
                        if self.RCR.request_to_post():
                            time.sleep(5)
                            # # # 获取页数。
                            numbers, temp_list = self.BPR.parse_to_regex("totalSize:(.*?),", self.RCR.page_source)
                            numbers = self.BFR.format_to_int(numbers)
                            remainder = numbers % 100  # 余数。
                            page = numbers / 100
                            page = self.BFR.format_to_int(page)
                            # # # 如果有余数加1。
                            if remainder:
                                page += 1
                            # # # 循环解析所有页面。
                            for p in range(page):
                                self.RCR.url = 'http://flight.yeebooking.com/yfp/routing-delivery/list'
                                self.RCR.post_data = [
                                    ("departureAircode", ""),
                                    ("arrivalAircode", ""),
                                    ("airNameCode", self.CPR.carrier),
                                    ("crawlerType", ""),
                                    ("crawlerStatus", ""),
                                    ("currentPage", p+1),
                                    ("pageSize", "100"),
                                ]
                                if not self.RCR.request_to_post():
                                    # # # 错误重试。
                                    self.logger.info(f"请求登录第{count + 1}次超时(*>﹏<*)【login】")
                                    self.callback_msg = f"请求登录第{count + 1}次超时，请重试"
                                    return self.process_to_login(count + 1, max_count)
                                else:
                                    # # # 获取表格。
                                    table, table_list = self.DPR.parse_to_attributes(
                                        "text", "css", ".table.table-bordered tbody tr", self.RCR.page_source)
                                    # # # 循环取数据。
                                    for i in range(len(table_list)):
                                        carrier, temp_list = self.DPR.parse_to_attributes(
                                            "text", "css",
                                            f".table.table-bordered tbody tr:nth-child({i+1}) "
                                            f"td:nth-child(2) span", self.RCR.page_source)
                                        departure, temp_list = self.DPR.parse_to_attributes(
                                            "text", "css",
                                            f".table.table-bordered tbody tr:nth-child({i+1}) "
                                            f"td:nth-child(3) span", self.RCR.page_source)
                                        arrival, temp_list = self.DPR.parse_to_attributes(
                                            "text", "css",
                                            f".table.table-bordered tbody tr:nth-child({i+1}) "
                                            f"td:nth-child(4) span", self.RCR.page_source)
    
                                        self.return_baggage.append([carrier, departure, arrival, "CNY"])
                                        
                            return True
            # # # 错误重试。
            self.logger.info(f"请求登录第{count + 1}次超时(*>﹏<*)【login】")
            self.callback_msg = f"请求登录第{count + 1}次超时，请重试"
            return self.process_to_login(count + 1, max_count)

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