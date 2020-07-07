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
"""Created on Fri May 10 03:47:45 UTC+8:00 2019
    接收器用于接收接口数据并返回响应数据
written by pyLeo.
"""
# Import current path.
import sys
sys.path.append('..')

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import logging
import requests
from datetime import datetime
import time


from explorer.persye_scraper import PersYEScraper


# # # app实例
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# # # 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1:3306/luggage'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# # # 日志格式化
app.logger = logging.getLogger("flask")
app.logger.setLevel(level=logging.INFO)
app.formatter = logging.Formatter('[%(asctime)s]%(message)s')
# app.handler = logging.FileHandler("post.log")
app.handler = logging.StreamHandler()
app.handler.setFormatter(app.formatter)
app.logger.addHandler(app.handler)



class Monitoring(db.Model):
	"""MM造值表,abck
	"""
	__tablename__ = "monitoring"
	id = db.Column(db.Integer, primary_key=True)
	carrier = db.Column(db.String(2))
	departure_aircode = db.Column(db.String(3))
	arrival_aircode = db.Column(db.String(3))
	baggage_weight = db.Column(db.Integer)
	foreign_currency = db.Column(db.String(3))
	foreign_price = db.Column(db.DECIMAL(11, 2))
	create_date = db.Column(db.Integer)
	china_yuan = db.Column(db.DECIMAL(11, 2))
	
	def __init__(self, carrier, departure_aircode, arrival_aircode, baggage_weight,
	             foreign_currency, foreign_price, create_date, china_yuan):
		self.carrier = carrier
		self.departure_aircode = departure_aircode
		self.arrival_aircode = arrival_aircode
		self.baggage_weight = baggage_weight
		self.foreign_currency = foreign_currency
		self.foreign_price = foreign_price
		self.create_date = create_date
		self.china_yuan = china_yuan


class Failed(db.Model):
	"""WN造值表,header
	"""
	__tablename__ = "failed"
	id = db.Column(db.Integer, primary_key=True)
	carrier = db.Column(db.String(2))
	departure_aircode = db.Column(db.String(3))
	arrival_aircode = db.Column(db.String(3))
	baggage_weight = db.Column(db.Integer)
	foreign_currency = db.Column(db.String(3))
	cause = db.Column(db.String(250))
	
	def __init__(self, carrier, departure_aircode, arrival_aircode, baggage_weight,
	             foreign_currency, cause):
		self.carrier = carrier
		self.departure_aircode = departure_aircode
		self.arrival_aircode = arrival_aircode
		self.baggage_weight = baggage_weight
		self.foreign_currency = foreign_currency
		self.cause = cause


class Routes(db.Model):
	"""WN造值表,header
	"""
	__tablename__ = "routes"
	id = db.Column(db.Integer, primary_key=True)
	carrier = db.Column(db.String(2))
	departure_aircode = db.Column(db.String(3))
	arrival_aircode = db.Column(db.String(3))
	foreign_currency = db.Column(db.String(3))
	departure_time = db.Column(db.String(8))
	return_time = db.Column(db.String(8))
	
	def __init__(self, carrier, departure_aircode, arrival_aircode, foreign_currency,
	             departure_time, return_time):
		self.carrier = carrier
		self.departure_aircode = departure_aircode
		self.arrival_aircode = arrival_aircode
		self.foreign_currency = foreign_currency
		self.departure_time = departure_time
		self.return_time = return_time


# def produce_mm():
# 	"""mm刷abck
# 	:return: None
# 	"""
# 	SC_mm.set_to_delete()
# 	SC_mm.get_from_url("https://booking.flypeach.com/cn")
# 	cookies = SC_mm.get_from_cookies()
# 	for i in cookies:
# 		name = i.get("name")
# 		value = i.get("value")
# 		if name == "_abck" and "~0~" in value and "~-1~-1~-1" in value:
# 			t = int(time.time())
# 			try:
# 				insert = ProduceMM(t, t, value)
# 				db.session.add(insert)
# 				db.session.commit()
# 			except Exception as ex:
# 				app.logger.info(f"mm刷值写入数据库错误{ex}")
# 			else:
# 				pass
# 			break
#
#
#
#
# def delete_wn():
# 	"""wn删除header
# 	:return: None
# 	"""
# 	try:
# 		now = int(time.time())
# 		ProduceWN.query.filter(ProduceWN.create_time < now - 86400).delete()
# 		db.session.commit()
# 	except Exception as ex:
# 		app.logger.info(f"wn删除数据库错误{ex}")
# 	else:
# 		pass


def insert_routes():
	
	post_data = {"carrier": "TR", "departureAirport": "SIN", "arriveAirport": "CJB",
	             "currency": "MOP", "departureTime": "20200110",
	             "returnTime": "", "updateId": "23333"}
	
	process_dict = {
		"task_id": 1111, "log_path": "test.log", "source_dict": post_data,
		"enable_proxy": False, "address": "http://127.0.0.1:8888", "retry_count": 2
	}
	scraper = PersYEScraper()
	result = scraper.process_to_main(process_dict)
	baggage = result.get("baggages")
	if baggage:
		try:
			for i in baggage:
				sql = f"insert ignore into routes(carrier, departure_aircode, arrival_aircode, foreign_currency) " \
				      f"values('%s', '%s', '%s', '%s');" % (i[0], i[1], i[2], i[3])
				db.session.execute(sql)
				
			db.session.commit()
		except Exception as ex:
			app.logger.info(f"wn刷值写入数据库错误{ex}")
		else:
			app.logger.info(f"插入数据库成功")
	else:
		app.logger.info(f"一定行返回为空")
	

def select_routes():



	result = Routes.query.filter(Routes.carrier=="TR").all()
	result = list(result)
	if not result:
		app.logger.info(f"wn刷值写入数据库错误")
	else:
		for i in result:
			post_data = {"carrier": i.carrier, "departureAirport": i.departure_aircode,
			             "arriveAirport": i.arrival_aircode,
			             "currency": i.foreign_currency, "departureTime": "20200110",
			             "returnTime": "", "updateId": i.carrier}
			
			url = "http://119.3.249.135:18082/update/tr/"
			response = requests.post(url=url, json=post_data, timeout=180)
			res = response.json()
			baggage = res.get("baggages")
			if baggage:
				for j in baggage:
					print(j)
					sql = f"insert ignore into monitoring(carrier, departure_aircode, arrival_aircode, baggage_weight, " \
					      f"foreign_currency, foreign_price, create_date, china_yuan) " \
					      f"values('%s', '%s', '%s', '%s', '%s', '%s', 3, 0) ON DUPLICATE KEY UPDATE " \
					      f"foreign_price='%s', create_date='%s';" % \
					      (j['carrier'], j['departure_aircode'], j['arrival_aircode'],
					       j['baggage_weight'], j['foreign_currency'], j['foreign_price'], j['foreign_price'], 11)
					db.session.execute(sql)

					
					cause = "成功"
					sql = f"insert ignore into failed(carrier, departure_aircode, arrival_aircode, " \
					      f"foreign_currency, cause) " \
					      f"values('%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE cause='%s';" % \
					      (i.carrier, i.departure_aircode, i.arrival_aircode,
					       i.foreign_currency, cause, cause)
					db.session.execute(sql)

			else:
				cause = res.get("msg")
				print(cause)
				sql = f"insert ignore into failed(carrier, departure_aircode, arrival_aircode, " \
				      f"foreign_currency, cause) " \
				      f"values('%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE cause='%s';" % \
				      (i.carrier, i.departure_aircode, i.arrival_aircode,
				       i.foreign_currency, cause, cause)
				db.session.execute(sql)
				
			db.session.commit()
			time.sleep(60)
		
	
	



scheduler = APScheduler()
scheduler.init_app(app=app)
# scheduler.add_job(func=produce_mm, id='produce_mm', trigger='interval', seconds=300, next_run_time=datetime.now())
# scheduler.add_job(func=produce_wn, id='produce_wn', trigger='interval', seconds=10800, next_run_time=datetime.now())
# scheduler.add_job(func=delete_mm, id='delete_mm', trigger='cron', hour=0, minute=0)
# scheduler.add_job(func=delete_wn, id='delete_wn', trigger='interval', seconds=21600, next_run_time=datetime.now())

# scheduler.add_job(func=insert_routes, id='insert_routes', trigger='interval',
#                   seconds=3300, next_run_time=datetime.now())
scheduler.add_job(func=select_routes, id='select_routes', trigger='interval',
                  seconds=3300, next_run_time=datetime.now())
scheduler.start()


# # # # 链接地址,例http://x.x.x.x:33334/produce/mm/
# @app.route('/produce/mm/', methods=['POST'])
# def server_mm():
# 	get_dict = BP.parse_as_source(request.get_data())
# 	if not get_dict:
# 		return jsonify({"value": ""})
#
# 	try:
# 		status = get_dict.get("mm")
# 		if status != "abck":
# 			return jsonify({"value": ""})
#
# 		now = int(time.time())
# 		sql = f"select id, produce_value from produce_mm where update_time < {now - 600} order by rand() limit 1;"
# 		result = db.session.execute(sql)
# 		result = list(result)
# 		if result:
# 			number = result[0][0]
# 			value = result[0][1]
# 			ProduceMM.query.filter(ProduceMM.id == number).update({'update_time': now + 180})
# 			db.session.commit()
# 			return jsonify({"value": value})
# 		else:
# 			return jsonify({"value": ""})
# 	except Exception as ex:
# 		app.logger.info(f"从数据库取mm刷值失败{ex}")
# 		return jsonify({"value": ""})
#
#
# # # # 链接地址,例http://x.x.x.x:33334/produce/wn/
# @app.route('/produce/wn/', methods=['POST'])
# def server_wn():
# 	get_dict = BP.parse_as_source(request.get_data())
# 	if not get_dict:
# 		return jsonify({"value": ""})
#
# 	try:
# 		status = get_dict.get("wn")
# 		if status != "header":
# 			return jsonify({"value": ""})
#
# 		now = int(time.time())
# 		sql = f"select produce_value from produce_wn where {now - 86400} < create_time < {now} order by rand() limit 1;"
# 		result = db.session.execute(sql)
# 		result = list(result)
# 		if result:
# 			value = result[0][0]
# 			return jsonify({"value": value})
# 		else:
# 			return jsonify({"value": ""})
# 	except Exception as ex:
# 		app.logger.info(f"从数据库取wn刷值失败{ex}")
# 		return jsonify({"value": ""})


if __name__ == '__main__':
	app.run(debug=False, host='127.0.0.1', port=11111, threaded=True)
