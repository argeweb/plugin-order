#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2017/3/1.

from argeweb import BasicModel
from argeweb import Fields
from plugins.product import ProductSpecificationModel
from plugins.product_stock.models.stock_keeping_unit_model import StockKeepingUnitModel
from plugins.application_user.models.application_user_model import ApplicationUserModel
from plugins.product.models.config_model import ConfigModel
from plugins.product.models.product_model import ProductModel

from order_model import OrderModel
from time import time


class OrderItemModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    spec = Fields.KeyProperty(verbose_name=u'產品規格', kind=ProductSpecificationModel)
    user = Fields.ApplicationUserProperty(verbose_name=u'所屬使用者')
    order = Fields.KeyProperty(verbose_name=u'所屬訂單', kind=OrderModel)
    order_be_delete = Fields.BooleanProperty(verbose_name=u'訂單是否被刪除', default=False)

    title = Fields.StringProperty(verbose_name=u'產品名稱')
    product_object = Fields.KeyProperty(verbose_name=u'所屬產品', kind=ProductModel)
    product_name = Fields.SearchingHelperProperty(verbose_name=u'產品名稱', target='product_object', target_field_name='name')
    product_no = Fields.SearchingHelperProperty(verbose_name=u'產品型號', target='product_object', target_field_name='product_no')
    product_image = Fields.SearchingHelperProperty(verbose_name=u'產品圖片', target='product_object', target_field_name='image')
    spec_full_name = Fields.StringProperty(verbose_name=u'完整規格名稱', default=u'')
    price = Fields.FloatProperty(verbose_name=u'銷售價格', default=-1)
    cost = Fields.FloatProperty(verbose_name=u'成本', default=0.0)
    quantity = Fields.IntegerProperty(verbose_name=u'數量', default=0)

    # 庫存相關
    try:
        from plugins.product_stock.models.stock_keeping_unit_model import StockKeepingUnitModel
    except ImportError:
        class StockKeepingUnitModel(BasicModel):
            pass
    sku = Fields.KeyProperty(verbose_name=u'最小庫存單位', kind=StockKeepingUnitModel)
    sku_full_name = Fields.StringProperty(verbose_name=u'產品最小庫存名稱')
    expired_time = Fields.FloatProperty(verbose_name=u'庫存回收時間')
    quantity_has_count = Fields.IntegerProperty(verbose_name=u'已計入庫存的數量', default=0)
    can_add_to_order = Fields.BooleanProperty(verbose_name=u'加至訂單中', default=False)

    #  0=訂購(無庫存), 1=現貨, 2預購
    order_type = Fields.StringProperty(verbose_name=u'訂購方式')
    order_type_value = Fields.IntegerProperty(verbose_name=u'訂購方式(值)')

    size_1 = Fields.FloatProperty(verbose_name=u'長度(公分)', default=10.0)
    size_2 = Fields.FloatProperty(verbose_name=u'寬度(公分)', default=10.0)
    size_3 = Fields.FloatProperty(verbose_name=u'高度(公分)', default=10.0)
    weight = Fields.FloatProperty(verbose_name=u'重量(公斤)', default=1.0)

    @property
    def sku_instance(self):
        if not hasattr(self, '_sku'):
            self._sku = self.sku.get()
        return self._sku

    @property
    def product_instance(self):
        if not hasattr(self, '_product'):
            self._product = self.sku_instance.product_object.get()
        return self._product

    @classmethod
    def before_delete(cls, key):
        try:
            item = key.get()
            if item.order_type_value == 0:
                if item.quantity > 0:
                    sku = item.sku.get()
                    sku.change_estimate_quantity(item.quantity_has_count)
                    sku.put()
        except:
            pass

    @classmethod
    def all_with_user(cls, user=None, *args, **kwargs):
        if user is None:
            return cls.query().order(-cls.sort)
        return cls.query(cls.user==user.key).order(-cls.sort)

    @classmethod
    def all_with_order(cls, order=None, *args, **kwargs):
        return cls.query(cls.order==order.key).order(-cls.sort)

    @classmethod
    def get(cls, order, spec, order_type_value=0):
        return cls.query(cls.spec==spec.key, cls.order==order.key, cls.order_type_value==order_type_value).get()

    @classmethod
    def get_or_create(cls, user, spec, order, order_type_value=0):
        product = spec.product_object.get()
        item = cls.get(order, spec, order_type_value)
        if item is None:
            item = cls()
            item.spec = spec.key
            item.user = user.key
            item.order = order.key
            item.order_type_value = order_type_value
            item.product_object = product.key
            try:
                item.supplier = product.supplier.get().key
            except:
                pass
            item.order_type = [u'訂購', u'現貨', u'預購'][order_type_value]
        if spec.use_price:
            item.price = spec.price
        else:
            item.price = product.price
        if spec.use_cost:
            item.cost = spec.cost
        else:
            item.cost = product.cost
        item.size_1 = product.size_1
        item.size_2 = product.size_2
        item.size_3 = product.size_3
        item.weight = product.weight
        item._spec = spec
        item._product = product
        item._order = order
        item.title = product.title
        item.spec_full_name = spec.full_name
        item.put()
        return item

    @classmethod
    def all_with_user(cls, user):
        key = None
        if user is not None:
            key = user.key
        return cls.query(cls.user==key).order(-cls.sort)

    @classmethod
    def create_from_shopping_cart_item(cls, shopping_cart_item, order):
        item = cls()
        for p in shopping_cart_item._properties:
            setattr(item, p, getattr(shopping_cart_item, p))
        item.order = order.key
        item.put()
        return item

    def get_can_order_quantity(self):
        if self.order_type == 1:
            return 9999999
        return self.sku_instance.quantity_can_be_used + int(self.quantity_has_count)

    def change_quantity(self, quantity):
        sku = self.sku_instance
        product = self.product_instance
        if sku.use_price:
            self.price = sku.price
        else:
            self.price = product.price
        if sku.use_cost:
            self.cost = sku.cost
        else:
            self.cost = product.cost

        if self.order_type_value == 0:
            config = ConfigModel.find_by_product(product)
            if config.stock_recover:
                self.expired_time = time() + config.stock_recover_time
            else:
                self.expired_time = time() + 525600
            can_use_quantity = sku.quantity_can_be_used + int(self.quantity_has_count)
            old_quantity_has_count = self.quantity_has_count
            if can_use_quantity >= quantity and product.can_order:
                self.can_add_to_order = True
                self.quantity = quantity
                self.quantity_has_count = quantity
            else:
                self.can_add_to_order = False
                self.quantity = 0
                self.quantity_has_count = 0
            self._can_use_quantity = can_use_quantity
            sku.change_estimate_quantity(sub_quantity=old_quantity_has_count, add_quantity=self.quantity)
            sku.put()
        else:
            if product.can_pre_order:
                self.can_add_to_order = True
                self.quantity = quantity
            else:
                self.can_add_to_order = False
                self.quantity = 0
            sku.change_pre_order_quantity(sub_quantity=int(self.quantity_has_count), add_quantity=self.quantity)
            sku.put()

    def volumetric_weight(self, divisor=6000.0):
        n = self.size_1 * self.size_2 * self.size_3 / float(divisor)
        return n
