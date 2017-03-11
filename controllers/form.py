#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.
from random import randint
from datetime import datetime
from argeweb import Controller, scaffold, route_menu, route_with, route, settings
from argeweb import auth, add_authorizations
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from ..models.order_item_model import OrderModel, OrderItemModel
from ..models.payment_type_model import PaymentTypeModel
from ..models.freight_type_model import FreightTypeModel
from ..models.freight_model import FreightModel
from plugins.user_shop_point.models.user_shop_point_model import UserShopPointModel
from plugins.mail import Mail
from plugins.shopping_cart.models.shopping_cart_item_model import ShoppingCartItemModel
from plugins.user_contact_data.models.user_contact_data_model import UserContactDataModel


class Form(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        pagination_actions = ('list',)
        pagination_limit = 50
        default_view = 'json'
        Model = OrderModel

    class Scaffold:
        display_in_form = ('user_name', 'account', 'is_enable', 'sort', 'created', 'modified')

    def check(self, allow_get=False):
        self.context['data'] = {'result': 'failure'}
        if allow_get is False and self.request.method != 'POST':
            return self.abort(404)
        if self.application_user is None:
            self.context['message'] = u'請先登入。'
            return True

    @route
    @add_authorizations(auth.check_user)
    @route_with(name='form:order:check_out')
    def check_out(self):
        if self.check():
            return
        order = OrderModel()
        order.user = self.application_user.key
        order.purchaser_name = self.application_user.name
        order.purchaser_email = self.application_user.email
        order.recipient_name = self.params.get_string('name')
        order.recipient_telephone = self.params.get_string('telephone')
        order.recipient_mobile = self.params.get_string('mobile')
        order.recipient_email = self.params.get_string('email')
        order.recipient_address_country = self.params.get_string('address_country')
        order.recipient_address_city = self.params.get_string('address_city')
        order.recipient_address_district = self.params.get_string('address_district')
        order.recipient_address_zip = self.params.get_string('address_zip')
        order.recipient_address_detail = self.params.get_string('address_detail')
        order.recipient_store_number = self.params.get_string('store_number')
        order.recipient_store_name = self.params.get_string('store_name')
        order.message = self.params.get_string('message')

        payment_type = self.params.get_ndb_record('payment_type')
        order.payment_type = payment_type.key
        order.payment_type_title = payment_type.title
        freight_type = self.params.get_ndb_record('freight_type')
        order.freight_type = freight_type.key
        order.freight_type_title = freight_type.title

        order.subtotal_amount = self.params.get_float('subtotal_amount')
        order.freight_amount = self.params.get_float('freight_amount')
        order.shopping_cash = self.params.get_float('shopping_cash')
        order.need_pay_amount = self.params.get_float('total_amount')
        order.total_amount = order.subtotal_amount + order.freight_amount
        if order.shopping_cash > order.total_amount:
            order.shopping_cash = order.total_amount
            order.need_pay_amount = 0

        order.status = 1
        order.payment_status = 0
        order.freight_status = 0
        if order.shopping_cash > 0:
            if order.need_pay_amount == 0:
                order.payment_status = 5
            else:
                order.payment_status = 6
        order.put()

        if order.shopping_cash > 0:
            self.session['shop_point_use'] = 0
            user_point_item = UserShopPointModel.get_or_create(self.application_user)
            user_point_item.decrease_point(
                order.shopping_cash, u'[系統] 由訂單 %s 扣除' % order.order_no,
                order.order_no, order.total_amount)
            user_point_item.put()

        items = []
        for item in ShoppingCartItemModel.all_with_user(self.application_user).fetch():
            if item.can_add_to_order == True:
                order_item = OrderItemModel.create_from_shopping_cart_item(item)
                order_item.order = order.key
                order_item.put()
                item.quantity_has_count = 0
                item.key.delete()
                items.append(u"%s %s 數量: %s" % (order_item.product_name, order_item.spec_full_name, order_item.quantity))
        mail = Mail(self)
        data_for_mail = {
            'site_name': self.host_information.site_name,
            'name': self.application_user.name,
            'email': self.application_user.email,
            'created': self.util.localize_time(datetime.now()),
            'domain': self.host_information.host,
            'order_items': u"<br>".join(items)
        }
        for p in order._properties:
            data_for_mail[p] = getattr(order, p)
        r = mail.send_width_template('order_create_send_to_user', self.application_user.email, data_for_mail)
        r = mail.send_width_template('order_create_send_to_admin', None, data_for_mail)
        self.context['data'] = {'result': 'success', 'order': self.util.encode_key(order)}
        self.context['message'] = u'已成功加入。'