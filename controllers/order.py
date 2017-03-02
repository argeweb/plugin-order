#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.


from argeweb import Controller, scaffold, route_menu, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search


class Order(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_actions = ('list',)
        pagination_limit = 50

    class Scaffold:
        # display_in_list = ('title_lang_zhtw', 'name')
        pass

    @route
    @route_menu(list_name=u'backend', text=u'新訂單', sort=1301, group=u'銷售管理', parameter=u'status=1')
    @route_menu(list_name=u'backend', text=u'已付款', sort=1302, group=u'銷售管理', parameter=u'status=2')
    @route_menu(list_name=u'backend', text=u'備貨中', sort=1303, group=u'銷售管理', parameter=u'status=3')
    @route_menu(list_name=u'backend', text=u'已出貨', sort=1304, group=u'銷售管理', parameter=u'status=4')
    @route_menu(list_name=u'backend', text=u'已結單', sort=1305, group=u'銷售管理', parameter=u'status=5')
    @route_menu(list_name=u'backend', text=u'異常流程', sort=1306, group=u'銷售管理', parameter=u'status=6')
    def admin_list(self):
        def query_factory_with_status(controller):
            return controller.meta.Model.all_with_status(controller.status)

        setattr(self, 'status', self.params.get_integer('status', 1))
        self.scaffold.query_factory = query_factory_with_status
        return scaffold.list(self)
