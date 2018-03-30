#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.
from datetime import datetime
from argeweb import Controller, scaffold, route_with, route, require_post
from argeweb import auth, add_authorizations
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from plugins.user_shop_point.models.user_shop_point_model import UserShopPointModel
from ..models.order_item_model import OrderModel


class Form(Controller):
    class Meta:
        default_view = 'json'
        Model = OrderModel

    class Scaffold:
        display_in_form = ['user_name', 'account', 'is_enable', 'sort', 'created', 'modified']

    def check(self):
        self.context['data'] = {'result': 'failure'}
        if self.application_user is None:
            self.context['message'] = u'請先登入。'
            return True

    @route
    @require_post
    @route_with(name='form:order:check_out_new')
    def check_out_new(self):
        if self.application_user is None:
            return self.json_failure_message(u'請先登入。')
        from plugins.shopping_cart.models.shopping_cart_model import ShoppingCartModel
        from ..models.order_item_model import OrderItemModel
        carts = ShoppingCartModel.find_by_properties(user=self.application_user.key).fetch()
        freight_type = self.params.get_ndb_record('freight_type')
        payment_type = self.params.get_ndb_record('payment_type')
        if freight_type is None or payment_type is None:
            return self.json_failure_message(u'請選擇付款方式與寄送方式。')
        freights = freight_type.items.fetch()
        order_link = u''
        order_list = []
        filed_name_list = [
            'purchaser_name', 'purchaser_email', 'purchaser_telephone', 'purchaser_mobile', 'recipient_name',
            'recipient_telephone', 'recipient_mobile', 'recipient_email', 'recipient_address_country',
            'recipient_address_city', 'recipient_address_district', 'recipient_address_zip', 'recipient_address_detail',
            'recipient_store_number', 'recipient_store_name', 'message', 'invoice_vehicle', 'invoice_type', 'invoice_donate',
            'invoice_mobile', 'invoice_moica', 'invoice_address', 'invoice_company_title', 'invoice_company_number'
        ]
        self.fire(
            event_name='before_order_checkout',
            user=self.application_user
        )
        self.logging.info(self.application_user.mobile)
        for cart in carts:
            items = cart.items
            # 清除空的購物車
            if len(items) == 0:
                cart.key.delete()
                continue

            # 建立訂單
            order = self.meta.Model()

            # 供應商處理
            order.supplier = cart.supplier
            if order.supplier:
                order.supplier_name = 'supplier_' + order.supplier.get().name

            # 使用者資料
            for filed_name in ['name', 'email']:
                field_value = getattr(self.application_user, filed_name)
                if field_value:
                    setattr(order, 'purchaser_' + filed_name, field_value)
            for filed_name in filed_name_list:
                field_value = self.params.get_string(filed_name, None)
                if field_value:
                    setattr(order, filed_name, field_value)
            # 產生 key
            order.put()

            order_link = order.name
            for cart_item in cart.items:
                if cart_item.can_add_to_order:
                    order_item = OrderItemModel.create_from_shopping_cart_item(cart_item, order)
                    cart_item.quantity_has_count = 0
                    cart_item.key.delete()
                    self.fire(
                        event_name='after_order_item_created',
                        order_item=order_item,
                        old_quantity=0,
                        new_quantity=cart_item.quantity
                    )
            self.fire(event_name='calc_freight_amount', target=cart, freight_data=freights)
            order.freight_amount = cart.freight_amount
            order.calc_size_weight_price_and_put()
            order.calc_amount(cart.total_price)
            order.user = self.application_user.key
            order.set_order_status('new_order')
            # 貨幣模組
            currency = None
            try:
                from plugins.currency.models.currency_model import CurrencyModel
                currency = CurrencyModel.get_current_or_main_currency_with_controller(self)
            except:
                pass
            order.set_currency(currency)
            # 付款
            order.set_payment_type(payment_type)
            order.set_payment_status('pending_payment')
            # 運送
            order.set_freight_type(freight_type)
            order.set_freight_status('unconfirmed')
            order_list.append(order)
            cart.key.delete()
        self.fire(
            event_name='after_order_checkout',
            order_list=order_list,
            user=self.application_user
        )
        for order in order_list:
            order.order_link = order_link
            order.put()
        self.context['data'] = {'result': 'success', 'order_link': order_link}
        self.context['message'] = u'完成'

    @route
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
                order.shopping_cash, u'由訂單 %s 扣除' % order.order_no,
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
    @route_with(name='form:order:cancel')
    def cancel_order(self):
        if self.application_user is None:
            return self.json_failure_message(u'請先登入。')
        str_order_name = self.params.get_list('order_list')
        for item in str_order_name:
            if item == u'':
                continue
            order = self.params.get_ndb_record(item)
            if order is None:
                continue
            status = order.status_object.get()
            if status.name == u'unconfirmed' or status.name == u'new_order':
                order.set_order_status(u'order_cancel')
                order.put()
        self.context['message'] = u'已成功取消。'
