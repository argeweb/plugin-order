#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields

order_status_name_index = [
    "unconfirmed",
    "new_order",
    "already_paid",
    "stocking",
    "shipped",
    "closed",
    "abnormal_flow",
    "order_cancel"
]
order_status_name_title = [
    "未確認",
    "新訂單",
    "已付款",
    "備貨中",
    "已出貨",
    "關閉",
    "異常流程",
    "取消訂單"
]


class OrderStatusModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'系統編號')
    title = Fields.StringProperty(default=u'未命名', verbose_name=u'訂單狀態名稱')
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u'啟用')

    @classmethod
    def get_or_create(cls, name):
        r = cls.find_by_name(name)
        if r is None:
            for index in xrange(0, len(order_status_name_index)):
                if name == order_status_name_index[index]:
                    title = order_status_name_title[index]
                    r = cls()
                    r.name = name
                    r.title = title
                    r.put()
        return r

    @classmethod
    def create_default_status(cls):
        for name in order_status_name_index:
            cls.get_or_create(name)
