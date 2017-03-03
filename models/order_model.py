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


class OrderModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'系統編號')
    user = Fields.KeyProperty(verbose_name=u'使用者', kind=ApplicationUserModel)
    order_no = Fields.StringProperty(verbose_name=u'訂單編號', default=u'')
    purchaser_name = Fields.StringProperty(verbose_name=u'購買人姓名')
    purchaser_email = Fields.StringProperty(verbose_name=u'購買人 E-Mail')
    recipient_name = Fields.StringProperty(verbose_name=u'收件人姓名')
    recipient_telephone = Fields.StringProperty(verbose_name=u'收件人電話')
    recipient_mobile = Fields.StringProperty(verbose_name=u'收件人手機')
    recipient_email = Fields.StringProperty(verbose_name=u'收件人 E-Mail')
    recipient_address_country = Fields.StringProperty(verbose_name=u'收件國家')
    recipient_address_city = Fields.StringProperty(verbose_name=u'收件縣市')
    recipient_address_district = Fields.StringProperty(verbose_name=u'收件鄉鎮市區')
    recipient_address_zip = Fields.StringProperty(verbose_name=u'收件郵遞區號')
    recipient_address_detail = Fields.StringProperty(verbose_name=u'收件地址 ')

    sku_link = Fields.SidePanelProperty(verbose_name=u'訂購項目', text=u'點擊此處查看 訂購項目',
                                        uri='admin:order:order_item:list_for_side_panel')

    payment_type = Fields.CategoryProperty(verbose_name=u'付款方式', kind=PaymentTypeModel)
    freight_type = Fields.CategoryProperty(verbose_name=u'寄送方式', kind=FreightTypeModel)
    payment_type_title = Fields.StringProperty(verbose_name=u'付款方式')
    freight_type_title = Fields.StringProperty(verbose_name=u'寄送方式')
    message = Fields.StringProperty(verbose_name=u'備註')
    subtotal_amount = Fields.FloatProperty(verbose_name=u'小計金額')
    freight_amount = Fields.FloatProperty(verbose_name=u'運費')
    shopping_cash = Fields.FloatProperty(verbose_name=u'使用的購物金')
    total_amount = Fields.FloatProperty(verbose_name=u'總金額')
    need_pay_amount = Fields.FloatProperty(verbose_name=u'應付金額')

    status = Fields.IntegerProperty(verbose_name=u'訂單狀態')
    payment_status = Fields.IntegerProperty(verbose_name=u'付款狀態')
    freight_status = Fields.IntegerProperty(verbose_name=u'寄送狀態')

    status_text = Fields.StringProperty(verbose_name=u'訂單狀態')
    payment_status_text = Fields.StringProperty(verbose_name=u'付款狀態')
    freight_status_text = Fields.StringProperty(verbose_name=u'寄送狀態')
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
        return cls.query(cls.status==status).order(-cls.sort)

    def gen_order_no(self):
        from argeweb.core.time_util import localize
        from datetime import datetime
        n = localize(datetime.today()).strftime('%Y%m%d %H%M%S').split(' ')
        return '%s-%s-%s' % (n[0], self.name[0:4], n[1])

    def before_put(self):
        super(OrderModel, self).before_put()
        if self.order_no is u'':
            self.order_no = self.gen_order_no()
        try:
            self.payment_type_title = self.payment_type.get().title
        except:
            self.payment_type_title = u''
        try:
            self.freight_type_title = self.freight_type.get().title
        except:
            self.freight_type_title = u''
        status_text_list = [
            u'尚未確認', u'新訂單', u'已付款', u'備貨中', u'已出貨', u'已結單', u'異常流程', u'取消訂單']
        payment_status_text_list = [
            u'未確認', u'待付款', u'已付款', u'退款中', u'已退款', u'購物金全款付款', u'購物金部分付款']
        freight_status_text_list = [
            u'未確認', u'未出貨', u'備貨中', u'補貨中', u'已出貨', u'已寄達', u'部分出貨', u'缺貨']
        self.status_text = status_text_list[int(self.status)]
        self.payment_status_text = payment_status_text_list[int(self.payment_status)]
        self.freight_status_text = freight_status_text_list[int(self.freight_status)]