#!/uunconfirmedr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.


from argeweb import Controller, scaffold, route_menu, route, route_with
from ..models.config_model import ConfigModel


class Order(Controller):
    class Scaffold:
        hidden_in_form = ['name', 'payment_type_title', 'freight_type_title', 'total_price']

    @route
    @route_menu(list_name=u'welcome', text=u'新訂單', sort=1301, parameter=u'status=new_order')
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'全部訂單', sort=1300)
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'新訂單', parameter=u'status=new_order', need_hr=True, sort=1301)
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'已付款', parameter=u'status=already_paid', sort=1302)
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'備貨中', parameter=u'status=stocking', sort=1303)
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'已出貨', parameter=u'status=shipped', sort=1304)
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'已結單', parameter=u'status=closed', sort=1305)
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'異常流程', parameter=u'status=abnormal_flow', sort=1306)
    @route_menu(list_name=u'backend', group=u'訂單管理', text=u'取消訂單', parameter=u'status=order_cancel', sort=1307)
    def admin_list(self):
        if 'query' not in self.request.params:
            def query_factory_with_status(controller):
                return controller.meta.Model.all_with_status(controller.status)

            self.scaffold.display_in_list = [
                'order_no',
                'purchaser_name',
                'payment_type_object',
                'payment_status_object',
                'total_amount',
                'created',
            ]
            setattr(self, 'status', self.params.get_string('status', ''))
            if self.status != '':
                self.scaffold.query_factory = query_factory_with_status
                list_field = {
                    'new_order': ['order_no', 'purchaser_name', 'total_amount', 'created', 'payment_type_object', 'currency_title', 'currency_need_pay_amount'],
                    'already_paid': ['order_no', 'purchaser_name', 'total_amount', 'created', 'payment_type_object', 'currency_title', 'currency_need_pay_amount'],
                    # 'stocking': [],
                    # 'shipped': [],
                    'closed': ['order_no', 'purchaser_name', 'payment_type_object', 'payment_status_object', 'total_amount', 'created', 'order_close_datetime', 'order_report_datetime'],
                    # 'abnormal_flow': [],
                    # 'order_cancel': [],
                }
                if self.status in list_field:
                    self.scaffold.display_in_list = list_field[self.status]
                self.context['search_prev_word'] = u'status=' + self.status + u' AND '
        else:
            self.scaffold.display_in_list = [
                'order_no',
                'purchaser_name',
                'payment_type_object',
                'total_amount',
                'created',
            ]
            s = self.params.get_string('query').split('AND')
            for si in s:
                if si.startswith(u'status'):
                    n = si.split(u'=')
                    self.context['search_prev_word'] = u'status=' + n[1] + u' AND '
        return scaffold.list(self)

    def admin_add(self):
        def scaffold_before_validate(**kwargs):
            from datetime import datetime
            item = kwargs['item']
            item.order_close_datetime = datetime.now()
            item.order_cancel_datetime = datetime.now()
            item.order_report_datetime = datetime.now()
        self.events.scaffold_before_validate += scaffold_before_validate
        return scaffold.add(self)

    def admin_edit(self, key):
        self.events.scaffold_after_save += self.scaffold_after_save
        scaffold.edit(self, key)

    def admin_view(self, key):
        from ..models.order_item_model import OrderItemModel
        scaffold.view(self, key)
        order = self.context[self.scaffold.singular]
        self.context['order'] = order
        self.context['items'] = OrderItemModel.all_with_order(order=order)

    @route
    @route_menu(list_name=u'backend', group=u'產品管理', need_hr=True, text=u'成本利潤', sort=1341)
    def admin_cost(self):
        self.scaffold.display_in_list = ['order_no', 'total_amount', 'cost_for_items', 'cost_for_freight', 'cost_for_other', 'cost', 'profit', 'cost_remark', 'created']
        self.meta.view.template_name = 'backend/list.html'
        return scaffold.list(self)

    @route
    @route_menu(list_name=u'super_user', group=u'訂單管理', text=u'狀態重置', sort=889)
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
        return 'done'

    @route
    def gen_payment_information(self):
        order_keys = self.params.get_string('order_id')
        source_order = None
        source_list = []
        need_pay_amount = 0.0
        for item in order_keys.split(u','):
            order = self.params.get_ndb_record(item)
            if not source_order:
                source_order = order
            need_pay_amount += order.need_pay_amount
            source_list.append(order)

        if source_order is None:
            return 'error order not exist'
        payment_type = source_order.payment_type_object.get()
        payment_status = source_order.payment_status_object.get()
        if payment_status is not None:
            if payment_status.name not in ['unconfirmed', 'pending_payment']:
                return 'error payment status not exist'

        if payment_type is None:
            return 'error payment type not exist'
        if self.application_user is None:
            return 'error user not exist'
        self.fire(
            event_name='create_payment',
            title=u'支付訂單 %s 使用 %s ' % (source_order.order_no, payment_type.title),
            detail=u'支付訂單 %s 使用 %s ' % (source_order.order_no, payment_type.title),
            amount=need_pay_amount,
            source=source_order,
            source_params={'order_no': source_order.order_no},
            source_callback_uri='order:order:after_pay',
            payment_type=payment_type,
            user=self.application_user,
            status='pending_payment',
            source_list=source_list
        )
        return self.redirect(self.payment_record.pay_url)

    @route
    def gen_payment_information_with_link(self):
        order_link = self.params.get_string('order_link')
        order_list = self.meta.Model.find_by_properties(order_link=order_link).fetch()
        if len(order_list) == 0:
            return 'error order not exist'
        order_key_list = []
        for item in order_list:
            order_key_list.append(self.util.encode_key(item))
        url = self.uri('order:order:gen_payment_information')
        return self.redirect(url + '?order_id=' + ','.join(order_key_list))

    @route
    def after_pay(self):
        from ..models.config_model import ConfigModel
        config = ConfigModel.get_config()

        payment_record = self.params.get_ndb_record('payment_record')
        if payment_record is None:
            return self.redirect_uri(config.after_pay_uri_error, {'error': u'付款記錄不存在'})
        payment_status = payment_record.payment_status.get()
        if payment_status is None:
            return self.redirect_uri(config.after_pay_uri_error, {'error': u'未知的付款狀態'})
        order_record = payment_record.source
        order_list = self.meta.Model.find_by_properties(order_link=order_record.order_link).fetch()
        for order in order_list:
            order.set_payment_status(payment_status)
            if payment_status.name in [u'already_paid', u'full_payment_with_point']:
                order.set_order_status(u'already_paid')
            order.put()
        return self.redirect_uri(config.after_pay_uri, {'order': order_record.order_no, 'pay': 'done'})

    @staticmethod
    def scaffold_after_save(controller, item, *args, **kwargs):
        has_change = False
        item.set_order_status()
        item.set_payment_type()
        item.set_freight_status()
        if item.status == u'closed' and item.is_closed is False:
            item.close_order()
            has_change = True
            controller.fire(
                event_name='after_order_close',
                order=item
            )
        if item.status == u'order_cancel' and item.is_cancel is False:
            item.cancel_order()
            has_change = True
            controller.fire(
                event_name='after_order_cancel',
                order=item
            )
        if has_change:
            item.put()

    def before_scaffold(self):
        super(Order, self).before_scaffold()
        self.config = ConfigModel.get_config()
        show_currency = self.config.show_currency
        for field_name in [
            'currency_name', 'currency_title', 'currency_exchange_rate', 'currency_subtotal_amount',
            'currency_freight_amount', 'currency_total_amount', 'currency_total_discount_amount',
            'currency_need_pay_amount',
        ]:
            self.scaffold.change_field_visibility(field_name, show_currency, show_currency)
        self.scaffold.change_field_visibility('recipient_store_number', self.config.show_convenience_stores)
        self.scaffold.change_field_visibility('recipient_store_name', self.config.show_convenience_stores)
        self.scaffold.change_field_visibility('is_report', self.config.show_report_filed)
        self.scaffold.change_field_visibility('order_report_datetime', self.config.show_report_filed)
        self.scaffold.change_field_visibility('supplier', self.config.use_supplier)

        self.meta.Model.Meta.tab_pages = [u'物流', u'金流', u'備註']
        if self.config.show_cost:
            self.meta.Model.Meta.tab_pages.append(u'成本')
            index = self.meta.Model.Meta.tab_pages.index(u'成本')
            self.meta.Model.cost_for_items._tab_page_index = index
            self.meta.Model.cost_for_freight._tab_page_index = index
            self.meta.Model.cost_for_other._tab_page_index = index
            self.meta.Model.cost._tab_page_index = index
            self.meta.Model.profit._tab_page_index = index
            self.meta.Model.cost_remark._tab_page_index = index

        if self.config.show_invoice:
            self.meta.Model.Meta.tab_pages.append(u'發票')
            index = self.meta.Model.Meta.tab_pages.index(u'發票')
            self.meta.Model.invoice._tab_page_index = index
            self.meta.Model.invoice_type._tab_page_index = index
            self.meta.Model.invoice_donate._tab_page_index = index
            self.meta.Model.invoice_mobile._tab_page_index = index
            self.meta.Model.invoice_moica._tab_page_index = index
            self.meta.Model.invoice_address._tab_page_index = index
            self.meta.Model.invoice_company_title._tab_page_index = index
            self.meta.Model.invoice_company_number._tab_page_index = index
            self.meta.Model.is_invoice_created._tab_page_index = index

    def after_scaffold(self, item=None):
        super(Order, self).after_scaffold(item)
        if item is None:
            return
        self.scaffold.change_field_visibility('order_close_datetime', item.is_closed, False)
        self.scaffold.change_field_visibility('order_cancel_datetime', item.is_cancel, False)
        self.scaffold.change_field_visibility('order_report_datetime', item.is_report, False)

        if self.config.show_invoice:
            for field_name in [
                'invoice_donate', 'invoice_mobile', 'invoice_moica', 'invoice_address', 'invoice_company_title',
                'invoice_company_number'
            ]:
                self.scaffold.change_field_visibility(field_name, False, False)
            if item.invoice_type == 'electronic':
                if item.invoice_vehicle == 'member':
                    pass
                elif item.invoice_vehicle == 'mobile':
                    self.scaffold.change_field_visibility('invoice_mobile', True, True)
                elif item.invoice_vehicle == 'moica':
                    self.scaffold.change_field_visibility('invoice_moica', True, True)
            elif item.invoice_type == 'donate':
                self.scaffold.change_field_visibility('invoice_donate', True, True)
            elif item.invoice_type == 'paper':
                self.scaffold.change_field_visibility('invoice_address', True, True)
            elif item.invoice_type == 'company':
                self.scaffold.change_field_visibility('invoice_address', True, True)
                self.scaffold.change_field_visibility('invoice_company_title', True, True)
                self.scaffold.change_field_visibility('invoice_company_number', True, True)
            self.scaffold.change_field_visibility('order_close_datetime', item.is_closed, item.is_closed)
            self.scaffold.change_field_visibility('order_cancel_datetime', item.is_cancel, item.is_cancel)
            self.scaffold.change_field_visibility('order_report_datetime', item.is_report, item.is_report)

