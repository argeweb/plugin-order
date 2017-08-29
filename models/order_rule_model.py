#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields


class OrderRuleModel(BasicModel):
    """

    """
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(verbose_name=u'規則名稱', default=u'未命名規則')
    check_target = Fields.StringProperty(verbose_name=u'檢查對象', default=u'')
    check_target_id = Fields.StringProperty(verbose_name=u'對象編號', default=u'')
    check_operation = Fields.StringProperty(verbose_name=u'檢查方式', default=u'')
    check_target_quantity = Fields.StringProperty(verbose_name=u'對象數量', default=u'')
    check_target_count = Fields.StringProperty(verbose_name=u'檢查次數', default=u'')
    calculate_target = Fields.StringProperty(verbose_name=u'計算對象', default=u'')
    multiplication = Fields.StringProperty(verbose_name=u'先增減乘數(%)', default=u'')
    addition = Fields.StringProperty(verbose_name=u'再增減數量', default=u'')
    is_enable = Fields.BooleanProperty(verbose_name=u'啟用', default=True)
