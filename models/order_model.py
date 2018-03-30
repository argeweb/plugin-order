#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.
import time

from google.appengine.ext import ndb

from argeweb import BasicModel
from argeweb import Fields
from plugins.application_user.models.application_user_model import ApplicationUserModel
from plugins.payment_middle_layer.models.payment_type_model import PaymentTypeModel
from plugins.payment_middle_layer.models.payment_status_model import PaymentStatusModel
from plugins.payment_middle_layer.models.payment_order_model import PaymentOrderModel
from freight_type_model import FreightTypeModel
from freight_status_model import FreightStatusModel
from order_status_model import OrderStatusModel


class OrderModel(PaymentOrderModel):
    class Meta:
        tab_pages = [u'物流', u'金流', u'備註', u'發票', u'成本']

    order_no = Fields.StringProperty(verbose_name=u'訂單編號', default=u'')
    order_link = Fields.HiddenProperty(verbose_name=u'訂單連結序號', default=u'')
    status_object = Fields.CategoryProperty(verbose_name=u'訂單狀態', kind=OrderStatusModel)
    status = Fields.HiddenProperty(verbose_name=u'訂單狀態', default=u'')
    status_title = Fields.HiddenProperty(verbose_name=u'訂單狀態', default=u'')

    user = Fields.ApplicationUserProperty(verbose_name=u'使用者', is_lock=True)

    try:
        from plugins.supplier.models.supplier_model import SupplierModel
    except ImportError:
        class SupplierModel(BasicModel):
            pass
    supplier = Fields.CategoryProperty(verbose_name=u'供應商', kind=SupplierModel)
    supplier_name = Fields.HiddenProperty(verbose_name=u'供應商識別名稱', default=u'')

    freight_type_object = Fields.CategoryProperty(verbose_name=u'寄送方式', kind=FreightTypeModel)
    freight_type = Fields.HiddenProperty(verbose_name=u'寄送方式', default=u'')
    freight_status_object = Fields.CategoryProperty(verbose_name=u'寄送狀態', kind=FreightStatusModel)
    freight_status = Fields.HiddenProperty(verbose_name=u'寄送狀態', default=u'')
    freight_status_title = Fields.HiddenProperty(verbose_name=u'寄送狀態')

    purchaser_name = Fields.StringProperty(verbose_name=u'購買人姓名', default=u'')
    purchaser_email = Fields.StringProperty(verbose_name=u'購買人 E-Mail', default=u'')
    purchaser_telephone = Fields.StringProperty(verbose_name=u'購買人電話', default=u'')
    purchaser_mobile = Fields.StringProperty(verbose_name=u'購買人手機', default=u'')
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
    sku_link = Fields.SidePanelProperty(verbose_name=u'訂購項目', text=u'點擊此處查看 訂購項目', auto_open=True,
                                        uri='admin:order:order_item:list_for_side_panel')

    total_size = Fields.FloatProperty(verbose_name=u'尺寸合計(公分)', default=0.0)
    total_volume = Fields.FloatProperty(verbose_name=u'體積合計(立方公分)', default=0.0)
    total_price = Fields.FloatProperty(verbose_name=u'金額合計', default=0.0)
    total_weight = Fields.FloatProperty(verbose_name=u'重量總重(公斤)', default=0.0)
    total_volumetric_weight = Fields.FloatProperty(verbose_name=u'材積總重', default=0.0)

    is_closed = Fields.BooleanProperty(verbose_name=u'是否已完成', default=False)
    is_cancel = Fields.BooleanProperty(verbose_name=u'是否已取消', default=False)
    is_report = Fields.BooleanProperty(verbose_name=u'是否已計入報表', default=False)

    order_close_datetime = Fields.DateTimeProperty(verbose_name=u'訂單完成時間', auto_now_add=True)
    order_cancel_datetime = Fields.DateTimeProperty(verbose_name=u'訂單取消時間', auto_now_add=True)
    order_report_datetime = Fields.DateTimeProperty(verbose_name=u'計入報表時間', auto_now_add=True)

    payment_type_object = Fields.CategoryProperty(verbose_name=u'付款方式', kind=PaymentTypeModel, tab_page=1)
    payment_type = Fields.HiddenProperty(verbose_name=u'付款方式')
    payment_status_object = Fields.CategoryProperty(verbose_name=u'付款狀態', kind=PaymentStatusModel, tab_page=1)
    payment_status = Fields.HiddenProperty(verbose_name=u'付款狀態')
    payment_status_title = Fields.HiddenProperty(verbose_name=u'付款狀態')

    subtotal_amount = Fields.FloatProperty(verbose_name=u'小計金額', tab_page=1, default=0.0)
    freight_amount = Fields.FloatProperty(verbose_name=u'運費', tab_page=1, default=0.0)
    total_amount = Fields.FloatProperty(verbose_name=u'總金額', tab_page=1, default=0.0)
    total_discount_amount = Fields.FloatProperty(verbose_name=u'折扣', tab_page=1, default=0.0)
    need_pay_amount = Fields.FloatProperty(verbose_name=u'應付金額', tab_page=1, default=0.0)

    currency_name = Fields.StringProperty(verbose_name=u'使用貨幣', tab_page=1)
    currency_title = Fields.StringProperty(verbose_name=u'貨幣名稱', tab_page=1)
    currency_exchange_rate = Fields.FloatProperty(verbose_name=u'當時匯率', tab_page=1, default=1.0)

    currency_subtotal_amount = Fields.FloatProperty(verbose_name=u'小計金額(貨幣)', tab_page=1, default=0.0)
    currency_freight_amount = Fields.FloatProperty(verbose_name=u'運費(貨幣)', tab_page=1, default=0.0)
    currency_total_amount = Fields.FloatProperty(verbose_name=u'總金額(貨幣)', tab_page=1, default=0.0)
    currency_total_discount_amount = Fields.FloatProperty(verbose_name=u'使用的購物金(貨幣)', tab_page=1, default=0.0)
    currency_need_pay_amount = Fields.FloatProperty(verbose_name=u'應付金額(貨幣)', tab_page=1, default=0.0)

    message = Fields.TextProperty(verbose_name=u'訂單留言', default=u'', tab_page=2)
    remark_backend = Fields.TextProperty(verbose_name=u'後台備註', default=u'', tab_page=2)
    remark_amount = Fields.TextProperty(verbose_name=u'對帳備註', default=u'', tab_page=2)
    remark_freight = Fields.TextProperty(verbose_name=u'寄送備註', default=u'', tab_page=2)
    remark_email = Fields.TextProperty(verbose_name=u'郵件備註', default=u'', tab_page=2)

    is_invoice_created = Fields.BooleanProperty(verbose_name=u'發票是否已開立', default=False, tab_page=99)
    invoice = Fields.StringProperty(verbose_name=u'發票號碼', tab_page=99)
    invoice_type = Fields.StringProperty(verbose_name=u'發票類型', tab_page=99, default=u'electronic', choices=[
        'electronic',
        'donate',
        'paper',
        'company',
    ], choices_text={
        'electronic': u'電子發票',
        'donate': u'捐贈發票',
        'paper': u'索取紙本',
        'company': u'公司行號',
    })
    invoice_vehicle = Fields.StringProperty(verbose_name=u'載具類型', tab_page=99, default=u'member', choices=[
        'member',
        'mobile',
        'moica',
    ], choices_text={
        'member': u'會員載具',
        'mobile': u'手機條碼',
        'moica': u'自然人憑証',
    })
    invoice_donate = Fields.StringProperty(verbose_name=u'捐贈對象', tab_page=99)
    invoice_mobile = Fields.StringProperty(verbose_name=u'手機條碼', tab_page=99)
    invoice_moica = Fields.StringProperty(verbose_name=u'自然人憑証', tab_page=99)
    invoice_address = Fields.StringProperty(verbose_name=u'寄送地址', tab_page=99)
    invoice_company_title = Fields.StringProperty(verbose_name=u'公司枱頭', tab_page=99)
    invoice_company_number = Fields.StringProperty(verbose_name=u'統一編號', tab_page=99)

    cost_for_items = Fields.FloatProperty(verbose_name=u'成本(項目)', default=0.0, tab_page=99)
    cost_for_freight = Fields.FloatProperty(verbose_name=u'成本(運費)', default=0.0, tab_page=99)
    cost_for_other = Fields.FloatProperty(verbose_name=u'成本(其它)', default=0.0, tab_page=99)
    cost = Fields.FloatProperty(verbose_name=u'成本', default=0.0, tab_page=99)
    profit = Fields.FloatProperty(verbose_name=u'利潤', default=0.0, tab_page=99)
    cost_remark = Fields.TextProperty(verbose_name=u'成本備註', default=u'', tab_page=99)

    expansion_filed_1 = Fields.HiddenProperty(verbose_name=u'擴充欄位 1', default=u'')
    expansion_filed_2 = Fields.HiddenProperty(verbose_name=u'擴充欄位 2', default=u'')
    expansion_filed_3 = Fields.HiddenProperty(verbose_name=u'擴充欄位 3', default=u'')
    expansion_filed_4 = Fields.HiddenProperty(verbose_name=u'擴充欄位 4', default=u'')
    expansion_filed_5 = Fields.HiddenProperty(verbose_name=u'擴充欄位 5', default=u'')

    @property
    def items(self):
        from order_item_model import OrderItemModel
        return OrderItemModel.all_with_order(self)

    @property
    def discount_items(self):
        from order_discount_model import OrderDiscountModel
        return OrderDiscountModel.all_with_order(self)

    def before_put(self):
        from datetime import datetime
        if self.order_close_datetime is None:
            self.order_close_datetime = datetime.now()
        if self.order_cancel_datetime is None:
            self.order_cancel_datetime = datetime.now()
        if self.order_report_datetime is None:
            self.order_report_datetime = datetime.now()
        self.set_payment_status()
        self.set_freight_status()
        self.set_order_status()
        super(OrderModel, self).before_put()

    @classmethod
    def before_delete(cls, key):
        try:
            from ..models.order_item_model import OrderItemModel
            items = OrderItemModel.all_with_order(key)
            keys = []
            for item in items:
                keys.append(item.key)
            ndb.delete_multi(keys)
        except:
            pass

    @classmethod
    def all(cls, user=None, *args, **kwargs):
        cls._fix_up_kind_map()
        if user is None:
            return cls.query().order(-cls.sort)
        return cls.query(cls.user==user.key).order(-cls.sort)

    @classmethod
    def all_with_supplier(cls, supplier, d1, d2, *args, **kwargs):
        return cls.query(cls.supplier==supplier.key, cls.created >= d1, cls.created <= d2).order(-cls.created)

    @classmethod
    def all_with_status(cls, status=None, *args, **kwargs):
        if status is None:
            return cls.query().order(-cls.sort)
        s = OrderStatusModel.get_by_name(status)
        return cls.query(cls.status_object==s.key).order(-cls.sort)

    def calc_amount(self, subtotal_amount, freight_amount=None, total_discount_amount=None, subtotal_cost=None):
        if freight_amount is None:
            freight_amount = self.freight_amount
        if total_discount_amount is None:
            total_discount_amount = self.total_discount_amount
        if subtotal_cost is None:
            subtotal_cost = self.cost_for_items
        self.subtotal_amount = subtotal_amount
        self.total_amount = subtotal_amount + freight_amount
        self.need_pay_amount = float(self.total_amount) - float(total_discount_amount)
        self.cost_for_freight = freight_amount
        self.cost = subtotal_cost + self.cost_for_freight + self.cost_for_other
        self.profit = subtotal_amount - self.cost
        if self.profit < 0:
            self.profit = 0

        if self.total_discount_amount >= self.total_amount:
            self.total_discount_amount = self.total_amount
            self.need_pay_amount = 0

    def set_freight_type(self, status):
        if isinstance(status, basestring):
            status = FreightTypeModel.get_by_name(status)
        self.freight_type_object = status.key
        self.freight_type = status.name

    def set_freight_status(self, status=None):
        if isinstance(status, basestring):
            status = FreightStatusModel.get_by_name(status)
        if status is None and self.freight_status_object is not None:
            status = self.freight_status_object.get()
        if status is not None:
            self.freight_status_object = status.key
            self.freight_status = status.name
            self.freight_status_title = status.title

    def set_order_status(self, status=None):
        if isinstance(status, basestring):
            status = OrderStatusModel.get_by_name(status)
        if status is None and self.status_object is not None:
            status = self.status_object.get()
        if status is not None:
            self.status_object = status.key
            self.status = status.name
            self.status_title = status.title

    def set_currency(self, currency):
        if currency:
            self.currency_name = currency.name
            self.currency_title = currency.title
            self.currency_exchange_rate = currency.exchange_rate
            self.calc_currency_amount()
        else:
            self.currency_name = 'main'
            self.currency_title = u'基準貨幣'
            self.currency_exchange_rate = 1.0

    def calc_currency_amount(self, params=None):
        if params is not None:
            self.currency_subtotal_amount = params.get_float('currency_subtotal_amount')
            self.currency_freight_amount = params.get_float('currency_freight_amount')
        else:
            try:
                from plugins.currency.models.currency_model import exchange
                self.currency_subtotal_amount = exchange(self.currency_exchange_rate, self.subtotal_amount)
                self.currency_freight_amount = exchange(self.currency_exchange_rate, self.freight_amount)
            except:
                return
        self.currency_total_amount = self.currency_subtotal_amount + self.currency_freight_amount
        self.currency_need_pay_amount = self.currency_total_amount - self.currency_total_discount_amount
        # TODO 計算折扣的貨幣金額

    def set_shop_point(self, session):
        self.total_discount_amount = 0.0
        self.currency_total_discount_amount = 0.0
        if 'shop_point_use' in session:
            self.total_discount_amount = session['shop_point_use']
        if 'shop_point_use_in_currency' in session:
            self.currency_total_discount_amount = session['shop_point_use_in_currency']

    def add_discount(self, title, amount):
        from .order_discount_model import OrderDiscountModel
        d = OrderDiscountModel()
        d.order = self.key
        d.title = title
        d.amount = amount
        d.put()

    def calc_size_weight_price_and_put(self, items=None):
        if items is None:
            items = self.items
        total_volume = 0.0
        total_size = 0.0
        total_price = 0.0
        total_weight = 0.0
        total_volumetric_weight = 0.0
        total_cost_for_items = 0.0
        for cart_item in items:
            total_size += cart_item.quantity * (cart_item.size_1 + cart_item.size_2 + cart_item.size_3)
            total_volume += cart_item.quantity * cart_item.size_1 * cart_item.size_2 * cart_item.size_3
            total_price += cart_item.quantity * cart_item.price
            total_weight += cart_item.quantity * cart_item.weight
            total_volumetric_weight += cart_item.quantity * cart_item.volumetric_weight()
            total_cost_for_items += cart_item.quantity * cart_item.cost
        self.total_volume = total_volume
        self.total_size = total_size
        self.total_price = total_price
        self.total_weight = total_weight
        self.total_volumetric_weight = total_volumetric_weight
        self.cost_for_items = total_cost_for_items
        self.put()

    def close_order(self):
        from config_model import ConfigModel
        from datetime import datetime, timedelta
        config = ConfigModel.get_config()
        self.order_close_datetime = datetime.now()
        if config.debug_mode:
            self.order_close_datetime = datetime.now() + timedelta(days=-30)
        self.is_closed = True
        self.set_order_status('closed')

    def cancel_order(self):
        from config_model import ConfigModel
        from datetime import datetime, timedelta
        config = ConfigModel.get_config()
        self.order_cancel_datetime = datetime.now()
        if config.debug_mode:
            self.order_cancel_datetime = datetime.now() + timedelta(days=-30)
        self.is_cancel = True
        self.set_order_status('order_cancel')


