#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import BasicConfigModel
from argeweb import Fields


class ConfigModel(BasicConfigModel):
    title = Fields.HiddenProperty(verbose_name=u'設定名稱', default=u'訂單相關設定')

    after_pay_uri = Fields.StringProperty(verbose_name=u'付款後 重新導向 URI', default=u'/pay_done.html')
    after_pay_uri_error = Fields.StringProperty(verbose_name=u'付款後 重新導向 URI (Error)', default=u'/pay_error.html')
    create_with_supplier = Fields.BooleanProperty(verbose_name=u'依供應商建立訂單', default=False)
    use_supplier = Fields.BooleanProperty(verbose_name=u'顯示供應商欄位', default=False)
    notice_supplier = Fields.BooleanProperty(verbose_name=u'通知供應商', default=False)
    show_convenience_stores = Fields.BooleanProperty(verbose_name=u'顯示超商取貨相關欄位', default=False)
    show_cost = Fields.BooleanProperty(verbose_name=u'顯示成本相關欄位', default=False)
    show_invoice = Fields.BooleanProperty(verbose_name=u'顯示發票相關欄位', default=False)

    show_currency = Fields.BooleanProperty(verbose_name=u'顯示貨幣相關欄位', default=False)
    show_freight_check_target = Fields.BooleanProperty(verbose_name=u'顯示運費計算目標', default=False)
    show_report_filed = Fields.BooleanProperty(verbose_name=u'顯示報表相關欄位', default=False)

    debug_mode = Fields.BooleanProperty(verbose_name=u'除錯模式', default=False)
