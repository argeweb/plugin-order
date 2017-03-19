#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import Controller, scaffold, route_menu, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search


class OrderItem(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_actions = ('list',)
        pagination_limit = 50

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
        if target == '--no-record--':
            self.context['no_record_data'] = True
            return
        order_record = self.util.decode_key(target).get()

        def query_factory_only_codefile(controller):
            m = self.meta.Model
            return m.all_with_order(order_record)

        self.scaffold.query_factory = query_factory_only_codefile
        self.context['order_record'] = order_record
        return scaffold.list(self)
