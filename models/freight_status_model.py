#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields

freight_status_name_index = [
    "unconfirmed",
    "not_shipped",
    "stocking",
    "replenishment",
    "shipped",
    "has_arrived",
    "part_of_the_shipment",
    "out_of_stock"
]
freight_status_name_title = [
    "未確認",
    "未出貨",
    "備貨中",
    "補貨中",
    "已出貨",
    "已寄達",
    "部分出貨",
    "缺貨"
]


class FreightStatusModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(default=u'未命名', verbose_name=u'寄送狀態名稱')
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u'啟用')

    @classmethod
    def get_or_create(cls, name):
        r = cls.find_by_name(name)
        if r is None:
            for index in xrange(0, len(freight_status_name_index)):
                if name == freight_status_name_index[index]:
                    title = freight_status_name_title[index]
                    r = cls()
                    r.name = name
                    r.title = title
                    r.put()
        return r

    @classmethod
    def create_default_status(cls):
        for name in freight_status_name_index:
            cls.get_or_create(name)