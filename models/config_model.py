#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import BasicModel
from argeweb import Fields


class ConfigModel(BasicModel):
    title = Fields.StringProperty(verbose_name=u'設定名稱', default=u'訂單相關設定')
    create_with_supplier = Fields.BooleanProperty(verbose_name=u'依供應商建立訂單', default=False)
    notice_supplier = Fields.BooleanProperty(verbose_name=u'通知供應商', default=True)
