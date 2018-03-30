#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.
import time

from argeweb import BasicModel
from argeweb import Fields
from order_model import OrderModel


class OrderDiscountModel(BasicModel):
    order = Fields.KeyProperty(verbose_name=u'訂單', kind=OrderModel)
    title = Fields.StringProperty(verbose_name=u'折扣說明', default=u'')
    amount = Fields.FloatProperty(verbose_name=u'折扣金額', default=0.0)

    @classmethod
    def all_with_order(cls, order=None, *args, **kwargs):
        return cls.query(cls.order==order.key).order(-cls.sort)
