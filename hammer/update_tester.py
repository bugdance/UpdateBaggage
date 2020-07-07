#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""Script test.

written by pyLeo.
"""
# Import current path.
import sys
sys.path.append('..')
# # # Analog interface.
import requests
from datetime import datetime
import time
import logging

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from explorer.pers5j_scraper import Pers5JScraper
from explorer.persdy_scraper import PersDYScraper
from explorer.perstr_scraper import PersTRScraper
from explorer.persvj_scraper import PersVJScraper
from explorer.persvy_scraper import PersVYScraper
from explorer.persye_scraper import PersYEScraper
from explorer.persmm_scraper import PersMMScraper


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


airline_account = "pers"
airline_company = "vy"
create_var = locals()
scraper = create_var[airline_account.capitalize() + airline_company.upper() + "Scraper"]()


def insert_routes():
    post_data = {"carrier": "5J", "departureAirport": "SIN", "arriveAirport": "CJB",
                 "currency": "MOP", "departureTime": "20191231",
                 "returnTime": "", "updateId": "23333"}

    process_dict = {
        "task_id": 1111, "log_path": "test.log", "source_dict": post_data,
        "enable_proxy": False, "address": "http://127.0.0.1:8888", "retry_count": 2
    }

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
    result = Routes.query.filter(Routes.carrier == "VY").all()
    result = list(result)
    if not result:
        app.logger.info(f"wn刷值写入数据库错误")
    else:
        for i in result:
            post_data = {"carrier": i.carrier, "departureAirport": i.departure_aircode,
                         "arriveAirport": i.arrival_aircode,
                         "currency": i.foreign_currency, "departureTime": "20200110",
                         "returnTime": "", "updateId": i.carrier}
            process_dict = {
                "task_id": 1111, "log_path": "test.log", "source_dict": post_data,
                "enable_proxy": False, "address": "http://127.0.0.1:8888", "retry_count": 2
            }

            res = scraper.process_to_main(process_dict)
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
            time.sleep(5)

# scheduler = APScheduler()
# scheduler.init_app(app=app)
# # scheduler.add_job(func=insert_routes, id='insert_routes', trigger='cron',
# #                   day_of_week=1, minute=0, next_run_time=datetime.now())
# scheduler.add_job(func=select_routes, id='select_routes', trigger='cron',
#                   day_of_week=1, minute=0, next_run_time=datetime.now())
# scheduler.start()
#
#
# if __name__ == '__main__':
#     app.run(debug=False, host='127.0.0.1', port=11111, threaded=True)


post_data = {"carrier": "VY", "departureAirport": "TPE", "arriveAirport": "NRT",
             "currency": "MOP", "departureTime": "20200123",
             "returnTime": "", "updateId": "23333"}


def post_test():
    """

    Returns:

    """
    company = "tr"
    url = f"http://119.3.249.135:18082/update/{company}/"
    response = requests.post(url=url, json=post_data)
    print(response.text)


if __name__ == '__main__':

    # post_test()
    while 1:
        process_dict = {
            "task_id": 1111, "log_path": "test.log", "source_dict": post_data,
            "enable_proxy": False, "address": "http://127.0.0.1:8888", "retry_count": 2
        }

        airline_account = "pers"
        airline_company = "dy"
        create_var = locals()
        scraper = create_var[airline_account.capitalize() + airline_company.upper() + "Scraper"]()
        result = scraper.process_to_main(process_dict)
        time.sleep(600)
