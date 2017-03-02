#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import ViewFunction, ViewDatastore
from models import *
from models.order_model import OrderModel

ViewDatastore.register('order_list', OrderModel.all)

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
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
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
