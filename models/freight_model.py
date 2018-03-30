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
    freight_type = Fields.CategoryProperty(verbose_name=u'寄送方式', kind=FreightTypeModel)
    check_target = Fields.StringProperty(verbose_name=u'檢查對象', default=u'total_volumetric_weight', choices=[
        'total_volume', 'total_volumetric_weight', 'total_size',  'total_price', 'total_weight',
    ], choices_text={
        'total_volumetric_weight': u'總材積重 V.W.',
        'total_volume': u'總體積',
        'total_size': u'尺寸合計',
        'total_price': u'金額小計',
        'total_weight': u'重量總重',
    })
    try:
        from plugins.supplier.models.supplier_model import SupplierModel
    except ImportError:
        class SupplierModel(BasicModel):
            pass
    supplier = Fields.CategoryProperty(verbose_name=u'供應商', kind=SupplierModel)

    start_value = Fields.FloatProperty(verbose_name=u'起始範圍 >', default=0.0)
    end_value = Fields.FloatProperty(verbose_name=u'結束範圍 <=', default=0.0)
    freight_amount = Fields.FloatProperty(verbose_name=u'運費', default=0.0)
    is_enable = Fields.BooleanProperty(verbose_name=u'啟用', default=True)

    def check_amount(self, val):
        if self.end_value >= val > self.start_value:
            return self.freight_amount
        return 0.0
