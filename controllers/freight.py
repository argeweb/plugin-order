#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import Controller, scaffold, route_menu


class Freight(Controller):
    class Scaffold:
        display_in_list = ['freight_type', 'supplier', 'start_value', 'end_value', 'freight_amount', 'is_enable']

    @route_menu(list_name=u'backend', group=u'產品管理', text=u'運費', sort=1123)
    def admin_list(self):
        return scaffold.list(self)

    def before_scaffold(self):
        from ..models.config_model import ConfigModel
        super(Freight, self).before_scaffold()
        config = ConfigModel.get_config()
        self.scaffold.change_field_visibility('check_target', config.show_freight_check_target)
        self.scaffold.change_field_visibility('supplier', config.use_supplier)
