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
from detector.perstr_simulator import PersTRSimulator
import time
import random
import hashlib
from urllib.parse import urlencode
import uuid


class PersTRScraper(RequestWorker):
	"""TR采集器
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
		self.PSR = PersTRSimulator()  # VJ模拟器。
		# # # 请求中用到的变量
		self.verify_token: str = ""  # 认证token
		self.tab_id: str = ""  # 认证tab id
		self.sequence: str = ""  # post 航班查询参数
		self.request_sequence: str = ""
		self.dCF_ticket: str = ""
		self.cookies = None
		self.ajax_header: str = ""  # 认证ajax header
		self.temp_source: str = ""  # 临时源数据
		self.hold_button: str = ""  # 占舱按钮
		self.key: str = ""
		# # # 返回中用到的变量
		self.total_price: float = 0.0  # 总价
		self.baggage_price: float = -1  # 行李总价
		self.baggage_data = []  # 行李数据
		self.pnr_timeout: str = ""  # 票号超时时间
	
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
		self.PSR.logger = self.logger
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
		self.user_agent, self.init_header = self.RCR.build_to_header("Chrome")
		# # # 主体流程。
		self.RCR.session.max_redirects = 10
		self.RCR.session.cookies.clear()
		# if self.set_to_proxy():
		# 	self.RCR.timeout = 35
		if self.query_from_home():
			if self.query_from_detail():
				if self.get_baggage():
					if self.get_for_record():
						if self.return_to_data():
							self.logger.removeHandler(self.handler)
							return self.callback_data
		# # # 错误返回。
		self.callback_data['msg'] = self.callback_msg
		# self.callback_data['msg'] = "解决问题中，请手工更新行李。"
		self.logger.info(self.callback_data)
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
	
	def pass_to_verify(self, captcha_url: str = "", referer_url: str = "", count: int = 0, max_count: int = 1) -> bool:
		"""认证流程
		:param captcha_url:  请求认证的地址
		:param referer_url:  认证的来源地址
		:param count:  重试次数
		:param max_count:  重试最大次数
		:return:  bool
		"""
		if count >= max_count:
			return False
		else:
			if self.tgrairwaysdstl_get():
				self.tgrairwaysdstl_post()
				if self.ajax_header:
					# # # 获取challenge
					self.RCR.url = "https://makeabooking.flyscoot.com/distil_r_captcha_challenge"
					self.RCR.param_data = None
					self.RCR.header = self.BFR.format_to_same(self.init_header)
					self.RCR.header.update({
						"Accept": "*/*",
						"Host": "makeabooking.flyscoot.com",
						"Origin": "https://makeabooking.flyscoot.com",
						"Referer": referer_url,
						"X-Distil-Ajax": self.ajax_header
					})
					self.RCR.post_data = None
					if self.RCR.request_to_post():
						challenge, temp_list = self.BPR.parse_to_regex("(.*?);", self.RCR.page_source)
						if challenge:
							# # # 获取mp3地址
							self.RCR.url = "http://api-na.geetest.com/get.php"
							self.RCR.param_data = (
								("gt", "0fdbade8a0fe41cba0ff758456d23dfa"), ("challenge", challenge),
								("type", "voice"), ("lang", "zh-cn"), ("callback", ""),
							)
							self.RCR.header = self.BFR.format_to_same(self.init_header)
							self.RCR.header.update({
								"Accept": "*/*",
								"Host": "api-na.geetest.com",
								"Referer": referer_url
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
												("gt", "0fdbade8a0fe41cba0ff758456d23dfa"),
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
												get_json = self.RCR.page_source.strip("()")
												get_json = self.BPR.parse_to_dict(get_json)
												validate, temp_list = self.BPR.parse_to_path("$.data.validate",
												                                             get_json)
												cap_url, temp_list = self.BPR.parse_to_regex(
													"url=(.*)", captcha_url)
												if cap_url:
													self.RCR.url = "https://makeabooking.flyscoot.com" + cap_url
												else:
													self.RCR.url = self.verify_url
												# if not validate or not cap_url:
												#     self.logger.info(f"认证提交地址错误(*>﹏<*)【{captcha_url}】")
												#     self.callback_msg = "认证提交地址错误"
												#     return self.pass_to_verify(captcha_url, referer_url, count + 1, max_count)
												# else:
												#     # 提交认证
												#     self.RCR.url = "https://makeabooking.flyscoot.com" + cap_url
												self.RCR.param_data = None
												self.RCR.header = self.BFR.format_to_same(self.init_header)
												self.RCR.header.update({
													"Accept": "*/*",
													"Content-Type": "application/x-www-form-urlencoded",
													"Host": "makeabooking.flyscoot.com",
													"Origin": "https://makeabooking.flyscoot.com",
													"Referer": referer_url,
													"X-Distil-Ajax": self.ajax_header
												})
												self.RCR.post_data = [
													("dCF_ticket", ""), ("geetest_challenge", challenge),
													("geetest_validate", validate),
													("geetest_seccode", f"{validate}|jordan"),
													("isAjax", "1"),
												]
												if self.RCR.request_to_post(status_code=204):
													self.logger.info("语音识别认证成功(*^__^*)【verify】")
													# if  self.tgrairwaysdstl_post():
													return True
			
			self.logger.info(f"认证第{count + 1}次超时或者错误(*>﹏<*)【verify】")
			self.callback_msg = f"认证第{count + 1}次超时或者错误"
			return self.pass_to_verify(captcha_url, referer_url, count + 1, max_count)
	
	def home_page(self, count: int = 0, max_count: int = 3) -> bool:
		if count >= max_count:
			return False
		self.RCR.url = "https://makeabooking.flyscoot.com/"
		self.RCR.param_data = None
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			'Host': "makeabooking.flyscoot.com",
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Sec-Fetch-Mode': 'navigate',
			'Accept-Encoding': 'gzip, deflate, br',
			'Sec-Fetch-Site': 'none',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		})
		if self.RCR.request_to_get(is_redirect=True):
			return True
		self.callback_msg = "首页请求失败"
		return self.home_page(count + 1, max_count)
	
	def tgrairwaysdstl_get(self, count: int = 0, max_count: int = 3) -> bool:
		if count >= max_count:
			return False
		# # # 获取ajax header
		self.RCR.url = "https://makeabooking.flyscoot.com/tgrairwaysdstl.js"
		self.RCR.param_data = None
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			"Accept": "*/*",
			"Host": "makeabooking.flyscoot.com",
			"Referer": "https://makeabooking.flyscoot.com/",
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'Sec-Fetch-Mode': 'no-cors',
			'Sec-Fetch-Site': 'same-origin',
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'zh-CN,zh;q=0.9',
		})
		if self.RCR.request_to_get(is_redirect=True):
			self.ajax_header, temp_list = self.BPR.parse_to_regex('ajax_header:"(.*?)",', self.RCR.page_source)
			self.url_pid, pid_list = self.BPR.parse_to_regex('path:"(.*?)",', self.RCR.page_source)
			return True
		self.callback_msg = "tgrairwaysdstl JS 文件 下载失败"
		return self.tgrairwaysdstl_get(count + 1, max_count)
	
	def tgrairwaysdstl_post(self, count: int = 0, max_count: int = 3) -> bool:
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
		self.RCR.url = 'https://makeabooking.flyscoot.com' + self.url_pid
		self.RCR.post_data = 'p=%7B%22proof%22%3A%22' + self.BPR.parse_to_quote(
			o) + '%22%2C%22fp2%22%3A%7B%22userAgent%22%3A%22Mozilla%2F5.0(WindowsNT10.0%3BWin64%3Bx64)AppleWebKit%2F537.36(KHTML%2ClikeGecko)Chrome%2F76.0.3809.132Safari%2F537.36%22%2C%22language%22%3A%22zh-CN%22%2C%22screen%22%3A%7B%22width%22%3A1920%2C%22height%22%3A1080%2C%22availHeight%22%3A1050%2C%22availWidth%22%3A1920%2C%22pixelDepth%22%3A24%2C%22innerWidth%22%3A1920%2C%22innerHeight%22%3A480%2C%22outerWidth%22%3A160%2C%22outerHeight%22%3A28%2C%22devicePixelRatio%22%3A1%7D%2C%22timezone%22%3A8%2C%22indexedDb%22%3Atrue%2C%22addBehavior%22%3Afalse%2C%22openDatabase%22%3Atrue%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22Win32%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%22ChromePDFPlugin%3A%3APortableDocumentFormat%3A%3Aapplication%2Fx-google-chrome-pdf~pdf%3BChromePDFViewer%3A%3A%3A%3Aapplication%2Fpdf~pdf%3BNativeClient%3A%3A%3A%3Aapplication%2Fx-nacl~%2Capplication%2Fx-pnacl~%22%2C%22canvas%22%3A%7B%22winding%22%3A%22yes%22%2C%22towebp%22%3Atrue%2C%22blending%22%3Atrue%2C%22img%22%3A%22aa281d97036237523f94f8257835ad78225ae962%22%7D%2C%22webGL%22%3A%7B%22img%22%3A%22bd6549c125f67b18985a8c509803f4b883ff810c%22%2C%22extensions%22%3A%22ANGLE_instanced_arrays%3BEXT_blend_minmax%3BEXT_color_buffer_half_float%3BEXT_disjoint_timer_query%3BEXT_float_blend%3BEXT_frag_depth%3BEXT_shader_texture_lod%3BEXT_texture_filter_anisotropic%3BWEBKIT_EXT_texture_filter_anisotropic%3BEXT_sRGB%3BKHR_parallel_shader_compile%3BOES_element_index_uint%3BOES_standard_derivatives%3BOES_texture_float%3BOES_texture_float_linear%3BOES_texture_half_float%3BOES_texture_half_float_linear%3BOES_vertex_array_object%3BWEBGL_color_buffer_float%3BWEBGL_compressed_texture_s3tc%3BWEBKIT_WEBGL_compressed_texture_s3tc%3BWEBGL_compressed_texture_s3tc_srgb%3BWEBGL_debug_renderer_info%3BWEBGL_debug_shaders%3BWEBGL_depth_texture%3BWEBKIT_WEBGL_depth_texture%3BWEBGL_draw_buffers%3BWEBGL_lose_context%3BWEBKIT_WEBGL_lose_context%22%2C%22aliasedlinewidthrange%22%3A%22%5B1%2C1%5D%22%2C%22aliasedpointsizerange%22%3A%22%5B1%2C1024%5D%22%2C%22alphabits%22%3A8%2C%22antialiasing%22%3A%22yes%22%2C%22bluebits%22%3A8%2C%22depthbits%22%3A24%2C%22greenbits%22%3A8%2C%22maxanisotropy%22%3A16%2C%22maxcombinedtextureimageunits%22%3A32%2C%22maxcubemaptexturesize%22%3A16384%2C%22maxfragmentuniformvectors%22%3A1024%2C%22maxrenderbuffersize%22%3A16384%2C%22maxtextureimageunits%22%3A16%2C%22maxtexturesize%22%3A16384%2C%22maxvaryingvectors%22%3A30%2C%22maxvertexattribs%22%3A16%2C%22maxvertextextureimageunits%22%3A16%2C%22maxvertexuniformvectors%22%3A4096%2C%22maxviewportdims%22%3A%22%5B32767%2C32767%5D%22%2C%22redbits%22%3A8%2C%22renderer%22%3A%22WebKitWebGL%22%2C%22shadinglanguageversion%22%3A%22WebGLGLSLES1.0(OpenGLESGLSLES1.0Chromium)%22%2C%22stencilbits%22%3A0%2C%22vendor%22%3A%22WebKit%22%2C%22version%22%3A%22WebGL1.0(OpenGLES2.0Chromium)%22%2C%22vertexshaderhighfloatprecision%22%3A23%2C%22vertexshaderhighfloatprecisionrangeMin%22%3A127%2C%22vertexshaderhighfloatprecisionrangeMax%22%3A127%2C%22vertexshadermediumfloatprecision%22%3A23%2C%22vertexshadermediumfloatprecisionrangeMin%22%3A127%2C%22vertexshadermediumfloatprecisionrangeMax%22%3A127%2C%22vertexshaderlowfloatprecision%22%3A23%2C%22vertexshaderlowfloatprecisionrangeMin%22%3A127%2C%22vertexshaderlowfloatprecisionrangeMax%22%3A127%2C%22fragmentshaderhighfloatprecision%22%3A23%2C%22fragmentshaderhighfloatprecisionrangeMin%22%3A127%2C%22fragmentshaderhighfloatprecisionrangeMax%22%3A127%2C%22fragmentshadermediumfloatprecision%22%3A23%2C%22fragmentshadermediumfloatprecisionrangeMin%22%3A127%2C%22fragmentshadermediumfloatprecisionrangeMax%22%3A127%2C%22fragmentshaderlowfloatprecision%22%3A23%2C%22fragmentshaderlowfloatprecisionrangeMin%22%3A127%2C%22fragmentshaderlowfloatprecisionrangeMax%22%3A127%2C%22vertexshaderhighintprecision%22%3A0%2C%22vertexshaderhighintprecisionrangeMin%22%3A31%2C%22vertexshaderhighintprecisionrangeMax%22%3A30%2C%22vertexshadermediumintprecision%22%3A0%2C%22vertexshadermediumintprecisionrangeMin%22%3A31%2C%22vertexshadermediumintprecisionrangeMax%22%3A30%2C%22vertexshaderlowintprecision%22%3A0%2C%22vertexshaderlowintprecisionrangeMin%22%3A31%2C%22vertexshaderlowintprecisionrangeMax%22%3A30%2C%22fragmentshaderhighintprecision%22%3A0%2C%22fragmentshaderhighintprecisionrangeMin%22%3A31%2C%22fragmentshaderhighintprecisionrangeMax%22%3A30%2C%22fragmentshadermediumintprecision%22%3A0%2C%22fragmentshadermediumintprecisionrangeMin%22%3A31%2C%22fragmentshadermediumintprecisionrangeMax%22%3A30%2C%22fragmentshaderlowintprecision%22%3A0%2C%22fragmentshaderlowintprecisionrangeMin%22%3A31%2C%22fragmentshaderlowintprecisionrangeMax%22%3A30%2C%22unmaskedvendor%22%3A%22GoogleInc.%22%2C%22unmaskedrenderer%22%3A%22ANGLE(Intel(R)HDGraphics630Direct3D11vs_5_0ps_5_0)%22%7D%2C%22touch%22%3A%7B%22maxTouchPoints%22%3A0%2C%22touchEvent%22%3Afalse%2C%22touchStart%22%3Afalse%7D%2C%22video%22%3A%7B%22ogg%22%3A%22probably%22%2C%22h264%22%3A%22probably%22%2C%22webm%22%3A%22probably%22%7D%2C%22audio%22%3A%7B%22ogg%22%3A%22probably%22%2C%22mp3%22%3A%22probably%22%2C%22wav%22%3A%22probably%22%2C%22m4a%22%3A%22maybe%22%7D%2C%22vendor%22%3A%22GoogleInc.%22%2C%22product%22%3A%22Gecko%22%2C%22productSub%22%3A%2220030107%22%2C%22browser%22%3A%7B%22ie%22%3Afalse%2C%22chrome%22%3Atrue%2C%22webdriver%22%3Afalse%7D%2C%22window%22%3A%7B%22historyLength%22%3A3%2C%22hardwareConcurrency%22%3A8%2C%22iframe%22%3Afalse%2C%22battery%22%3Atrue%7D%2C%22location%22%3A%7B%22protocol%22%3A%22https%3A%22%7D%2C%22fonts%22%3A%22Calibri%3BCentury%3BHaettenschweiler%3BLeelawadee%3BMarlett%3BPristina%3BSimHei%22%2C%22devices%22%3A%7B%22count%22%3A4%2C%22data%22%3A%7B%220%22%3A%7B%22deviceId%22%3A%22default%22%2C%22groupId%22%3A%22557fbc5fde847ebf1703626ea534a580379b8d4b7f836f66844c6ec6a7bd9f0c%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%2C%221%22%3A%7B%22deviceId%22%3A%22communications%22%2C%22groupId%22%3A%22557fbc5fde847ebf1703626ea534a580379b8d4b7f836f66844c6ec6a7bd9f0c%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%2C%222%22%3A%7B%22deviceId%22%3A%22c53f141051186ea05707e5efb6ced0e16d8d85413cdd9f062d9db802f6d10773%22%2C%22groupId%22%3A%2219316e1c613c06a2c2eca450017773260e0901e4bd3a09cdfb704feb9ca9eabe%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%2C%223%22%3A%7B%22deviceId%22%3A%22eb60b3cb1f9977b074f5bc3ef57c81c2296f99f905bef86b7a21b2f36092619c%22%2C%22groupId%22%3A%22557fbc5fde847ebf1703626ea534a580379b8d4b7f836f66844c6ec6a7bd9f0c%22%2C%22kind%22%3A%22audiooutput%22%2C%22label%22%3A%22%22%7D%7D%7D%7D%2C%22cookies%22%3A1%2C%22setTimeout%22%3A0%2C%22setInterval%22%3A0%2C%22appName%22%3A%22Netscape%22%2C%22platform%22%3A%22Win32%22%2C%22syslang%22%3A%22zh-CN%22%2C%22userlang%22%3A%22zh-CN%22%2C%22cpu%22%3A%22%22%2C%22productSub%22%3A%2220030107%22%2C%22plugins%22%3A%7B%220%22%3A%22ChromePDFPlugin%22%2C%221%22%3A%22ChromePDFViewer%22%2C%222%22%3A%22NativeClient%22%7D%2C%22mimeTypes%22%3A%7B%220%22%3A%22application%2Fpdf%22%2C%221%22%3A%22PortableDocumentFormatapplication%2Fx-google-chrome-pdf%22%2C%222%22%3A%22NativeClientExecutableapplication%2Fx-nacl%22%2C%223%22%3A%22PortableNativeClientExecutableapplication%2Fx-pnacl%22%7D%2C%22screen%22%3A%7B%22width%22%3A1920%2C%22height%22%3A1080%2C%22colorDepth%22%3A24%7D%2C%22fonts%22%3A%7B%220%22%3A%22Calibri%22%2C%221%22%3A%22Cambria%22%2C%222%22%3A%22Times%22%2C%223%22%3A%22Constantia%22%2C%224%22%3A%22LucidaBright%22%2C%225%22%3A%22Georgia%22%2C%226%22%3A%22SegoeUI%22%2C%227%22%3A%22Candara%22%2C%228%22%3A%22TrebuchetMS%22%2C%229%22%3A%22Verdana%22%2C%2210%22%3A%22Consolas%22%2C%2211%22%3A%22LucidaConsole%22%2C%2212%22%3A%22LucidaSansTypewriter%22%2C%2213%22%3A%22DejaVuSansMono%22%2C%2214%22%3A%22CourierNew%22%2C%2215%22%3A%22Courier%22%7D%7D'
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			"Host": "makeabooking.flyscoot.com",
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'Sec-Fetch-Mode': 'cors',
			'Origin': 'https://makeabooking.flyscoot.com',
			'X-Distil-Ajax': self.ajax_header,
			'Content-Type': 'text/plain;charset=UTF-8',
			'Accept': '*/*',
			'Sec-Fetch-Site': 'same-origin',
			"Accept-Encoding": "gzip, deflate, br",
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
			'Referer': 'http://makeabooking.flyscoot.com/',
		})
		if self.RCR.request_to_post(is_redirect=True):
			self.logger.info(self.RCR.get_from_cookies())
			return True
		self.callback_msg = "tgrairwaysdstl JS 文件 PSOT 失败"
		return self.tgrairwaysdstl_post(count + 1, max_count)
	
	def distil_identify_cookie(self, count: int = 0, max_count: int = 3) -> bool:
		if count >= max_count:
			return False
		self.DG_ZUID = self.RCR.get_from_cookies().get('DG_ZUID')
		self.RCR.url = f"https://makeabooking.flyscoot.com/distil_identify_cookie.html?httpReferrer=%2F&uid={self.DG_ZUID}"
		self.logger.info(self.RCR.url)
		self.RCR.param_data = None
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			"Host": "makeabooking.flyscoot.com",
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
			'Referer': "https://makeabooking.flyscoot.com/",
		})
		if self.RCR.request_to_get(is_redirect=True):
			return True
		return self.distil_identify_cookie(count + 1, max_count)
	
	def set_cookies_acw_sc(self):
		arg1 = self.RCR.page_source[25:65]
		base = "3000176000856006061501533003690027800375"
		trans = ""
		res = ''
		try:
			list_1 = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16,
			          0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7,
			          0x4, 0x11, 0x5,
			          0x3, 0x1c, 0x22, 0x25, 0xc, 0x24]
			for i in range(len(list_1)):
				trans += arg1[list_1[i] - 1]
			for i in range(0, len(trans), 2):
				v1 = int(trans[i: i + 2], 16)
				v2 = int(base[i: i + 2], 16)
				res += "%02x" % (v1 ^ v2)
			self.RCR.set_to_cookies(include_domain=False,
			                        cookie_list=[{"name": 'acw_sc_v2',
			                                      "value": res,
			                                      # 'domain': 'makeabooking.flyscoot.com',
			                                      # 'path': '/'
			                                      }]
			                        )
			return True
		except Exception as ex:
			self.callback_msg = f"设置 Cookie 失败 | {ex}"
			return False
	
	def query_from_home(self, count: int = 0, max_count: int = 5) -> bool:
		"""首页查询航班流程
		:return:  bool
		"""
		if count >= max_count:
			if "distil_r_captcha.html" in self.RCR.page_source:
				self.callback_msg = "验证失败"
				self.logger.info(self.callback_msg)
				return False
			return False
		if self.home_page():
			if "__RequestVerificationToken" in self.RCR.page_source:
				self.verify_token, token_temp_list = self.DPR.parse_to_attributes(
					"value", "css", "input[name='__RequestVerificationToken']", self.RCR.page_source)
				self.tab_id, temp_list = self.BPR.parse_to_regex("id: '(.*?)'", self.RCR.page_source)
				self.sequence, temp_list = self.BPR.parse_to_regex("sequence: (.*?),",
				                                                   self.RCR.page_source)
				if self.tgrairwaysdstl_get():
					if self.tgrairwaysdstl_post():
						return True
				return True
			elif "distilCaptchaForm" in self.RCR.page_source:
				action_url, temp_list = self.DPR.parse_to_attributes("action", "css",
				                                                     "#distilCaptchaForm",
				                                                     self.RCR.page_source)
				self.verify_url = "http://makeabooking.flyscoot.com" + action_url
				self.logger.info(f'验证地址 | {self.verify_url}')
				if self.pass_to_verify(referer_url=self.RCR.url):
					self.tgrairwaysdstl_post()
					return self.query_from_home(count + 1, max_count)
			elif "distil_r_captcha.html" in self.RCR.page_source:
				verify_url, temp_list = self.BPR.parse_to_regex('url=(.*?)"', self.RCR.page_source)
				self.verify_url = "https://makeabooking.flyscoot.com" + verify_url
				self.logger.info(self.verify_url)
				# if self.pass_to_verify():
				# if self.tgrairwaysdstl_get():
				#     if self.tgrairwaysdstl_post():
				# self.RCR.session.cookies.clear()
				if self.pass_to_verify(referer_url=self.RCR.url):
					self.tgrairwaysdstl_post()
					return self.query_from_home(count + 1, max_count)
			elif "ruxitagentjs" in self.RCR.page_source:
				return False
			else:
				self.set_cookies_acw_sc()
				self.callback_msg = "封禁IP， 设置Cookie"
				# self.home_page()
				# self.tgrairwaysdstl_get()
				# self.tgrairwaysdstl_post()
				return self.query_from_home(count + 1, max_count)
		self.callback_msg = f"首页请求失败 | {self.RCR.url}"
		return False
	
	def query_from_detail(self, count: int = 0, max_count: int = 4) -> bool:
		"""查询航班详情信息流程
		:param count:  重试次数
		:param max_count:  重试最大次数
		:return:  bool
		"""
		if count >= max_count:
			return False
		else:
			self.RCR.url = 'https://makeabooking.flyscoot.com/'
			flight_date = self.DFR.format_to_transform(self.CPR.departure_date, "%Y%m%d")
			flight_date = flight_date.strftime("%m/%d/%Y")
			self.RCR.post_data = {
				'__RequestVerificationToken': self.verify_token,
				'revAvailabilitySearch.SearchInfo.Direction': 'Oneway',
				'revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureStationCode': self.CPR.departure_code,
				'revAvailabilitySearch.SearchInfo.SearchStations[0].ArrivalStationCode': self.CPR.arrival_code,
				'revAvailabilitySearch.SearchInfo.SearchStations[0].DepartureDate': flight_date,
				'revAvailabilitySearch.SearchInfo.SearchStations[1].DepartureDate': '',
				'revAvailabilitySearch.SearchInfo.AdultCount': '1',
				'revAvailabilitySearch.SearchInfo.ChildrenCount': '0',
				'revAvailabilitySearch.SearchInfo.InfantCount': '0',
				'revAvailabilitySearch.SearchInfo.PromoCode': '',
				'__tabid': self.tab_id,
				'__requestSequence': self.sequence,
				'__scoot_page_info': '{"interactionCount":{"scroll":8,"click":7,"keyup":6},"inputCount":22,"hasRetainContactDetail":""}'
			}
			self.RCR.header = self.BFR.format_to_same(self.init_header)
			self.RCR.header.update({
				'Cache-Control': 'max-age=0',
				"Connection": "Keep-Alive",
				"Host": "makeabooking.flyscoot.com",
				"Accept-Encoding": "gzip, deflate, br",
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
				'Upgrade-Insecure-Requests': '1',
				'Referer': 'https://makeabooking.flyscoot.com/',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			})
			if self.RCR.request_to_post(is_redirect=True):
				if "distilIdentificationBlock" in self.RCR.page_source:
					self.callback_msg = "验证失败， 出现 Bloack"
					self.home_page()
					self.tgrairwaysdstl_get()
					self.tgrairwaysdstl_post()
					self.distil_identify_cookie()
					return self.query_from_detail(count + 2, max_count)
				if "distilIdentificationBlockPOST" in self.RCR.page_source:
					# self.logger.info("验证是否是浏览器")
					self.tgrairwaysdstl_get()
					self.tgrairwaysdstl_post()
					self.home_page()
					if "__RequestVerificationToken" in self.RCR.page_source:
						return self.query_from_detail(count + 1, max_count)
					else:
						self.tgrairwaysdstl_get()
						self.tgrairwaysdstl_post()
						self.pass_to_verify(referer_url=self.RCR.url)
						self.query_from_detail(count + 1, max_count)
						return False
				if "__RequestVerificationToken" in self.RCR.page_source:
					flight_table, temp_list = self.DPR.parse_to_attributes("id", "css", "#departure-results",
					                                                       self.RCR.page_source)
					if not flight_table:
						self.callback_msg = f"查询不到航线信息(*>﹏<*)【{self.CPR.departure_code} | {self.CPR.arrival_code}】"
						self.logger.info(self.callback_msg)
						# 切换日期进行重新搜索
						# 获取 7 天航班日期
						flight_date, flight_date_list = self.DPR.parse_to_attributes("onclick", "css",
						                                                             f"[data-market-pair='{self.CPR.departure_code + self.CPR.arrival_code}']",
						                                                             self.RCR.page_source)
						flight_price, flight_price_list = self.DPR.parse_to_attributes("text", "css",
						                                                               f"[data-market-pair='{self.CPR.departure_code + self.CPR.arrival_code}'] strong",
						                                                               self.RCR.page_source)
						for i in flight_date_list:
							if "return false" in i:
								continue
							else:
								break
						else:
							self.callback_msg = f"最近 7 天航班无价格信息【{self.CPR.departure_code} | {self.CPR.arrival_code}】"
							self.logger.info(self.callback_msg)
							return False
						num_index = -1
						if len(flight_price_list) == len(flight_date_list):
							for num in range(len(flight_price_list)):
								if "No flights" in flight_price_list[num]:
									continue
								else:
									num_index = num
									break
						if num_index == -1:
							self.callback_msg = f"最近 7 天航班无价格信息【{self.CPR.departure_code} | {self.CPR.arrival_code}】"
							self.logger.info(self.callback_msg)
							return False
						foreign_price, temp_foreign_price_list = self.BPR.parse_to_regex(
							".*?([0-9]{2}.[0-9]{2}.[0-9]{4})", str(flight_date_list[num_index]))
						self.CPR.flight_date = self.DFR.format_to_transform(foreign_price, '%m/%d/%Y').strftime(
							'%Y%m%d')
						return self.query_from_detail(count, max_count)
					self.temp_source = self.BFR.format_to_same(self.RCR.page_source)
					return True
				elif "distilCaptchaForm" in self.RCR.page_source:
					action_url, temp_list = self.DPR.parse_to_attributes("action", "css",
					                                                     "#distilCaptchaForm",
					                                                     self.RCR.page_source)
					self.verify_url = "http://makeabooking.flyscoot.com" + action_url
					self.logger.info(self.verify_url)
					if self.pass_to_verify(referer_url=self.RCR.url):
						if self.home_page():
							self.logger.info("home page")
							return self.query_from_detail(count + 1, max_count)
				elif "distil_r_blocked" in self.RCR.page_source:
					self.callback_msg = "验证地址 distil_r_blocked"
					self.logger.info(self.callback_msg)
					return False
				elif "acw_sc_v2" in self.RCR.page_source:
					arg1 = self.RCR.page_source[25:65]
					base = "3000176000856006061501533003690027800375"
					trans = ""
					res = ''
					list_1 = [0xf, 0x23, 0x1d, 0x18, 0x21, 0x10, 0x1, 0x26, 0xa, 0x9, 0x13, 0x1f, 0x28, 0x1b, 0x16,
					          0x17, 0x19, 0xd, 0x6, 0xb, 0x27, 0x12, 0x14, 0x8, 0xe, 0x15, 0x20, 0x1a, 0x2, 0x1e, 0x7,
					          0x4, 0x11, 0x5,
					          0x3, 0x1c, 0x22, 0x25, 0xc, 0x24]
					for i in range(len(list_1)):
						trans += arg1[list_1[i] - 1]
					for i in range(0, len(trans), 2):
						v1 = int(trans[i: i + 2], 16)
						v2 = int(base[i: i + 2], 16)
						res += "%02x" % (v1 ^ v2)
					self.RCR.set_to_cookies(include_domain=False,
					                        cookie_list=[{"name": 'acw_sc_v2',
					                                      "value": res,
					                                      # 'domain':'makeabooking.flyscoot.com',
					                                      # 'path':'/'
					                                      }]
					                        )
					self.query_from_home()
					self.callback_msg = "封禁IP， 设置Cookie"
					return self.query_from_detail(count + 1, max_count)
				elif "dUF_form_fields" in self.RCR.page_source:
					self.callback_msg = "填写表格"
					return False
				else:
					self.callback_msg = "出现异常，未知错误"
					return False
	
	def get_baggage(self, count: int = 0, max_count: int = 3) -> bool:
		'''
		获取行李页面
		:param count:
		:param max_count:
		:return:
		'''
		if count >= max_count:
			return False
		self.sell_keys, sell_list = self.DPR.parse_to_attributes(
			"value", "css", "div[data-fare='fly'] input[id='revAvailabilitySelect_MarketKeys_0_']",
			self.RCR.page_source)
		self.verify_token, token_temp_list = self.DPR.parse_to_attributes(
			"value", "css", "input[name='__RequestVerificationToken']", self.RCR.page_source)
		self.tab_id, temp_list = self.BPR.parse_to_regex("id: '(.*?)'", self.RCR.page_source)
		self.RCR.url = 'https://makeabooking.flyscoot.com/BookApi/Summary'
		self.RCR.param_data = None
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			"Accept": "text/plain, */*; q=0.01",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			"Host": "makeabooking.flyscoot.com",
			"Origin": "https://makeabooking.flyscoot.com",
			"Referer": "https://makeabooking.flyscoot.com/Book/Flight",
			"X-Distil-Ajax": self.ajax_header,
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
			"X-Requested-With": "XMLHttpRequest"
		})
		self.RCR.post_data = [
			("revBookingSummary.MarketSellKeys[0]", self.sell_keys),
			("__tabid", self.tab_id),
			("__RequestVerificationToken", self.verify_token),
		]
		if self.RCR.request_to_post():
			if self.baggage_page():
				return True
		self.callback_msg = f"行李数据未找到| {self.RCR.url}"
		return self.get_baggage(count + 1, max_count)
	
	def baggage_page(self, count: int = 0, max_count: int = 3):
		'''
		提交航班信息
		:param count:
		:param max_count:
		:return:
		'''
		self.sell_keys, sell_list = self.DPR.parse_to_attributes(
			"value", "css", "div[data-fare='fly'] input[id='revAvailabilitySelect_MarketKeys_0_']",
			self.temp_source)
		self.verify_token, token_temp_list = self.DPR.parse_to_attributes(
			"value", "css", "input[name='__RequestVerificationToken']", self.temp_source)
		self.tab_id, temp_list = self.BPR.parse_to_regex("id: '(.*?)'", self.temp_source)
		self.RCR.url = 'https://makeabooking.flyscoot.com/Book/Flight'
		self.RCR.param_data = None
		self.RCR.header = self.BFR.format_to_same(self.init_header)
		self.RCR.header.update({
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
			"Host": "makeabooking.flyscoot.com",
			'Referer': 'https://makeabooking.flyscoot.com/Book/Flight',
			'Connection': 'keep-alive',
			'Pragma': 'no-cache',
			'Cache-Control': 'no-cache',
			'Origin': 'https://makeabooking.flyscoot.com',
			'Upgrade-Insecure-Requests': '1',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
		})
		self.RCR.post_data = [
			("__RequestVerificationToken", self.verify_token),
			("revAvailabilitySelect.init", ""),
			("revAvailabilitySelect.MarketKeys[0]", self.sell_keys),
			("__tabid", self.tab_id),
			('__requestSequence', self.sequence),
			("__scoot_page_info",
			 '{"interactionCount":{"click":4,"scroll":7},"inputCount":22,"hasRetainContactDetail":""}'),
		]
		if self.RCR.request_to_post(is_redirect=True):
			if "baggage-listing" in self.RCR.page_source:
				return True
			else:
				if "distil_r_captcha.html" in self.RCR.page_source:
					verify_url, temp_list = self.BPR.parse_to_regex('url=(.*?)"', self.RCR.page_source)
					self.verify_url = "https://makeabooking.flyscoot.com" + verify_url
					self.logger.info(self.verify_url)
					# if self.tgrairwaysdstl_get():
					#     if self.tgrairwaysdstl_post():
					if self.pass_to_verify(referer_url=self.RCR.url):
						return self.baggage_page(count + 1, max_count)
			return True
	
	def get_for_record(self, count: int = 0, max_count: int = 3):
		"""查询获取行李数据
		:param count:  重试次数
		:param max_count:  重试最大次数
		:return:  bool
		"""
		if count >= max_count:
			return False
		else:
			luggage, luggage_list = self.DPR.parse_to_attributes("text", "css",
			                                                     "[data-name='baggages'] .baggage-listing .visible-xs-block select[class='form-control control-select'] option[value]",
			                                                     self.RCR.page_source)
			if not luggage:
				self.callback_msg = "行李提取失败"
				return False
			for i in luggage_list:
				if "Thanks" in i:
					continue
				else:
					foreign_price, temp_foreign_price_list = self.BPR.parse_to_regex("\([A-Z]+(.*)\)", i)
					foreign_price = self.BFR.format_to_float(2, foreign_price)
					# self.logger.info(temp_foreign_price_list)
					temp = i.split('kg')
					luggage_currency, temp_luggage_currency = self.BPR.parse_to_regex("([A-Z]{3})", i)
					dict_temp = {}
					dict_temp['departure_aircode'] = self.CPR.departure_code
					dict_temp['arrival_aircode'] = self.CPR.arrival_code
					dict_temp['baggage_weight'] = temp[0]  # 行李重量
					dict_temp['foreign_currency'] = luggage_currency  # 原始货币
					dict_temp['foreign_price'] = foreign_price  # 行李价格
					dict_temp['carrier'] = "tr"  # 行李获取的日期
					# dict_temp['rmb_price'] = rmb_price       # 人民币价格
					self.baggage_data.append(dict_temp)
				if self.baggage_data == []:
					self.callback_msg = "行李提取失败"
					return False
			return True
	
	def return_to_data(self) -> bool:
		"""返回结果数据
		:return:  bool
		"""
		self.callback_data["success"] = "true"
		self.callback_data['msg'] = "更新成功"
		self.callback_data["baggages"] = self.baggage_data  # 行李数据
		self.logger.info(self.callback_data)
		return True