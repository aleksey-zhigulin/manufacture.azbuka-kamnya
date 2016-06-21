from __future__ import unicode_literals
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _

SHOP_APP_LABEL = 'shop'
SHOP_VALUE_ADDED_TAX = Decimal(0)
SHOP_DEFAULT_CURRENCY = 'RUB'
# SHOP_CART_MODIFIERS = (
#     'myshop.polymorphic_modifiers.MyShopCartModifier' if SHOP_TUTORIAL == 'polymorphic'
#     else 'shop.modifiers.defaults.DefaultCartModifier',
#     'shop.modifiers.taxes.CartExcludedTaxModifier',
#     'myshop.modifiers.PostalShippingModifier',
#     'myshop.modifiers.CustomerPickupModifier',
#     'myshop.modifiers.StripePaymentModifier',
#     'shop.modifiers.defaults.PayInAdvanceModifier',
# )
SHOP_EDITCART_NG_MODEL_OPTIONS = "{updateOn: 'default blur', debounce: {'default': 2500, 'blur': 0}}"

SHOP_ORDER_WORKFLOWS = (
    'shop.payment.defaults.PayInAdvanceWorkflowMixin',
    'shop.shipping.delivery.PartialDeliveryWorkflowMixin'
    'shop_stripe.payment.OrderWorkflowMixin',
)

SHOP_MONEY_FORMAT = '{amount} {symbol}'
