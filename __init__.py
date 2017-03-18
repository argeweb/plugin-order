#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import ViewFunction, ViewDatastore
from models import *
from models.order_model import OrderModel
from models.order_item_model import OrderItemModel

ViewDatastore.register('order_list', OrderModel.all)
ViewDatastore.register('order_items', OrderItemModel.all_with_order)

plugins_helper = {
    'title': u'訂單管理模組',
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
                {'action': 'list', 'name': u'狀態管理'},
                {'action': 'add', 'name': u'新增狀態'},
                {'action': 'edit', 'name': u'編輯狀態'},
                {'action': 'view', 'name': u'檢視狀態'},
                {'action': 'delete', 'name': u'刪除狀態'},
            ]
        },
        'payment_status': {
            'group': u'付款狀態',
            'actions': [
                {'action': 'list', 'name': u'付款狀態'},
                {'action': 'add', 'name': u'新增付款狀態'},
                {'action': 'edit', 'name': u'編輯付款狀態'},
                {'action': 'view', 'name': u'檢視付款狀態'},
                {'action': 'delete', 'name': u'刪除付款狀態'},
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
        'payment_type': {
            'group': u'付款方式',
            'actions': [
                {'action': 'list', 'name': u'付款方式'},
                {'action': 'add', 'name': u'新增付款方式'},
                {'action': 'edit', 'name': u'編輯付款方式'},
                {'action': 'view', 'name': u'檢視付款方式'},
                {'action': 'delete', 'name': u'刪除付款方式'},
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
        }
    }
}
