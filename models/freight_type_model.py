#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields


class FreightTypeModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'系統編號')
    title = Fields.StringProperty(default=u'未命名', verbose_name=u'付款方式名稱')
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u'啟用')
