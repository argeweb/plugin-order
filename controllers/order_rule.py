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


class OrderRule(Controller):
    # @route_menu(list_name=u'backend', text=u'規則', sort=1324, group=u'產品銷售')
    def admin_list(self):
        return scaffold.list(self)