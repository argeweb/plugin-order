#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.
from datetime import datetime
from argeweb import Controller, scaffold, route_menu, route_with, route, settings
from argeweb import auth, add_authorizations
from argeweb.components.pagination import Pagination
from argeweb.components.csrf import CSRF, csrf_protect
from argeweb.components.search import Search
from plugins.mail import Mail


class Data(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search, CSRF)
        default_view = 'json'

    @route
    @add_authorizations(auth.check_user)
    @route_with('/data/order/check_info', name='data:order:check_info')
    def check_info(self):
        from ..models.freight_model import FreightModel, FreightTypeModel
        from ..models.payment_type_model import PaymentTypeModel
        from ..models.order_rule_model import OrderRuleModel
        cu = None
        try:
            from plugins.currency.models.currency_model import CurrencyModel
            cu = CurrencyModel.get_current_or_main_currency_with_controller(self)
        except:
            pass
        freight_data = []
        for item in FreightModel.all_enable().fetch(1000):
            start_amount = item.start_amount
            end_amount = item.end_amount
            freight_amount = item.freight_amount
            if cu:
                start_amount = cu.calc(start_amount)
                end_amount = cu.calc(end_amount)
                freight_amount = cu.calc(freight_amount)
            freight_data.append({
                'key': self.util.encode_key(item),
                'freight_type': self.util.encode_key(item.freight_type),
                'start_amount': start_amount,
                'end_amount': end_amount,
                'freight_amount': freight_amount,
            })
        freight_type_data = []
        for item in FreightTypeModel.all_enable().fetch(1000):
            freight_type_data.append({
                'key': self.util.encode_key(item),
                'name': item.name,
                'title': item.title
            })
        payment_type_data = []
        for item in PaymentTypeModel.all_enable().fetch(1000):
            payment_type_data.append({
                'key': self.util.encode_key(item),
                'name': item.name,
                'title': item.title
            })
        order_rule_data = []
        for item in OrderRuleModel.all_enable().fetch(1000):
            order_rule_data.append({
                'key': self.util.encode_key(item),
                'title': item.title,
                'check_target': item.check_target,
                'check_target_id': item.check_target_id,
                'check_operation': item.check_operation,
                'check_target_quantity': item.check_target_quantity,
                'check_target_count': item.check_target_count,
                'calculate_target': item.calculate_target,
                'multiplication': item.multiplication,
                'addition': item.addition
            })
        self.context["data"] = {
            'freight': freight_data,
            'freight_type': freight_type_data,
            'payment_type': payment_type_data,
            'order_rule': order_rule_data
        }
