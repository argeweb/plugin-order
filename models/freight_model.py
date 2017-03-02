#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields
from freight_type_model import FreightTypeModel


class FreightModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'系統編號')
    freight_type = Fields.CategoryProperty(verbose_name=u'寄送方式', kind=FreightTypeModel)
    start_amount = Fields.IntegerProperty(verbose_name=u'起始金額', default=0)
    end_amount = Fields.IntegerProperty(verbose_name=u'結束金額', default=0)
    freight_amount = Fields.IntegerProperty(verbose_name=u'運費', default=0)
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u'啟用')
