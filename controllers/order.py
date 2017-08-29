#!/uunconfirmedr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.


from argeweb import Controller, scaffold, route_menu, route


class Order(Controller):
    class Scaffold:
        hidden_in_form = ['name', 'payment_type_title', 'freight_type_title',]

    @route
    @route_menu(list_name=u'welcome', text=u'新訂單', sort=1301, parameter=u'status=new_order')
    @route_menu(list_name=u'backend', group=u'訂單管理', parameter=u'status=new_order', need_hr=True, text=u'新訂單', sort=1301)
    @route_menu(list_name=u'backend', group=u'訂單管理', parameter=u'status=already_paid', text=u'已付款', sort=1302)
    @route_menu(list_name=u'backend', group=u'訂單管理', parameter=u'status=stocking', text=u'備貨中', sort=1303)
    @route_menu(list_name=u'backend', group=u'訂單管理', parameter=u'status=shipped', text=u'已出貨', sort=1304)
    @route_menu(list_name=u'backend', group=u'訂單管理', parameter=u'status=closed', text=u'已結單', sort=1305)
    @route_menu(list_name=u'backend', group=u'訂單管理', parameter=u'status=abnormal_flow', text=u'異常流程', sort=1306)
    @route_menu(list_name=u'backend', group=u'訂單管理', parameter=u'status=order_cancel', text=u'取消訂單', sort=1307)
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
            self.context['search_prev_word'] = u'status=' + self.status + u' AND '
        else:
            s = self.params.get_string('query').split('AND')
            for si in s:
                if si.startswith(u'status'):
                    n = si.split(u'=')
                    self.context['search_prev_word'] = u'status=' + n[1] + u' AND '
        return scaffold.list(self)

    def admin_view(self, key):
        from ..models.order_item_model import OrderItemModel
        scaffold.view(self, key)
        order = self.context[self.scaffold.singular]
        self.context['order'] = order
        self.context['items'] = OrderItemModel.all_with_order(order=order)

    @route
    @route_menu(list_name=u'backend', group=u'產品管理', need_hr=True, text=u'成本利潤', sort=1312)
    def admin_cost(self):
        self.scaffold.display_in_list = ['order_no', 'total_amount', 'cost_for_items', 'cost_for_freight', 'cost_for_other', 'cost', 'profit', 'cost_remark', 'created']
        self.meta.view.template_name = 'backend/list.html'
        return scaffold.list(self)

    @route
    @route_menu(list_name=u'system', group=u'訂單管理', text=u'狀態重置', sort=889)
    def admin_reset_config(self):
        from plugins.payment_middle_layer.models.payment_status_model import PaymentStatusModel
        from ..models.order_status_model import OrderStatusModel
        from ..models.freight_status_model import FreightStatusModel
        OrderStatusModel.create_default_status()
        FreightStatusModel.create_default_status()
        PaymentStatusModel.create_default_status()
        return self.json({'message': u'狀態已重置'})

    @route
    def taskqueue_after_install(self):
        pass