#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.
from datetime import datetime
from argeweb import Controller, scaffold, route_with, route
from argeweb import auth, add_authorizations
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from plugins.user_shop_point.models.user_shop_point_model import UserShopPointModel
from ..models.order_item_model import OrderModel


class Form(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        default_view = 'json'
        Model = OrderModel

    class Scaffold:
        display_in_form = ['user_name', 'account', 'is_enable', 'sort', 'created', 'modified']

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
        # 貨幣
        currency = None
        try:
            from plugins.currency.models.currency_model import CurrencyModel
            currency = CurrencyModel.get_current_or_main_currency_with_controller(self)
        except:
            pass
        order, items = OrderModel.process_new_order(self.application_user, self.params, self.session, currency)

        items_for_mail = []
        for item in items:
            items_for_mail.append(u"%s %s 數量: %s" % (item.product_name, item.spec_full_name, item.quantity))

        if order.shopping_cash > 0:
            self.session['shop_point_use'] = 0
            user_point_item = UserShopPointModel.get_or_create(self.application_user)
            user_point_item.decrease_point(
                order.shopping_cash, u'[系統] 由訂單 %s 扣除' % order.order_no,
                order.order_no, order.total_amount)
            user_point_item.put()
        data_for_mail = {
            'site_name': self.host_information.site_name,
            'name': self.application_user.name,
            'email': self.application_user.email,
            'created': self.util.localize_time(datetime.now()),
            'domain': self.host_information.host,
            'order_items': u"<br>".join(items_for_mail)
        }
        for p in order._properties:
            data_for_mail[p] = getattr(order, p)

        self.fire(
            event_name='send_mail_width_template',
            template_name='order_create_send_to_user',
            send_to=self.application_user.email,
            data=data_for_mail
        )
        self.fire(
            event_name='send_mail_width_template',
            template_name='order_create_send_to_admin',
            send_to=None,
            data=data_for_mail
        )

        self.context['data'] = {'result': 'success', 'order': self.util.encode_key(order)}
        self.context['message'] = u'已成功加入。'

    @route
    @add_authorizations(auth.check_user)
    def gen_payment_information(self):
        order = self.params.get_ndb_record('order_id')
        if order is None:
            return 'error order not exist'
        payment_type = order.payment_type_object.get()
        if payment_type is None:
            return 'error payment type not exist'
        if self.application_user is None:
            return 'error user not exist'
        payment_record = self.fire(
            event_name='create_payment',
            title=u'支付訂單 %s 使用 %s ' % (order.order_no, payment_type.title),
            detail=u'支付訂單 %s 使用 %s ' % (order.order_no, payment_type.title),
            amount=order.need_pay_amount,
            source=order,
            source_params={'order_no': order.order_no},
            source_callback_uri='form:order:after_pay',
            payment_type=payment_type,
            user=self.application_user,
            status='pending_payment',
        )
        return self.redirect(payment_record.pay_url)

    @route
    def after_pay(self):
        return self.json(self.params.get_ndb_record('payment_record'))