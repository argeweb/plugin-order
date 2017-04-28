#!/uunconfirmedr/bin/env python
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

    class Scaffold:
        # display_in_list = ('title_lang_zhtw', 'name')
        hidden_in_form = ['name', 'payment_type_title', 'freight_type_title',]

    @route
    @route_menu(list_name=u'backend', text=u'新訂單', sort=1301, group=u'銷售管理', parameter=u'status=new_order')
    @route_menu(list_name=u'backend', text=u'已付款', sort=1302, group=u'銷售管理', parameter=u'status=already_paid')
    @route_menu(list_name=u'backend', text=u'備貨中', sort=1303, group=u'銷售管理', parameter=u'status=stocking')
    @route_menu(list_name=u'backend', text=u'已出貨', sort=1304, group=u'銷售管理', parameter=u'status=shipped')
    @route_menu(list_name=u'backend', text=u'已結單', sort=1305, group=u'銷售管理', parameter=u'status=closed')
    @route_menu(list_name=u'backend', text=u'異常流程', sort=1306, group=u'銷售管理', parameter=u'status=abnormal_flow')
    @route_menu(list_name=u'backend', text=u'取消訂單', sort=1307, group=u'銷售管理', parameter=u'status=order_cancel')
    def admin_list(self):
        if 'query' not in self.request.params:
            def query_factory_with_status(controller):
                return controller.meta.Model.all_with_status(controller.status)

            setattr(self, 'status', self.params.get_string('status', ''))
            self.scaffold.query_factory = query_factory_with_status
            list_field = {
                'new_order': ['order_no', 'created', 'payment_type', 'payment_status', 'currency_title', 'currency_need_pay_amount'],
                'already_paid': ['order_no', 'created', 'payment_type', 'payment_status', 'currency_title', 'currency_need_pay_amount'],
                # 'stocking': [],
                # 'shipped': [],
                # 'closed': [],
                # 'abnormal_flow': [],
                # 'order_cancel': [],
            }
            if self.status in list_field:
                self.scaffold.display_in_list = list_field[self.status]
        return scaffold.list(self)

    def admin_view(self, key):
        from ..models.order_item_model import OrderItemModel
        scaffold.view(self, key)
        order = self.context[self.scaffold.singular]
        self.context['order'] = order
        self.context['items'] = OrderItemModel.all_with_order(order=order)

    @route
    @route_menu(list_name=u'backend', text=u'訂單相關設定', sort=9931, group=u'系統設定')
    def admin_config(self):
        pass

    @route
    def admin_reset_config(self):
        from ..models.order_status_model import OrderStatusModel
        from ..models.freight_status_model import FreightStatusModel
        from ..models.payment_status_model import PaymentStatusModel
        OrderStatusModel.create_default_status()
        FreightStatusModel.create_default_status()
        PaymentStatusModel.create_default_status()
        return self.json({'message': u'done'})
