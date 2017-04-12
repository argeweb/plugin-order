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
    class Meta:
        tab_pages = [u'物流', u'金流', u'備註', u'成本']

    name = Fields.StringProperty(verbose_name=u'識別名稱')

    status_object = Fields.CategoryProperty(verbose_name=u'訂單狀態', kind=OrderStatusModel)
    status = Fields.SearchingHelperProperty(verbose_name=u'訂單狀態', target='status_object', target_field_name='title')
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

    freight_type_object = Fields.CategoryProperty(verbose_name=u'寄送方式', kind=FreightTypeModel)
    freight_type = Fields.SearchingHelperProperty(verbose_name=u'寄送方式', target='freight_type_object', target_field_name='title')
    freight_status_object = Fields.CategoryProperty(verbose_name=u'寄送狀態', kind=FreightStatusModel)
    freight_status = Fields.SearchingHelperProperty(verbose_name=u'寄送狀態', target='freight_status_object', target_field_name='title')

    payment_type_object = Fields.CategoryProperty(verbose_name=u'付款方式', kind=PaymentTypeModel, tab_page=1)
    payment_type = Fields.SearchingHelperProperty(verbose_name=u'付款方式', target='payment_type_object', target_field_name='title', tab_page=1)
    payment_status_object = Fields.CategoryProperty(verbose_name=u'付款狀態', kind=PaymentStatusModel, tab_page=1)
    payment_status = Fields.SearchingHelperProperty(verbose_name=u'付款狀態', target='payment_status_object', target_field_name='title', tab_page=1)

    subtotal_amount = Fields.FloatProperty(verbose_name=u'小計金額', tab_page=1)
    freight_amount = Fields.FloatProperty(verbose_name=u'運費', tab_page=1)
    total_amount = Fields.FloatProperty(verbose_name=u'總金額', tab_page=1)
    shopping_cash = Fields.FloatProperty(verbose_name=u'使用的購物金', tab_page=1)
    need_pay_amount = Fields.FloatProperty(verbose_name=u'應付金額', tab_page=1)

    currency_name = Fields.StringProperty(verbose_name=u'使用貨幣', tab_page=1)
    currency_title = Fields.StringProperty(verbose_name=u'貨幣名稱', tab_page=1)
    currency_exchange_rate = Fields.FloatProperty(verbose_name=u'當時匯率', tab_page=1)

    currency_subtotal_amount = Fields.FloatProperty(verbose_name=u'小計金額(貨幣)', tab_page=1)
    currency_freight_amount = Fields.FloatProperty(verbose_name=u'運費(貨幣)', tab_page=1)
    currency_total_amount = Fields.FloatProperty(verbose_name=u'總金額(貨幣)', tab_page=1)
    currency_shopping_cash = Fields.FloatProperty(verbose_name=u'使用的購物金(貨幣)', tab_page=1)
    currency_need_pay_amount = Fields.FloatProperty(verbose_name=u'應付金額(貨幣)', tab_page=1)

    cost_for_items = Fields.FloatProperty(verbose_name=u'成本(項目)', default=0.0, tab_page=3)
    cost_for_freight = Fields.FloatProperty(verbose_name=u'成本(運費)', default=0.0, tab_page=3)
    cost_for_other = Fields.FloatProperty(verbose_name=u'成本(其它)', default=0.0, tab_page=3)
    cost = Fields.FloatProperty(verbose_name=u'成本', default=0.0, tab_page=3)
    profit = Fields.FloatProperty(verbose_name=u'利潤', default=0.0, tab_page=3)
    cost_remark = Fields.TextProperty(verbose_name=u'成本備註', tab_page=3)

    message = Fields.TextProperty(verbose_name=u'訂單留言', tab_page=2)
    remark_backend = Fields.TextProperty(verbose_name=u'後台備註', tab_page=2)
    remark_amount = Fields.TextProperty(verbose_name=u'對帳備註', tab_page=2)
    remark_freight = Fields.TextProperty(verbose_name=u'寄送備註', tab_page=2)
    remark_email = Fields.TextProperty(verbose_name=u'郵件備註', tab_page=2)

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
        return cls.query(cls.status_object==s.key).order(-cls.sort)

    @classmethod
    def process_new_order(cls, application_user, params, session, currency, *args, **kwargs):
        order = OrderModel()
        # 訂單資料
        order.set_user_data(application_user, params)
        order.set_user_contact_data(params)
        order.set_shop_point(session)
        # 貨幣
        order.set_currency(currency)
        order.calc_currency_amount(params)
        # 付款
        payment_type_object = params.get_ndb_record('payment_type')
        order.payment_type_object = payment_type_object.key
        # 運送
        freight_type_object = params.get_ndb_record('freight_type')
        order.freight_type_object = freight_type_object.key
        order.put()

        # 訂購項目
        items = []
        subtotal_amount = 0.0
        subtotal_cost = 0.0
        from plugins.shopping_cart.models.shopping_cart_item_model import ShoppingCartItemModel
        from ..models.order_item_model import OrderItemModel
        for item in ShoppingCartItemModel.all_with_user(application_user).fetch():
            if item.can_add_to_order:
                order_item = OrderItemModel.create_from_shopping_cart_item(item, order)
                items.append(order_item)
                subtotal_amount += order_item.quantity * order_item.price
                subtotal_cost += order_item.quantity * order_item.cost
                item.quantity_has_count = 0
                item.key.delete()

        # 金額計算
        order.set_freight_amount(subtotal_amount)
        order.calc_total_amount(subtotal_amount)
        order.calc_total_cost(subtotal_cost)

        order_status = 'new_order'
        freight_status = 'unconfirmed'
        payment_status = 'unconfirmed'
        if order.shopping_cash > 0:
            if order.need_pay_amount == 0:
                order_status = 'already_paid'
                payment_status = 'full_payment_with_point'
            else:
                payment_status = 'part_payment_with_point'

        order.set_order_status(order_status)
        order.set_freight_status(freight_status)
        order.set_payment_status(payment_status)
        order.put()
        return order, items

    def gen_order_no(self):
        from argeweb.core.time_util import localize
        from datetime import datetime
        n = localize(datetime.today()).strftime('%Y%m%d %H%M%S').split(' ')
        return '%s-%s-%s' % (n[0], self.name[0:4], n[1])

    def calc_total_cost(self, subtotal_cost):
        self.cost_for_items = subtotal_cost
        self.cost = self.cost_for_items + self.cost_for_freight + self.cost_for_other
        self.profit = self.total_amount - self.cost

    def calc_total_amount(self, subtotal_amount):
        self.subtotal_amount = subtotal_amount
        self.total_amount = subtotal_amount + self.freight_amount
        self.need_pay_amount = float(self.total_amount) - float(self.shopping_cash)

        if self.shopping_cash >= self.total_amount:
            self.shopping_cash = self.total_amount
            self.need_pay_amount = 0

    def set_order_status(self, name):
        self.status_object = OrderStatusModel.find_by_name(name).key

    def set_freight_status(self, name):
        self.freight_status_object = FreightStatusModel.find_by_name(name).key

    def set_payment_status(self, name):
        self.payment_status_object = PaymentStatusModel.find_by_name(name).key

    def set_freight_amount(self, subtotal_amount):
        from ..models.freight_model import FreightModel, FreightTypeModel
        is_find = False
        amount = 0.0
        for item in FreightModel.query(FreightModel.freight_type == self.freight_type_object).fetch():
            if item.start_amount <= subtotal_amount < item.end_amount and is_find is False:
                is_find = True
                amount = item.freight_amount
        self.freight_amount = amount
        return amount

    def set_user_data(self, application_user, params):
        if application_user:
            self.user = application_user.key
            self.purchaser_name = application_user.name
            self.purchaser_email = application_user.email
        else:
            self.user = None
            self.purchaser_name = params.get_string('purchaser_name')
            self.purchaser_email = params.get_string('purchaser_email')

    def set_user_contact_data(self, params):
        self.recipient_name = params.get_string('name')
        self.recipient_telephone = params.get_string('telephone')
        self.recipient_mobile = params.get_string('mobile')
        self.recipient_email = params.get_string('email')
        self.recipient_address_country = params.get_string('address_country')
        self.recipient_address_city = params.get_string('address_city')
        self.recipient_address_district = params.get_string('address_district')
        self.recipient_address_zip = params.get_string('address_zip')
        self.recipient_address_detail = params.get_string('address_detail')
        self.recipient_store_number = params.get_string('store_number')
        self.recipient_store_name = params.get_string('store_name')
        self.message = params.get_string('message')

    def set_currency(self, currency):
        if currency:
            self.currency_name = currency.name
            self.currency_title = currency.title
            self.currency_exchange_rate = currency.exchange_rate
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
        self.currency_need_pay_amount = self.currency_total_amount - self.currency_shopping_cash

    def set_shop_point(self, session):
        self.shopping_cash = 0.0
        self.currency_shopping_cash = 0.0
        if 'shop_point_use' in session:
            self.shopping_cash = session['shop_point_use']
        if 'shop_point_use_in_currency' in session:
            self.currency_shopping_cash = session['shop_point_use_in_currency']

    def before_put(self):
        super(OrderModel, self).before_put()
        if self.order_no is u'':
            self.order_no = self.gen_order_no()

    @classmethod
    def before_delete(cls, key):
        try:
            from ..models.order_item_model import OrderItemModel
            items = OrderItemModel.all_with_order(key)
            for item in items:
                item.order_be_delete = True
                item.put()
        except:
            pass
