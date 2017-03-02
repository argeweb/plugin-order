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
        order.total_amount = order.need_pay_amount + order.shopping_cash
        order.status = 1
        order.payment_status = 0
        order.freight_status = 0
        if order.shopping_cash > 0:
            if order.need_pay_amount == 0:
                order.payment_status = 5
            else:
                order.payment_status = 6
        order.put()
        self.context['data'] = {'result': 'success', 'order': self.util.encode_key(order)}
        self.context['message'] = u'已成功加入。'