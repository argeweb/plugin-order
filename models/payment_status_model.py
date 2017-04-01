#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields

payment_status_name_index = [
    "unconfirmed",
    "pending_payment",
    "already_paid",
    "refunding",
    "refunded",
    "full_payment_with_point",
    "part_payment_with_point"
]
payment_status_name_title = [
    "未確認",
    "待付款",
    "已付款",
    "退款中",
    "已退款",
    "購物金全額付款",
    "購物金部分付款"
]


class PaymentStatusModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(default=u'未命名', verbose_name=u'付款狀態名稱')
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u'啟用')

    @classmethod
    def get_or_create(cls, name):
        r = cls.find_by_name(name)
        if r is None:
            for index in xrange(0, len(payment_status_name_index)):
                if name == payment_status_name_index[index]:
                    title = payment_status_name_title[index]
                    r = cls()
                    r.name = name
                    r.title = title
                    r.put()
        return r

    @classmethod
    def create_default_status(cls):
        for name in payment_status_name_index:
            cls.get_or_create(name)