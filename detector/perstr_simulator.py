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
"""The simulator is use for verify some process."""
from aip import AipSpeech
import os


class PersTRSimulator:
	"""TR模拟器，模拟语音验证。"""
	
	def __init__(self):
		self.logger: any = None  # 日志记录器。
		self.app_id = '16545421'  # 百度app id。
		self.api_key = 'vFHhGpxyvKfuDLz7sIxnLtXo'  # 百度app key。
		self.secret_key = '4ztvkdVGuucwgM806kXWMxnYcUziKpAw'  # 百度secret key。
	
	def recognize_to_voice(self, voice_name: str = "", source_bytes: bytes = b"") -> tuple:
		"""识别语音验证码。
		
		Args:
			voice_name: 语音名称。
			source_bytes: 语音流。

		Returns:
			tuple
		"""
		try:
			mp3_path = f"mp3/{voice_name}.mp3"
			pcm_path = f"pcm/{voice_name}.pcm"
			# # # 保存mp3文件。
			with open(mp3_path, "wb") as f:
				f.write(source_bytes)
			# # # mp3转pcm。
			os.system(
				"ffmpeg -hide_banner -y -threads 1 -i {} -ss 00:00:05 -t 00:00:06 "
				"-acodec pcm_s16le -f s16le -ac 1 -ar 16000 {}".format(mp3_path, pcm_path))
			# # # 读取pcm文件。
			with open(pcm_path, 'rb') as f:
				file = f.read()
			# # # 识别pcm文件。
			client = AipSpeech(self.app_id, self.api_key, self.secret_key)
			result = client.asr(file, 'pcm', 16000, {'dev_pid': 1536})
			result_list = result.get('result')
		except Exception as ex:
			self.logger.info(f"识别验证音频失败(*>﹏<*)【{voice_name}】")
			self.logger.info(f"验证音频失败原因(*>﹏<*)【{ex}】")
			return "", []
		else:
			if not result_list:
				self.logger.info(f"识别验证音频失败(*>﹏<*)【{result}】")
				return "", []
			else:
				return result_list[0], result_list

