#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields

freight_status = {
    'unconfirmed': u'未確認',
    'not_shipped': u'未出貨',
    'stocking': u'備貨中',
    'replenishment': u'補貨中',
    'shipped': u'已出貨',
    'has_arrived': u'已寄達',
    'part_of_the_shipment': u'部分出貨',
    'out_of_stock': u'缺貨'
}


class FreightStatusModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(verbose_name=u'寄送狀態名稱', default=u'未命名')
    is_enable = Fields.BooleanProperty(verbose_name=u'啟用', default=True)

    @classmethod
    def create_default_status(cls):
        for name, title in freight_status.items():
            cls.get_or_create_by_name(name, title=title)