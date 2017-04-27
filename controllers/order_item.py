#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import Controller, scaffold, route_menu, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search
from plugins.product_stock.models.warehouse_model import WarehouseModel


class OrderItem(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)

    class Scaffold:
        display_in_list = ('user', 'order_type', 'title', 'spec_full_name', 'price', 'quantity', 'created')

    def on_scaffold_before_apply(self, controller, container, item):
        item.change_quantity(item.quantity)

    def admin_add(self):
        self.events.scaffold_before_apply += self.on_scaffold_before_apply
        scaffold.add(self)

    def admin_list(self):
        return scaffold.list(self)

    @route
    def admin_list_for_side_panel(self, target=''):
        def query_factory_only_codefile(controller):
            m = self.meta.Model
            return m.all_with_order(order_record)

        if target == '--no-record--':
            self.context['no_record_data'] = True
            return

        order_record = self.params.get_ndb_record(target)
        self.scaffold.query_factory = query_factory_only_codefile
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
            r = self.params.get_ndb_record('order_item_key_%s' % str(index))
            q = self.params.get_integer('order_item_quantity_%s' % str(index))
            if r is None:
                continue
            if q <= 0:
                r.delete()
            else:
                r.change_quantity(q)
                r.put()
                subtotal_amount += r.quantity * r.price
                subtotal_cost += r.quantity * r.cost
                data.append(r)
        order.calc_total_amount(subtotal_amount)
        order.calc_total_cost(subtotal_cost)
        order.calc_currency_amount()
        order.put()
        self.context['message'] = u'完成'
        self.context['data'] = {'result': 'success', 'items': data}

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
            if item.quantity != quantity:
                result = 'failure'
                self.context['message'] = u'數量不足，可訂購數量為 %s' % item.get_can_order_quantity()
        if order_type == 1:
            if item._product.can_pre_order is False:
                result = 'failure'
                self.context['message'] = u'此項目無法進行預購'
                item.delete()
        self.context['data'] = {'result': result, 'item': item}
