#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields
from plugins.application_user.models.application_user_model import ApplicationUserModel
from payment_type_model import PaymentTypeModel
from freight_type_model import FreightTypeModel
from payment_status_model import PaymentStatusModel
from freight_status_model import FreightStatusModel
from order_status_model import OrderStatusModel, order_status_name_index


class OrderModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'系統編號')
    sku_link = Fields.SidePanelProperty(verbose_name=u'訂購項目', text=u'點擊此處查看 訂購項目',
                                        uri='admin:order:order_item:list_for_side_panel')

    user = Fields.KeyProperty(verbose_name=u'使用者', kind=ApplicationUserModel)
    order_no = Fields.StringProperty(verbose_name=u'訂單編號', default=u'')
    purchaser_name = Fields.StringProperty(verbose_name=u'購買人姓名', default=u'')
    purchaser_email = Fields.StringProperty(verbose_name=u'購買人 E-Mail', default=u'')
    recipient_name = Fields.StringProperty(verbose_name=u'收件人姓名', default=u'')
    recipient_telephone = Fields.StringProperty(verbose_name=u'收件人電話', default=u'')
    recipient_mobile = Fields.StringProperty(verbose_name=u'收件人手機', default=u'')
    recipient_email = Fields.StringProperty(verbose_name=u'收件人 E-Mail', default=u'')
    recipient_address_country = Fields.StringProperty(verbose_name=u'收件國家', default=u'')
    recipient_address_city = Fields.StringProperty(verbose_name=u'收件縣市', default=u'')
    recipient_address_district = Fields.StringProperty(verbose_name=u'收件鄉鎮市區', default=u'')
    recipient_address_zip = Fields.StringProperty(verbose_name=u'收件郵遞區號', default=u'')
    recipient_address_detail = Fields.StringProperty(verbose_name=u'收件地址 ', default=u'')
    recipient_store_number = Fields.StringProperty(verbose_name=u'超商取貨店號 ', default=u'')
    recipient_store_name = Fields.StringProperty(verbose_name=u'超商取貨店名', default=u'')

    payment_type = Fields.CategoryProperty(verbose_name=u'付款方式', kind=PaymentTypeModel)
    freight_type = Fields.CategoryProperty(verbose_name=u'寄送方式', kind=FreightTypeModel)
    payment_type_title = Fields.SearchingHelperProperty(verbose_name=u'付款方式', target='payment_type', target_field_name='title')
    freight_type_title = Fields.SearchingHelperProperty(verbose_name=u'寄送方式', target='freight_type', target_field_name='title')
    message = Fields.StringProperty(verbose_name=u'備註')
    subtotal_amount = Fields.FloatProperty(verbose_name=u'小計金額')
    freight_amount = Fields.FloatProperty(verbose_name=u'運費')
    shopping_cash = Fields.FloatProperty(verbose_name=u'使用的購物金')
    total_amount = Fields.FloatProperty(verbose_name=u'總金額')
    need_pay_amount = Fields.FloatProperty(verbose_name=u'應付金額')

    status = Fields.CategoryProperty(verbose_name=u'訂單狀態', kind=OrderStatusModel)
    payment_status = Fields.CategoryProperty(verbose_name=u'付款狀態', kind=PaymentStatusModel)
    freight_status = Fields.CategoryProperty(verbose_name=u'寄送狀態', kind=FreightStatusModel)

    status_title = Fields.SearchingHelperProperty(verbose_name=u'訂單狀態', target='status', target_field_name='title')
    payment_status_title = Fields.SearchingHelperProperty(verbose_name=u'付款狀態', target='payment_status', target_field_name='title')
    freight_status_title = Fields.SearchingHelperProperty(verbose_name=u'寄送狀態', target='freight_status', target_field_name='title')
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u'啟用')

    @classmethod
    def all(cls, user=None, *args, **kwargs):
        if user is None:
            return cls.query().order(-cls.sort)
        return cls.query(cls.user==user.key).order(-cls.sort)

    @classmethod
    def all_with_status(cls, status=None, *args, **kwargs):
        if status is None:
            return cls.query().order(-cls.sort)
        s = OrderStatusModel.find_by_name(status)
        return cls.query(cls.status==s.key).order(-cls.sort)

    def gen_order_no(self):
        from argeweb.core.time_util import localize
        from datetime import datetime
        n = localize(datetime.today()).strftime('%Y%m%d %H%M%S').split(' ')
        return '%s-%s-%s' % (n[0], self.name[0:4], n[1])

    def before_put(self):
        super(OrderModel, self).before_put()
        if self.order_no is u'':
            self.order_no = self.gen_order_no()