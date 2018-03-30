#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import Controller, scaffold, route, route_menu


class OrderItem(Controller):
    class Scaffold:
        display_in_list = ['user', 'order_type', 'title', 'spec_full_name', 'price', 'quantity', 'created']

    def admin_add(self):
        scaffold.add(self)

    @route_menu(list_name=u'super_user', group=u'記錄查看', need_hr=True, text=u'訂單項目', sort=1333)
    def admin_list(self):
        return scaffold.list(self)

    @route
    def admin_list_for_side_panel(self, target=''):
        def query_factory_with_order(controller):
            m = self.meta.Model
            return m.all_with_order(order_record)

        if target == '--no-record--':
            self.context['no_record_data'] = True
            return

        order_record = self.params.get_ndb_record(target)
        self.scaffold.query_factory = query_factory_with_order
        self.context['order_record'] = order_record
        return scaffold.list(self)

    @route
    def admin_change_quantity(self):
        self.meta.change_view('json')
        order = self.params.get_ndb_record('order_key')
        data = []
        length = self.params.get_integer('length')
        # remake = self.params.get_string('remake')
        subtotal_amount = 0.0
        subtotal_cost = 0.0
        for index in xrange(0, length):
            item = self.params.get_ndb_record('order_item_key_%s' % str(index))
            quantity = self.params.get_integer('order_item_quantity_%s' % str(index))
            if item is None:
                continue
            if quantity <= 0:
                item.delete()
            else:
                self.fire(
                    event_name='order_item_change_quantity',
                    item=item,
                    quantity=quantity
                )
                item.put()
                subtotal_cost += item.quantity * item.cost
                data.append(item)
        order.calc_size_weight_price_and_put()
        # 貨幣模組
        currency = None
        try:
            from plugins.currency.models.currency_model import CurrencyModel
            currency = CurrencyModel.get_current_or_main_currency(order.currency_name)
        except:
            pass
        order.set_currency(currency)
        order.calc_amount(order.total_price)
        order.put()
        self.context['message'] = u'完成'
        self.context['data'] = {'result': 'success', 'items': data}

    @route
    def admin_insert_with_spec(self):
        self.meta.change_view('json')
        order = self.params.get_ndb_record('order_key')
        spec = self.params.get_ndb_record('spec_key')
        quantity = self.params.get_integer('quantity')
        order_type = self.params.get_integer('order_type')
        try:
            user = order.user.get()
        except:
            return self.json_failure_message(u'訂單缺少了訂購者，請先設置該欄位')
        item = self.meta.Model.get_or_create(user, spec, order, order_type)
        # TODO 應該回傳  fire 事件的結果
        self.fire(
            event_name='order_item_change_quantity',
            item=item,
            quantity=quantity
        )
        item.put()
        order.calc_size_weight_price_and_put()
        # 貨幣模組
        currency = None
        try:
            from plugins.currency.models.currency_model import CurrencyModel
            currency = CurrencyModel.get_current_or_main_currency(order.currency_name)
        except:
            pass
        order.set_currency(currency)
        order.calc_amount(order.total_price)
        order.put()
        self.json_success_message(u'完成')


    @route
    def admin_insert_with_sku(self):
        self.meta.change_view('json')
        order = self.params.get_ndb_record('order_key')
        sku = self.params.get_ndb_record('sku_key')
        quantity = self.params.get_integer('quantity')
        order_type = self.params.get_integer('order_type')
        try:
            user = order.user.get()
        except:
            self.context['message'] = u'訂單缺少了訂購者，請先設置該欄位'
            self.context['data'] = {'result': 'failure'}
            return
        try:
            item = self.meta.Model.get_or_create(user, sku, order, quantity, order_type)
        except:
            self.context['message'] = u'請先選擇產品及規格'
            self.context['data'] = {'result': 'failure'}
            return
        self.context['message'] = u'完成'
        result = 'success'
        if order_type == 0:
            if item._product.can_order is False:
                result = 'failure'
                self.context['message'] = u'此項目無法進行訂購'
            q = item.get_can_order_quantity
            if q < quantity:
                result = 'failure'
                self.context['message'] = u'數量不足，可訂購數量為 %s' % q
        if order_type == 1:
            if item._product.can_pre_order is False:
                result = 'failure'
                self.context['message'] = u'此項目無法進行預購'
                item.delete()
        self.context['data'] = {'result': result, 'item': item}
