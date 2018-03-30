#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import ViewDatastore
from argeweb.core.events import on
from models import *
from models.order_model import OrderModel
from models.order_item_model import OrderItemModel
from models.freight_type_model import FreightTypeModel
from models.freight_status_model import FreightStatusModel
from models.order_status_model import OrderStatusModel
from models.order_discount_model import OrderDiscountModel


@on('order_item_change_quantity')
def order_item_change_quantity(controller, item, quantity, *args, **kwargs):
    if item.order_type_value == 0:
        if item.spec.get().can_be_purchased:
            item.quantity = quantity


@on('update_freight_type')
def update_freight_type(controller, name, title=None, is_enable=None, *args, **kwargs):
    p = FreightTypeModel.get_or_create_by_name(name)
    p.name = name
    if title is not None:
        p.title = title
    if is_enable is not None:
        p.is_enable = is_enable
    p.put()
    return p


@on('calc_freight_amount')
def calc_freight_amount(controller, target, freight_type=None, freight_data=None, *args, **kwargs):
    if freight_data is None:
        freight_data = freight_type.items.fetch()
    freight_max = 0.0
    use_supplier_freight = False
    supplier_max = 0.0
    for freight in freight_data:
        if freight.is_enable is False:
            continue
        if freight.supplier is not None and freight.supplier != target.supplier:
            continue
        target_value = getattr(target, freight.check_target)
        if freight.check_target == 'total_volumetric_weight':
            target_value_2 = getattr(target, 'total_weight')
            if target_value_2 > target_value:
                target_value = target_value_2
        f = freight.check_amount(target_value)
        if freight.supplier is not None:
            use_supplier_freight = True
            if f > supplier_max:
                supplier_max = f
        if f > freight_max:
            freight_max = f

    for freight in freight_data:
        if freight.is_enable is False:
            continue
        if freight.supplier is not None and freight.supplier != target.supplier:
            continue
        if freight.check_target != 'total_price':
            continue
        target_value = getattr(target, 'total_price')
        if freight.end_value >= target_value > freight.start_value:
            freight_max = freight.freight_amount

    if use_supplier_freight:
        setattr(target, 'freight_amount', supplier_max)
    else:
        setattr(target, 'freight_amount', freight_max)


ViewDatastore.register('order_list', OrderModel.all)
ViewDatastore.register('order', OrderModel.find_by_properties)
ViewDatastore.register('order_status_list', OrderStatusModel.all)
ViewDatastore.register('order_items', OrderItemModel.all_with_order)
ViewDatastore.register('order_discount_items', OrderDiscountModel.all_with_order)
ViewDatastore.register('freight_type_list', FreightTypeModel.all_enable)
ViewDatastore.register('freight_type', FreightTypeModel.find_by_properties)
ViewDatastore.register('freight_status_list', FreightStatusModel.all)
ViewDatastore.register('supplier_order_list', OrderModel.all_with_supplier)


plugins_helper = {
    'title': u'訂單管理',
    'desc': u'訂單相關之管理',
    'controllers': {
        'order': {
            'group': u'訂單管理',
            'actions': [
                {'action': 'list', 'name': u'訂單管理'},
                {'action': 'add', 'name': u'新增訂單管理'},
                {'action': 'edit', 'name': u'編輯訂單管理'},
                {'action': 'view', 'name': u'檢視訂單管理'},
                {'action': 'delete', 'name': u'刪除訂單管理'},
                {'action': 'config', 'name': u'訂單相關設定'},
                {'action': 'cost', 'name': u'成本利潤'},
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
            ]
        },
        'order_item': {
            'group': u'訂單項目',
            'actions': [
                {'action': 'list', 'name': u'訂單項目'},
                {'action': 'add', 'name': u'新增訂單項目'},
                {'action': 'edit', 'name': u'編輯訂單項目'},
                {'action': 'view', 'name': u'檢視訂單項目'},
                {'action': 'delete', 'name': u'刪除訂單項目'},
            ]
        },
        'order_status': {
            'group': u'訂單狀態',
            'actions': [
                {'action': 'list', 'name': u'訂單狀態'},
                {'action': 'add', 'name': u'新增訂單狀態'},
                {'action': 'edit', 'name': u'編輯訂單狀態'},
                {'action': 'view', 'name': u'檢視訂單狀態'},
                {'action': 'delete', 'name': u'刪除訂單狀態'},
            ]
        },
        'freight_status': {
            'group': u'寄送狀態',
            'actions': [
                {'action': 'list', 'name': u'寄送狀態'},
                {'action': 'add', 'name': u'新增寄送狀態'},
                {'action': 'edit', 'name': u'編輯寄送狀態'},
                {'action': 'view', 'name': u'檢視寄送狀態'},
                {'action': 'delete', 'name': u'刪除寄送狀態'},
            ]
        },
        'order_rule': {
            'group': u'訂單規則',
            'actions': [
                {'action': 'list', 'name': u'規則管理'},
                {'action': 'add', 'name': u'新增規則'},
                {'action': 'edit', 'name': u'編輯規則'},
                {'action': 'view', 'name': u'檢視規則'},
                {'action': 'delete', 'name': u'刪除規則'},
            ]
        },
        'freight_type': {
            'group': u'寄送方式',
            'actions': [
                {'action': 'list', 'name': u'寄送方式'},
                {'action': 'add', 'name': u'新增寄送方式'},
                {'action': 'edit', 'name': u'編輯寄送方式'},
                {'action': 'view', 'name': u'檢視寄送方式'},
                {'action': 'delete', 'name': u'刪除寄送方式'},
            ]
        },
        'freight': {
            'group': u'運費',
            'actions': [
                {'action': 'list', 'name': u'運費'},
                {'action': 'add', 'name': u'新增運費'},
                {'action': 'edit', 'name': u'編輯運費'},
                {'action': 'view', 'name': u'檢視運費'},
                {'action': 'delete', 'name': u'刪除運費'},
            ]
        },
        'config': {
            'group': u'訂單相關設定',
            'actions': [
                {'action': 'config', 'name': u'訂單相關設定'}
            ]
        }
    }
}
