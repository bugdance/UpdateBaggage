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
"""The parser is use for parse the data."""


class CallInParser:
    """接入解析器，解析接口结构数据。"""

    def __init__(self, enable_corp: bool = True):
        """Init.

        Args:
            enable_corp (bool): Whether it is a corporate account(True/False). 是否是企业账户。
        """
        self.logger: any = None  # 日志记录器。
        self.enable_corp: bool = enable_corp  # 是否是企业类型。
        # # # Interface data. 接口数据。
        self.task_id: any = None  # 任务编号。
        self.carrier: str = ""  # 航司代码。
        self.departure_code: str = ""  # 始发三字码。
        self.arrival_code: str = ""  # 到达三字码。
        self.departure_date: str = ""  # 去程日期。
        self.return_date: str = ""  # 回程日期。
        self.currency: str = ""  # 默认货币类型。

    def parse_to_interface(self, source_dict: dict = None) -> bool:
        """Parsing interface parameters. 解析接口数据。

        Args:
            source_dict (dict): The source dict. 来源字典。

        Returns:
            bool
        """
        if not source_dict or type(source_dict) is not dict:
            self.logger.info(f"解析接口参数有误(*>﹏<*)【{source_dict}】")
            return False
        # # # Parse the data. 解析数据。
        self.task_id = source_dict.get('updateId')
        self.carrier = source_dict.get('carrier')
        self.departure_code = source_dict.get('departureAirport')
        self.arrival_code = source_dict.get('arriveAirport')
        self.departure_date = source_dict.get('departureTime')
        self.return_date = source_dict.get('returnTime')
        self.currency = source_dict.get("currency")
        return True
