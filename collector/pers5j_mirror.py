#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""Created on Fri May 10 03:47:45 UTC+8:00 2019
    镜像器用于存储稳定的数据, 5J镜像器
written by pyleo.
"""
class Pers5JMirror:
    """5J镜像器
    """
    def __init__(self):
        self.currency_route = {
            'TWD': ('TPE', 'MEL'),
            'KRW': ('ICN', 'KLO'),
            'JPY': ('FUK', 'MNL'),
            'PHP': ('CEB', 'MNL'),
            'MOP': ('MFM', 'MEL'),
            'SGD': ('SIN', 'MNL'),
            'CNY': ('CAN', 'MNL'),
            'HKD': ('HKG', 'CRK'),
            'THB': ('BKK', 'MNL'),
            'MYR': ('BKI', 'MNL'),
            'BND': ('BWN', 'MNL'),
            'AUD': ('SYD', 'MNL'),
            'USD': ('GUM', 'MNL')
        }