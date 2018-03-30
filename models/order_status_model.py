#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields

order_status = {
    'unconfirmed': u'未確認',
    'new_order': u'新訂單',
    'already_paid': u'已付款',
    'stocking': u'備貨中',
    'shipped': u'已出貨',
    'closed': u'訂單完成',
    'abnormal_flow': u'異常流程',
    'order_cancel': u'取消訂單'
}


class OrderStatusModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(verbose_name=u'訂單狀態名稱', default=u'未命名')

    @classmethod
    def create_default_status(cls):
        for name, title in order_status.items():
            cls.get_or_create_by_name(name, title=title)
