#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.


from argeweb import Controller, scaffold, route_menu


class FreightStatus(Controller):
    @route_menu(list_name=u'system', group=u'訂單管理', text=u'寄送狀態', sort=881)
    def admin_list(self):
        return scaffold.list(self)