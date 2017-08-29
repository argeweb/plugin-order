#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.


from argeweb import Controller, scaffold, route_menu


class FreightType(Controller):
    @route_menu(list_name=u'backend', group=u'產品管理', text=u'寄送方式', sort=1322)
    def admin_list(self):
        return scaffold.list(self)