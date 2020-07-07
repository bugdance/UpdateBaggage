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
import random
import hashlib
from urllib.parse import urlencode
class PersF9Scraper(RequestWorker):
    """F9采集器，行李价格抓取
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

        self.baggage_data: list = []    # 行李数据
        self.verify_url: str = ""       # 验证地址
        self.temp_source: str = ""      # 临时源数据

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
        
        self.CPR.departure_date = self.DFR.format_to_transform(self.CPR.departure_date, "%Y%m%d")
        self.CPR.departure_date = self.CPR.departure_date.strftime("%m/%d/%Y")
        if self.query_from_home():
            if self.query_from_detail():
                if self.set_meal():
                    if self.query_from_seat():
                        if self.query_from_bags():
                            if self.collect_to_luggage():
                                if self.return_to_data():
                                    self.logger.removeHandler(self.handler)
                                    return self.callback_data
        self.callback_data['msg'] = self.callback_msg
        self.logger.info(self.callback_data)
        self.logger.removeHandler(self.handler)
        return self.callback_data
    
    def query_from_flight_date(self, count: int = 0, max_count: int = 3) -> bool:
        """查询航班日期
        :param count:  重试次数
        :param max_count:  重试最大次数
        :return:  bool
        """
        if count >= max_count:
            self.callback_msg = f"查询详情信息流程失败【{self.RCR.url}】"
            return False
        else:
            self.RCR.url = 'https://booking.flyfrontier.com/Flight/RetrieveSchedule'
            self.RCR.header = self.BFR.format_to_same(self.init_header)
            self.RCR.param_data = (
                ('calendarSelectableDays.Origin', self.CPR.departure_code),
                ('calendarSelectableDays.Destination', self.CPR.arrival_code),
                ('_', int(time.time())),
            )
            self.RCR.header.update({
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': 'https://www.flyfrontier.com/',
                'Origin': 'https://www.flyfrontier.com',
                'Sec-Fetch-Mode': 'cors',
            })
            if self.RCR.request_to_get(is_redirect=True, page_type='json'):
                flight_date = self.DFR.format_to_transform(self.CPR.departure_date, "%m/%d/%Y")
                flight_date = flight_date.strftime("%m/%d/%Y")
                n = 1
                if str(flight_date) in str(self.RCR.page_source):
                    dates, temp_list = self.BPR.parse_to_path("$..disabledDates", self.RCR.page_source)
                    for i in dates:
                        # 根据当前日期， 加一天
                        self.CPR.departure_date = self.DFR.format_to_custom(source_time=self.CPR.departure_date,
                                                                           source_format="%m/%d/%Y",
                                                                           custom_days=n)
                        self.CPR.departure_date = self.CPR.departure_date.strftime("%m/%d/%Y")
                        if str(self.CPR.departure_date) in str(self.RCR.page_source):
                            n += 1
                            continue
                        else:
                            return True
                    else:
                        self.callback_msg = f"未找到当前航线有日期的航班 | {self.CPR.departure_code} - {self.CPR.arrival_code}"
                        return False
                else:
                    return True
            self.callback_msg = f"查询航班日期失败【{self.RCR.url}】"
            return False
    def query_from_home(self, count: int = 0, max_count: int = 3) -> bool:
        """查询详情信息流程
        :param count:  重试次数
        :param max_count:  重试最大次数
        :return:  bool
        """
        if count >= max_count:
            self.callback_msg = f"查询详情信息流程失败【{self.RCR.url}】"
            return False
        else:
            # 判断航班日期是否有航班
            if self.query_from_flight_date():
                pass
            flight_date = self.DFR.format_to_transform(self.CPR.departure_date, "%m/%d/%Y")
            flight_date = flight_date.strftime("%b-%d-%Y").split('-')
            self.RCR.url = f"https://booking.flyfrontier.com/Flight/InternalSelect?o1={self.CPR.departure_code}&d1={self.CPR.arrival_code}&dd1={flight_date[0]}%20{flight_date[1]},%20{flight_date[2]}&ADT=1&mon=true&promo="
            self.RCR.header = self.BFR.format_to_same(self.init_header)
            self.RCR.header.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Host": "booking.flyfrontier.com",
                "Referer": "https://www.flyfrontier.com/",
                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                "Accept-Encoding": "gzip, deflate, br",
                "Upgrade-Insecure-Requests": "1",
            })
            if self.RCR.request_to_get(is_redirect=True):
                if "standardFareKey" in self.RCR.page_source:
                    self.temp_source = self.BFR.format_to_same(self.RCR.page_source)
                    self.frntrirdstl_get()
                    self.frntrirdstl_post()
                    return True
                elif "ibe-flight-na-container" in self.RCR.page_source and "ibe-flight-slider" in self.RCR.page_source:
                    self.callback_msg = f"当前航线无航班信息 | {self.CPR.departure_code} - {self.CPR.arrival_code}"
                    return False
                # 提取验证 URL
                content_url, temp_list = self.DPR.parse_to_attributes("css", "content", "meta[http-equiv=refresh]", self.RCR.page_source)
                action_url, temp_list = self.DPR.parse_to_attributes("css", "action", "#distilCaptchaForm", self.RCR.page_source)
                js_url, temp_list = self.DPR.parse_to_attributes("css", "src", "script[src]", self.RCR.page_source)
                if content_url or action_url:
                    verify_url = "https://booking.flyfrontier.com/"
                    if content_url:
                        captcha_url = content_url
                    else:
                        captcha_url = action_url
                    if js_url:
                        self.logger.info(captcha_url)
                        self.logger.info(verify_url)
                        self.logger.info(js_url)
                        if self.pass_to_verify(captcha_url, verify_url, js_url):
                            return self.query_from_home(count + 1, max_count)
                        else:
                            self.logger.info("认证错误")
                            return False
                    else:
                        self.logger.info("认证js错误")
                        return False
            # if self.RCR.request_to_get(is_redirect=True):
            #     if len(self.RCR.page_source) > 99999:
            #         return True
            # if "distil_r_captcha.html" in self.RCR.page_source:
            #     verify_url, temp_list = self.BPR.parse_to_regex('url=(.*?)"', self.RCR.page_source)
            #     self.verify_url = "https://makeabooking.flyscoot.com" + verify_url
            #     # if self.pass_to_verify():
                # if self.tgrairwaysdstl_get():
                #     if self.tgrairwaysdstl_post():
                # self.RCR.session.cookies.clear()
                # if self.pass_to_verify(referer_url=referer_url):
                #     return True
            # if "/Flight/Select" in self.RCR.page_source:
            #         self.RCR.url = "https://book.cebupacificair.com/Flight/Select"
            #         flight_date = self.DFR.format_to_transform(self.CPR.flight_date, "%Y%m%d")
            #         flight_date = flight_date.strftime("%Y-%m-%d")
            #         = (
            #             ('o2', self.CPR.departure_code),  # 指定行李航线
            #             ('d2', self.CPR.arrival_code),
            #             ('dd1', flight_date),  # 第一程航线时间
            #             ('dd2', flight_date),  # 指定行李航线日期
            #             ('ADT', '1'),
            #             ('CHD', '0'),
            #             ('INF', '0'),
            #             ('inl', '0'),
            #             ('pos', 'cebu.us'),
            #             ('culture', ''),
            #             ('p', ''),
            #         )
            #         self.RCR.header = self.BFR.format_to_same(self.init_header)
            #         self.RCR.header.update({
            #             # "Host": "book.cebupacificair.com",
            #             'Referer': 'https://www.cebupacificair.com/en-us',
            #             'Upgrade-Insecure-Requests': '1',
            #         })
            #         if self.RCR.request_to_get(is_redirect=True):
            #             if len(self.RCR.page_source) > 10000:
            #                 pass
            #             else:
            #                 return self.query_from_detail(count + 1, max_count)
            #                 # self.RCR.url = "https://book.cebupacificair.com/Flight/InternalSelect"
            #                 # self.RCR.param_data = (
            #                 #     ('o1', self.depart_col_dep),  # 第一程航线 规定货币
            #                 #     ('d1', self.depart_col_arr),
            #                 #     ('o2', self.dep),  # 指定行李航线
            #                 #     ('d2', self.arr),
            #                 #     ('dd1', self.depart_col_date),  # 第一程航线时间
            #                 #     ('p', ''),
            #                 #     ('dd2', self.return_col_date),  # 指定行李航线日期
            #                 #     ('ADT', '1'),
            #                 #     ('CHD', '0'),
            #                 #     ('INF', '0'),
            #                 #     ('s', 'true'),
            #                 #     ('mon', 'true'),
            #                 # )
            #             self.RCR.url = "https://book.cebupacificair.com/Flight/Select"
            #             self.RCR.param_data = None
            #             self.RCR.header = self.BFR.format_to_same(self.init_header)
            #             self.RCR.header.update({
            #                 # "Host": "book.cebupacificair.com",
            #                 'Referer': "https://book.cebupacificair.com/Flight/InternalSelect",
            #                 'Upgrade-Insecure-Requests': '1',
            #             })
            #             if self.RCR.request_to_get():
            #                     self.logger.info(self.callback_msg)
            #                     return self.query_from_detail(count + 1, max_count)
            #                 # 第一程是否有航班， 如果有航班，则跳过，
            #                 # 否则提取第一程航班的日期， 判断哪一天有航班，进行重新搜索
            #                 exit_fligth, exit_fligth_list = self.DPR.parse_to_attributes(
            #                     "css", "text", '[id="depart-table"] [class="avail-info-no-flights"] h3',
            #                     self.RCR.page_source)
            #
            #                 if "flights for this day are either sold out or unavailable" in str(
            #                         exit_fligth_list):
            #                     return False
            #
            #                 # 第二程是否有有航班
            #                 exit_fligth, exit_fligth_list = self.DPR.parse_to_attributes(
            #                     "css", "text", '[id="return-table"] [class="avail-info-no-flights"] h3',
            #                     self.RCR.page_source)
            #
            #                 # 判断第二程  (指定行李航线) ， 当前日期是否有航班
            #                 if "flights for this day are either sold out or unavailable" in str(
            #                         exit_fligth_list):
            #                     return False
            #
            #                 # 第一程 航班   # 选择第一程航班
            #                 self.dep_key, dep_key_list = self.DPR.parse_to_attributes("css", "value",
            #                                                                           '[id*="trip_0_date_0_flight"]',
            #                                                                           self.RCR.page_source)
            #
            #                 # 第二程（行李行程）   # 选择第二程航班
            #                 self.return_key, return_key_list = self.DPR.parse_to_attributes("css", "value",
            #                                                                                 '[id*="trip_1_date_0_flight"]',
            #                                                                                 self.RCR.page_source)
            #
            #                 bookingkey, bookingkey_list = self.DPR.parse_to_attributes("css", "value",
            #                                                                            '[class="bookingKey"][name="bookingKey"]',
            #                                                                            self.RCR.page_source)
            #                 if dep_key_list and return_key_list:
            #
            #                     self.RCR.url = "https://book.cebupacificair.com/Flight/Select"
            #                     self.RCR.header = self.BFR.format_to_same(self.init_header)
            #                     self.RCR.post_data = {
            #                         'cebSellBundleSsrs.BundleTypeSelectionDepart': '',
            #                         'cebSellBundleSsrs.BundleTypeSelectionDepart': '',
            #                         'cebSellBundleSsrs.BundleTypeSelectionReturn': '',
            #                         'cebSellBundleSsrs.BundleTypeSelectionReturn': '',
            #                         'cebAvailability.MarketFareKeys[0]': self.dep_key,
            #                         'cebAvailability.MarketFareKeys[1]': self.return_key,
            #                         'bookingKey': bookingkey,
            #                     }
            #
            #                     self.RCR.header.update({
            #                         'Upgrade-Insecure-Requests': '1',
            #                         # "Host": "book.cebupacificair.com",
            #                         'Origin': 'https://book.cebupacificair.com',
            #                         'Content-Type': 'application/x-www-form-urlencoded',
            #                         'Referer': 'https://book.cebupacificair.com/Flight/Select',
            #                     })
            #                     if self.RCR.request_to_post():
            #                         self.RCR.url = "https://book.cebupacificair.com/Passengers/Edit"
            #                         self.RCR.header = self.BFR.format_to_same(self.init_header)
            #                         self.RCR.post_data = None
            #                         self.RCR.header.update({
            #                             'Upgrade-Insecure-Requests': '1',
            #                             # "Host": "book.cebupacificair.com",
            #                             'Referer': 'https://book.cebupacificair.com/Flight/Select',
            #                         })
            #                         if self.RCR.request_to_get():
            #                             if self.page_verify(str(self.RCR.page_source)):
            #                                 self.callback_msg = f"出现验证码【{self.RCR.url}】"
            #                                 self.set_to_proxy()
            #                                 # self.ssh.get_server_ip()
            #                                 # self.RCR.set_to_proxy(enable_proxy=True,
            #                                 #                       address='http://yunku:123@{}:3138'.format(
            #                                 #                           self.ssh.proxy_ip))
            #                                 return self.query_from_detail(count + 1, max_count)
            #                             self.temp_source = self.BFR.format_to_same(self.RCR.page_source)
            #                             return True
            #
            #                     else:
            #                         # 切换日期，重新搜索
            #                         return self.query_from_detail(count + 1, max_count)
            #
            #                 else:
            #                     return self.query_from_detail(count + 1, max_count)
            #
            #         self.callback_msg = "获取航班信息失败"
            #         # return False
            #     self.RCR.url = "https://book.cebupacificair.com/Flight/QueueItRedirect"
            #     self.RCR.param_data = None
            #     self.RCR.header = self.BFR.format_to_same(self.init_header)
            #     self.RCR.header.update({
            #         # "Host": "book.cebupacificair.com",
            #         'Referer': 'https://book.cebupacificair.com/',
            #         'Upgrade-Insecure-Requests': '1',
            #     })
            #     if self.RCR.request_to_get(is_redirect=True):
            #         self.RCR.url = "https://book.cebupacificair.com/"
            #         self.RCR.param_data = None
            #         self.RCR.header = self.BFR.format_to_same(self.init_header)
            #         self.RCR.header.update({
            #             # "Host": "book.cebupacificair.com",
            #             'Upgrade-Insecure-Requests': '1',
            #         })
            #         if self.RCR.request_to_get(is_redirect=True):
            #
            #             self.RCR.url = "https://book.cebupacificair.com/Flight/QueueItRedirect"
            #             self.RCR.param_data = None
            #             self.RCR.header = self.BFR.format_to_same(self.init_header)
            #             self.RCR.header.update({
            #                 # "Host": "book.cebupacificair.com",
            #                 'Referer': 'https://book.cebupacificair.com/',
            #                 'Upgrade-Insecure-Requests': '1',
            #             })
            #             if self.RCR.request_to_get(is_redirect=True):
            #                 self.RCR.url, temp = self.BPR.parse_to_regex('window\.location\=\'(.*?)\'\}\)',
            #                                                                   self.RCR.page_source)
            #                 print(self.RCR.url)
            #                 if self.RCR.url:
            #                     self.RCR.param_data = None
            #                     self.RCR.header = self.BFR.format_to_same(self.init_header)
            #                     self.RCR.header.update({
            #                         # "Host": "cebupacificair.queue-it.net",
            #                         'Upgrade-Insecure-Requests': '1',
            #                     })
            #                     if self.RCR.request_to_get(is_redirect=True):
            #                         if "QueueItRedirect" in self.RCR.page_source:
            #                                 return True
            return self.query_from_home(count + 1, max_count)
    def query_from_detail(self, count: int = 0, max_count: int = 4):
        if count >= max_count:
            return False
        # 提取航班
        flight_keys, flight_date_list = self.BPR.parse_to_regex('\"standardFareKey...(.*?)",', self.temp_source)
        for i in flight_date_list:
            if len(i) > 100:
                self.logger.info(flight_date_list)
                continue
            else:
                flight_keys = i.replace('\\', '')
                flight_keys = self.BPR.parse_to_replace("\\|\"|\"", "", flight_keys)
                break
        else:
            self.callback_msg = f"当前航班无直飞【{self.CPR.departure_code} - {self.CPR.arrival_code}】"
            return False
        if flight_keys:
            self.RCR.url = "https://booking.flyfrontier.com/Flight/Select"
            self.RCR.post_data = {
                'frontierAvailability.MarketFareKeys[0]': flight_keys,
                'frontierAvailability.DiscountDenInformation.IsDiscountDenBooking': 'false',
                'frontierAvailability.DiscountDenInformation.DiscountDenDepartureSavings': '0',
                'frontierAvailability.DiscountDenInformation.DiscountDenReturnSavings': '0',
                'frontierAvailability.DiscountDenInformation.AlreadyDiscountDenMember': 'false'
            }
            self.RCR.header = self.BFR.format_to_same(self.init_header)
            self.RCR.header.update({
                'Pragma': 'no-cache',
                'Cache-control': 'no-cache',
                'Origin': 'https://booking.flyfrontier.com',
                'Upgrade-insecure-requests': '1',
                'Content-type': 'application/x-www-form-urlencoded',
                'Sec-fetch-mode': 'navigate',
                'Sec-fetch-user': '?1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Sec-fetch-site': 'same-origin',
                'Referer': 'https://booking.flyfrontier.com/Flight/Select',
            })
            if self.RCR.request_to_post(is_redirect=True):
                if "frontierRegisterMember_personalEmailAddressConfirmation" in self.RCR.page_source:
                    return True
                #
                # 提取验证 URL
                content_url, temp_list = self.DPR.parse_to_attributes("css", "content", "meta[http-equiv=refresh]",
                                                                      self.RCR.page_source)
                action_url, temp_list = self.DPR.parse_to_attributes("css", "action", "#distilCaptchaForm",
                                                                     self.RCR.page_source)
                js_url, temp_list = self.DPR.parse_to_attributes("css", "src", "script[src]", self.RCR.page_source)
                if content_url or action_url:
                    verify_url = "https://booking.flyfrontier.com/"
                    if content_url:
                        captcha_url = content_url
                    else:
                        captcha_url = action_url
                    if js_url:
                        self.logger.info(captcha_url)
                        self.logger.info(verify_url)
                        self.logger.info(js_url)
                        if self.pass_to_verify(captcha_url, verify_url, js_url):
                            return self.query_from_detail(count + 1, max_count)
                        else:
                            self.logger.info("认证错误")
                            return False
                    else:
                        self.logger.info("认证js错误")
                        return False
                return True
            return True
        else:
            self.logger.info("当前日期无航班")
            flight_date, flight_date_list = self.DPR.parse_to_attributes("css", "data-date", "[class='ibe-flight-slider-box w-inline-block w-hidden-small w-hidden-tiny']",
                                                                         self.RCR.page_source)
            self.logger.info(flight_date)
            self.logger.info(flight_date_list)
            return False
    def set_meal(self, count: int = 0, max_count: int = 2):
        if count >= max_count:
            self.callback_msg = f"提交乘客信息失败【 set_meal 】"
            return False
        self.RCR.url = "https://booking.flyfrontier.com/Passengers/Update"
        self.RCR.post_data = {
            'frontierPassengers[0].PassengerNumber': '0',
            'frontierPassengers[0].TypeInfo.PaxType': 'ADT',
            'frontierPassengers[0].CustomerNumber': '',
            'frontierPassengers_0': 'Adult',
            'frontierPassengers[0].Name.First': 'shi',
            'frontierPassengers[0].Name.Middle': 'san',
            'frontierPassengers[0].Name.Last': 'shi',
            'frontierPassengers[0].Name.Suffix': '',
            'frontierPassengers[0].Info.Gender': '1',
            'frontierPassengers[0].TypeInfo.DateOfBirth': '1/15/1996',
            'frontierPassengers.PassengersRedressNumbers[0].PassengerNumber': '0',
            'frontierPassengers.PassengersRedressNumbers[0].RedressNumber': '',
            'frontierPassengers.KnownTravelerNumbers[0].KnownTravelerNumber': '',
            'frontierContact.TypeCode': 'P',
            'frontierContact.CustomerNumber': '',
            'frontierContact.Name.First': 'shi',
            'frontierContact.Name.Last': 'shi',
            'frontierContact.EmailAddress': 'zl158211.@163.com',
            'frontierContact.OtherPhone': '17634004766',
            'frontierContact.WorkPhone': '',
            'frontierContact.CountryCode': 'CN',
            'frontierContact.PostalCode': '',
            'frontierContact.ProvinceState': '',
            'frontierContact.CompanyName': '',
            'frontierContact.SourceOrganization': ''
        }
        self.RCR.header = self.BFR.format_to_same(self.init_header)
        self.RCR.header.update({
            'authority': 'booking.flyfrontier.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'origin': 'https://booking.flyfrontier.com',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://booking.flyfrontier.com/Passengers/Edit',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        })
        if self.RCR.request_to_post(is_redirect=True):
            if "__RequestVerificationToken" in self.RCR.page_source:
                self.verify_token, token_temp_list = self.DPR.parse_to_attributes(
                    "css", "value", "input[name='__RequestVerificationToken']", self.RCR.page_source)
                return True
            else:
                self.callback_msg = f"提交乘客信息异常【 set_meal 】"
                return False
        else:
            return self.set_meal(count + 1, max_count)
    def query_from_seat(self, count: int = 0, max_count: int = 2):
        # 获取座位页面
        if count >= max_count:
            self.callback_msg = f"提交乘客信息失败【 set_meal 】"
            return False
        self.RCR.url = "https://booking.flyfrontier.com/Bundles/Index"
        self.RCR.post_data = {
            '__RequestVerificationToken': self.verify_token,
        }
        self.RCR.header = self.BFR.format_to_same(self.init_header)
        self.RCR.header.update({
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'origin': 'https://booking.flyfrontier.com',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://booking.flyfrontier.com/Bundles/Index',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        })
        if self.RCR.request_to_post(is_redirect=True):
            if "__RequestVerificationToken" in self.RCR.page_source:
                self.verify_token, token_temp_list = self.DPR.parse_to_attributes(
                    "css", "value", "input[name='__RequestVerificationToken']", self.RCR.page_source)
                return True
            else:
                self.logger.info(self.RCR.page_source)
                return True
        else:
            return self.query_from_seat(count + 1, max_count)
    def query_from_bags(self, count: int = 0, max_count: int = 2) -> bool:
        # 获取行李数据页面
        if count >= max_count:
            self.callback_msg = f"提交乘客信息失败【 set_meal 】"
            return False
        self.RCR.url = "https://booking.flyfrontier.com/SeatMap/Index"
        self.RCR.post_data = {
            '__RequestVerificationToken': self.verify_token,
        }
        self.RCR.header = self.BFR.format_to_same(self.init_header)
        self.RCR.header.update({
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'origin': 'https://booking.flyfrontier.com',
            'upgrade-insecure-requests': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'sec-fetch-site': 'same-origin',
            'referer': 'https://booking.flyfrontier.com/Bundles/Index',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
        })
        if self.RCR.request_to_post(is_redirect=True):
            if "ibe-field-box w-input ibe-select-field w-select js-customSelect js-bagsSelect js-bagsCheckedSelect" in self.RCR.page_source:
                return True
            else:
                self.logger.info(self.RCR.page_source)
                return True
        else:
            return self.query_from_seat(count + 1, max_count)
    def collect_to_luggage(self,  count: int = 0, max_count: int = 1) -> bool:
        """收集行李信息
        :return:  bool
        """
        if count >= max_count:
            return False
        try:
            luggage_currency, luggage_currency_list = self.BPR.parse_to_regex('currency":"(.*?)",',
                                                              self.RCR.page_source)
            luggages, luggages_list = self.BPR.parse_to_regex('bagsPage.*?data.*?({.*?)"formSelector',
                                                              self.RCR.page_source)
            luggage, luggage_temp_list = self.BPR.parse_to_path('$..checked', self.BPR.parse_to_dict(luggages[:-1]))
            for i in luggage_temp_list:
                if "price" in str(i):
                    for x in i:
                        if x.get('price') == '0':
                            continue
                        else:
                            a = x.get("name").split("-")
                            if len(a) == 2:
                                luggage_piece, luggage_piece_list = self.BPR.parse_to_regex('[0-9]{1,}', str(a[0]))
                                price, price_list = self.BPR.parse_to_regex('[0-9]{1,}', str(a[-1]))
                                # self.logger.info(f"{price} {luggage_piece}")
                                dict_temp = {}
                                dict_temp['departure_aircode'] = self.CPR.departure_code
                                dict_temp['arrival_aircode'] = self.CPR.arrival_code
                                dict_temp['baggage_weight'] = int(luggage_piece) * 22  # 行李重量
                                dict_temp['foreign_currency'] = luggage_currency        # 原始货币
                                dict_temp['foreign_price'] = price            # 行李价格
                                dict_temp['carrier'] = "f9"                   # 行李航司
                                # dict_temp['rmb_price'] = rmb_price          # 人民币价格
                                self.baggage_data.append(dict_temp)
            self.callback_msg = "行李抓取成功"
            return True
        except Exception as ex:
            self.callback_msg = f'{ex} | 行李提取有误'
            self.logger.info(self.callback_msg)
            return False
    def pass_to_verify(self, captcha_url: str = "", referer_url: str = "", js_url: str = "", count: int = 0,
               max_count: int = 3) -> bool:
        """认证流程
        :param captcha_url:  请求认证的地址
        :param referer_url:  认证的来源地址
        :param js_url:  认证的js地址
        :param count:  重试次数
        :param max_count:  重试最大次数
        :return:  bool
        """
        if count >= max_count:
            return False
        else:
            if self.frntrirdstl_get():
                if self.ajax_header:
                    # # # 获取challenge
                    self.RCR.url = "https://booking.flyfrontier.com/distil_r_captcha_challenge"
                    self.RCR.param_data = None
                    self.RCR.header = self.BFR.format_to_same(self.init_header)
                    self.RCR.header.update({
                        "Accept": "*/*",
                        "Host": "booking.flyfrontier.com",
                        "Origin": "https://booking.flyfrontier.com",
                        "Referer": referer_url,
                        "X-Distil-Ajax": self.ajax_header,
                        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                        "Accept-Encoding": "gzip, deflate, br",
                    })
                    self.RCR.post_data = None
                    if self.RCR.request_to_post():
                        challenge, temp_list = self.BPR.parse_to_regex("(.*?);", self.RCR.page_source)
                        if challenge:
                            # # # 获取mp3地址
                            self.RCR.url = "http://api-na.geetest.com/get.php"
                            self.RCR.param_data = (
                                ("gt", "f2ae6cadcf7886856696502e1d55e00c"), ("challenge", challenge),
                                ("type", "voice"), ("lang", "zh-cn"), ("callback", ""),
                            )
                            self.RCR.header = self.BFR.format_to_same(self.init_header)
                            self.RCR.header.update({
                                "Accept": "*/*",
                                "Host": "api-na.geetest.com",
                                "Referer": referer_url,
                                "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                                "Accept-Encoding": "gzip, deflate, br",
                            })
                            if self.RCR.request_to_get():
                                get_json = self.RCR.page_source.strip("()")
                                get_json = self.BPR.parse_to_dict(get_json)
                                voice_path, temp_list = self.BPR.parse_to_path("$.data.new_voice_path", get_json)
                                voice_path, temp_list = self.BPR.parse_to_regex("/voice/zh/(.*).mp3", voice_path)
                                if not voice_path:
                                    self.logger.info(f"认证音频地址错误(*>﹏<*)【{self.RCR.page_source}】")
                                    self.callback_msg = "认证音频地址错误"
                                    return self.pass_to_verify(captcha_url, referer_url, count + 1, max_count)
                                else:
                                    # # # 获取mp3文件
                                    self.RCR.url = "http://114.55.207.125:50005/getcaptcha/geetest/" + voice_path
                                    self.RCR.param_data = None
                                    self.RCR.header = None
                                    if self.RCR.request_to_get():
                                        # # 识别语音
                                        number, temp_list = self.BPR.parse_to_regex("\d+", self.RCR.page_source)
                                        if number:
                                            # # # 获取validate
                                            self.RCR.url = "http://api-na.geetest.com/ajax.php"
                                            self.RCR.param_data = (
                                                ("gt", "ce33de396f8d04030f6eca8fbd225070"),
                                                ("challenge", challenge),
                                                ("a", number), ("lang", "zh-cn"), ("callback", "")
                                            )
                                            self.RCR.header = self.BFR.format_to_same(self.init_header)
                                            self.RCR.header.update({
                                                "Accept": "*/*",
                                                "Host": "api-na.geetest.com",
                                                "Referer": referer_url
                                            })
                                            if self.RCR.request_to_get():
                                                self.logger.info(self.RCR.page_source)
                                                get_json = self.RCR.page_source.strip("()")
                                                get_json = self.BPR.parse_to_dict(get_json)
                                                validate, temp_list = self.BPR.parse_to_path("$.data.validate",
                                                                                             get_json)
                                                # self.logger.info(temp_list)
                                                # self.logger.info(captcha_url)
                                                cap_url, temp_list = self.BPR.parse_to_regex(
                                                    "url=(.*)", captcha_url)
                                                # self.logger.info(temp_list)
                                                if cap_url:
                                                    self.RCR.url = "https://booking.flyfrontier.com" + cap_url
                                                else:
                                                    self.RCR.url = "https://booking.flyfrontier.com" + captcha_url
                                                self.logger.info(self.RCR.url)
                                                # if not validate or not cap_url:
                                                #     return self.pass_to_verify(captcha_url, referer_url, js_url, count + 1, max_count)
                                                # else:
                                                # # # 提交认证
                                                self.RCR.param_data = None
                                                self.RCR.header = self.BFR.format_to_same(self.init_header)
                                                self.RCR.header.update({
                                                    "Accept": "*/*",
                                                    "Content-Type": "application/x-www-form-urlencoded",
                                                    "Host": "booking.flyfrontier.com",
                                                    "Origin": "https://booking.flyfrontier.com",
                                                    "Referer": referer_url,
                                                    "X-Distil-Ajax": self.ajax_header,
                                                    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
                                                    "Accept-Encoding": "gzip, deflate, br",
                                                })
                                                self.RCR.post_data = [
                                                    ("dCF_ticket", ""), ("geetest_challenge", challenge),
                                                    ("geetest_validate", validate),
                                                    ("geetest_seccode", f"{validate}|jordan"),
                                                    ("isAjax", "1"),
                                                ]
                                                if self.RCR.request_to_post(status_code=204):
                                                    self.logger.info("语音识别认证成功(*^__^*)【verify】")
                                                    return True
            self.logger.info(f"认证第{count + 1}次超时或者错误(*>﹏<*)【verify】")
            return self.pass_to_verify(captcha_url, referer_url, js_url, count + 1, max_count)
    def frntrirdstl_get(self, count: int = 0, max_count: int = 3) -> bool:
        if count >= max_count:
            return False
        # # # 获取ajax header
        self.RCR.url = "https://booking.flyfrontier.com/frntrirdstl.js"
        self.RCR.param_data = None
        self.RCR.header = self.BFR.format_to_same(self.init_header)
        self.RCR.header.update({
            "Accept": "*/*",
            "Host": "booking.flyfrontier.com",
            "Referer": "https://booking.flyfrontier.com/",
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-origin',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        })
        if self.RCR.request_to_get():
            self.ajax_header, temp_list = self.BPR.parse_to_regex('ajax_header:"(.*?)",', self.RCR.page_source)
            self.url_pid, pid_list = self.BPR.parse_to_regex('path:"(.*?)",', self.RCR.page_source)
            return True
    def frntrirdstl_post(self, count: int = 0, max_count: int = 3) -> bool:
        if count >= max_count:
            return False
        pwd_len = 20
        str_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                    't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        n = 0
        pwd = ""
        while len(pwd) < pwd_len:
            a = random.randint(0, 36)
            if a >= 0 and a < len(str_list):
                pwd += str(str_list[a])
                n += 1
        num = 16777216
        o = ''
        for i in range(num):
            e = str(int(time.time())) + ":" + pwd
            o = '%x:%s' % (i, e)
            sha = hashlib.sha1(o.encode('utf-8'))
            encrypts = sha.hexdigest()
            if "00" == encrypts[:2]:
                break
        self.RCR.url = 'https://booking.flyfrontier.com' + self.url_pid
        self.RCR.post_data = 'p=%7B%22proof%22%3A%22' + str(urlencode({"": o})[1:])  + '%22%2C%22fp2%22%3A%7B%22userAgent%22%3A%22Mozilla%2F5.0(WindowsNT10.0%3BWin64%3Bx64)AppleWebKit%2F537.36(KHTML%2ClikeGecko)Chrome%2F76.0.3809.132Safari%2F537.36%22%2C%22language%22%3A%22zh-CN%22%2C%22screen%22%3A%7B%22width%22%3A1920%2C%22height%22%3A1080%2C%22availHeight%22%3A1050%2C%22availWidth%22%3A1920%2C%22pixelDepth%22%3A24%2C%22innerWidth%22%3A1920%2C%22innerHeight%22%3A457%2C%22outerWidth%22%3A1920%2C%22outerHeight%22%3A1050%2C%22devicePixelRatio%22%3A1%7D%2C%22timezone%22%3A8%2C%22indexedDb%22%3Atrue%2C%22addBehavior%22%3Afalse%2C%22openDatabase%22%3Atrue%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22Win32%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%22ChromePDFPlugin%3A%3APortableDocumentFormat%3A%3Aapplication%2Fx-google-chrome-pdf~pdf%3BChromePDFViewer%3A%3A%3A%3Aapplication%2Fpdf~pdf%3BNativeClient%3A%3A%3A%3Aapplication%2Fx-nacl~%2Capplication%2Fx-pnacl~%22%2C%22canvas%22%3A%7B%22winding%22%3A%22yes%22%2C%22towebp%22%3Atrue%2C%22blending%22%3Atrue%2C%22img%22%3A%22aa281d97036237523f94f8257835ad78225ae962%22%7D%2C%22webGL%22%3A%7B%22img%22%3A%22bd6549c125f67b18985a8c509803f4b883ff810c%22%2C%22extensions%22%3A%22ANGLE_instanced_arrays%3BEXT_blend_minmax%3BEXT_color_buffer_half_float%3BEXT_disjoint_timer_query%3BEXT_float_blend%3BEXT_frag_depth%3BEXT_shader_texture_lod%3BEXT_texture_filter_anisotropic%3BWEBKIT_EXT_texture_filter_anisotropic%3BEXT_sRGB%3BKHR_parallel_shader_compile%3BOES_element_index_uint%3BOES_standard_derivatives%3BOES_texture_float%3BOES_texture_float_linear%3BOES_texture_half_float%3BOES_texture_half_float_linear%3BOES_vertex_array_object%3BWEBGL_color_buffer_float%3BWEBGL_compressed_texture_s3tc%3BWEBKIT_WEBGL_compressed_texture_s3tc%3BWEBGL_compressed_texture_s3tc_srgb%3BWEBGL_debug_renderer_info%3BWEBGL_debug_shaders%3BWEBGL_depth_texture%3BWEBKIT_WEBGL_depth_texture%3BWEBGL_draw_buffers%3BWEBGL_lose_context%3BWEBKIT_WEBGL_lose_context%22%2C%22aliasedlinewidthrange%22%3A%22%5B1%2C1%5D%22%2C%22aliasedpointsizerange%22%3A%22%5B1%2C1024%5D%22%2C%22alphabits%22%3A8%2C%22antialiasing%22%3A%22yes%22%2C%22bluebits%22%3A8%2C%22depthbits%22%3A24%2C%22greenbits%22%3A8%2C%22maxanisotropy%22%3A16%2C%22maxcombinedtextureimageunits%22%3A32%2C%22maxcubemaptexturesize%22%3A16384%2C%22maxfragmentuniformvectors%22%3A1024%2C%22maxrenderbuffersize%22%3A16384%2C%22maxtextureimageunits%22%3A16%2C%22maxtexturesize%22%3A16384%2C%22maxvaryingvectors%22%3A30%2C%22maxvertexattribs%22%3A16%2C%22maxvertextextureimageunits%22%3A16%2C%22maxvertexuniformvectors%22%3A4096%2C%22maxviewportdims%22%3A%22%5B32767%2C32767%5D%22%2C%22redbits%22%3A8%2C%22renderer%22%3A%22WebKitWebGL%22%2C%22shadinglanguageversion%22%3A%22WebGLGLSLES1.0(OpenGLESGLSLES1.0Chromium)%22%2C%22stencilbits%22%3A0%2C%22vendor%22%3A%22WebKit%22%2C%22version%22%3A%22WebGL1.0(OpenGLES2.0Chromium)%22%2C%22vertexshaderhighfloatprecision%22%3A23%2C%22vertexshaderhighfloatprecisionrangeMin%22%3A127%2C%22vertexshaderhighfloatprecisionrangeMax%22%3A127%2C%22vertexshadermediumfloatprecision%22%3A23%2C%22vertexshadermediumfloatprecisionrangeMin%22%3A127%2C%22vertexshadermediumfloatprecisionrangeMax%22%3A127%2C%22vertexshaderlowfloatprecision%22%3A23%2C%22vertexshaderlowfloatprecisionrangeMin%22%3A127%2C%22vertexshaderlowfloatprecisionrangeMax%22%3A127%2C%22fragmentshaderhighfloatprecision%22%3A23%2C%22fragmentshaderhighfloatprecisionrangeMin%22%3A127%2C%22fragmentshaderhighfloatprecisionrangeMax%22%3A127%2C%22fragmentshadermediumfloatprecision%22%3A23%2C%22fragmentshadermediumfloatprecisionrangeMin%22%3A127%2C%22fragmentshadermediumfloatprecisionrangeMax%22%3A127%2C%22fragmentshaderlowfloatprecision%22%3A23%2C%22fragmentshaderlowfloatprecisionrangeMin%22%3A127%2C%22fragmentshaderlowfloatprecisionrangeMax%22%3A127%2C%22vertexshaderhighintprecision%22%3A0%2C%22vertexshaderhighintprecisionrangeMin%22%3A31%2C%22vertexshaderhighintprecisionrangeMax%22%3A30%2C%22vertexshadermediumintprecision%22%3A0%2C%22vertexshadermediumintprecisionrangeMin%22%3A31%2C%22vertexshadermediumintprecisionrangeMax%22%3A30%2C%22vertexshaderlowintprecision%22%3A0%2C%22vertexshaderlowintprecisionrangeMin%22%3A31%2C%22vertexshaderlowintprecisionrangeMax%22%3A30%2C%22fragmentshaderhighintprecision%22%3A0%2C%22fragmentshaderhighintprecisionrangeMin%22%3A31%2C%22fragmentshaderhighintprecisionrangeMax%22%3A30%2C%22fragmentshadermediumintprecision%22%3A0%2C%22fragmentshadermediumintprecisionrangeMin%22%3A31%2C%22fragmentshadermediumintprecisionrangeMax%22%3A30%2C%22fragmentshaderlowintprecision%22%3A0%2C%22fragmentshaderlowintprecisionrangeMin%22%3A31%2C%22fragmentshaderlowintprecisionrangeMax%22%3A30%2C%22unmaskedvendor%22%3A%22GoogleInc.%22%2C%22unmaskedrenderer%22%3A%22ANGLE(Intel(R)HDGraphics630Direct3D11vs_5_0ps_5_0)%22%7D%2C%22touch%22%3A%7B%22maxTouchPoints%22%3A0%2C%22touchEvent%22%3Afalse%2C%22touchStart%22%3Afalse%7D%2C%22video%22%3A%7B%22ogg%22%3A%22probably%22%2C%22h264%22%3A%22probably%22%2C%22webm%22%3A%22probably%22%7D%2C%22audio%22%3A%7B%22ogg%22%3A%22probably%22%2C%22mp3%22%3A%22probably%22%2C%22wav%22%3A%22probably%22%2C%22m4a%22%3A%22maybe%22%7D%2C%22vendor%22%3A%22GoogleInc.%22%2C%22product%22%3A%22Gecko%22%2C%22productSub%22%3A%2220030107%22%2C%22browser%22%3A%7B%22ie%22%3Afalse%2C%22chrome%22%3Atrue%2C%22webdriver%22%3Afalse%7D%2C%22window%22%3A%7B%22historyLength%22%3A2%2C%22hardwareConcurrency%22%3A8%2C%22iframe%22%3Afalse%2C%22battery%22%3Atrue%7D%2C%22location%22%3A%7B%22protocol%22%3A%22https%3A%22%7D%2C%22fonts%22%3A%22Calibri%3BCentury%3BHaettenschweiler%3BLeelawadee%3BMarlett%3BPristina%3BSimHei%22%2C%22devices%22%3A%7B%22count%22%3A4%2C%22data%22%3A%7B%220%22%3A%7B%22deviceId%22%3A%22default%22%2C%22groupId%22%3A%224c89888d4295f2527630a443e2cd786c43289deff5e216e0c73e92cf3ba282d7%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%2C%221%22%3A%7B%22deviceId%22%3A%22communications%22%2C%22groupId%22%3A%224c89888d4295f2527630a443e2cd786c43289deff5e216e0c73e92cf3ba282d7%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%2C%222%22%3A%7B%22deviceId%22%3A%221672b484ad1cd72eec3fa5994db367b8cc91ecc511072cac016354f1556f7406%22%2C%22groupId%22%3A%22cbaef8a5d62a86755cd1953c7cedfb92bd53982ca477c5d4e59020d9ca929c18%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%2C%223%22%3A%7B%22deviceId%22%3A%2236369a548410156d7aa55b542150c1b426cf38496c60e6c8dd5e1ff0e02c3738%22%2C%22groupId%22%3A%224c89888d4295f2527630a443e2cd786c43289deff5e216e0c73e92cf3ba282d7%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%7D%7D%7D%2C%22cookies%22%3A1%2C%22setTimeout%22%3A0%2C%22setInterval%22%3A0%2C%22appName%22%3A%22Netscape%22%2C%22platform%22%3A%22Win32%22%2C%22syslang%22%3A%22zh-CN%22%2C%22userlang%22%3A%22zh-CN%22%2C%22cpu%22%3A%22%22%2C%22productSub%22%3A%2220030107%22%2C%22plugins%22%3A%7B%220%22%3A%22ChromePDFPlugin%22%2C%221%22%3A%22ChromePDFViewer%22%2C%222%22%3A%22NativeClient%22%7D%2C%22mimeTypes%22%3A%7B%220%22%3A%22application%2Fpdf%22%2C%221%22%3A%22PortableDocumentFormatapplication%2Fx-google-chrome-pdf%22%2C%222%22%3A%22NativeClientExecutableapplication%2Fx-nacl%22%2C%223%22%3A%22PortableNativeClientExecutableapplication%2Fx-pnacl%22%7D%2C%22screen%22%3A%7B%22width%22%3A1920%2C%22height%22%3A1080%2C%22colorDepth%22%3A24%7D%2C%22fonts%22%3A%7B%220%22%3A%22Calibri%22%2C%221%22%3A%22Cambria%22%2C%222%22%3A%22Times%22%2C%223%22%3A%22Constantia%22%2C%224%22%3A%22LucidaBright%22%2C%225%22%3A%22Georgia%22%2C%226%22%3A%22SegoeUI%22%2C%227%22%3A%22Candara%22%2C%228%22%3A%22TrebuchetMS%22%2C%229%22%3A%22Verdana%22%2C%2210%22%3A%22Consolas%22%2C%2211%22%3A%22LucidaConsole%22%2C%2212%22%3A%22LucidaSansTypewriter%22%2C%2213%22%3A%22DejaVuSansMono%22%2C%2214%22%3A%22CourierNew%22%2C%2215%22%3A%22Courier%22%7D%7D'
        self.RCR.header = self.BFR.format_to_same(self.init_header)
        self.RCR.header.update({
            "Host": "booking.flyfrontier.com",
            'Pragma': 'no-cache',
            'Sec-Fetch-Mode': 'cors',
            'Origin': 'https://booking.flyfrontier.com',
            'X-Distil-Ajax': self.ajax_header,
            'Content-Type': 'text/plain;charset=UTF-8',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-origin',
            "Accept-Encoding": "gzip, deflate, br",
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'http://booking.flyfrontier.com',
        })
        if self.RCR.request_to_post(is_redirect=True):
            return True
    def return_to_data(self) -> bool:
        """返回结果数据
        :return:  bool
        """
        self.callback_data["success"] = "true"
        self.callback_data['msg'] = "更新成功"
        self.callback_data["baggage"] = self.baggage_data   # 行李数据
        self.logger.info(self.callback_data)
        return True