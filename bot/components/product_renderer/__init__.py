from .telegram_renderers import (SellerProductRenderer as _SellerProductRenderer,
                                 MediatorProductRenderer as _MediatorProductRenderer,
                                 BuyerProductRenderer as _BuyerProductRenderer,
                                 DeleteProductRenderer as _DeleteProductRenderer,
                                 OnlyProductRenderer as _OnlyProductRenderer,
                                 BuyerSkipProductRenderer as _BuyerSkipProductRenderer)

seller_product_renderer = _SellerProductRenderer()
# delete_product_renderer = _DeleteProductRenderer()
mediator_product_renderer = _MediatorProductRenderer()

buyer_product_renderer = _BuyerProductRenderer()
skip_buyer_product_renderer = _BuyerSkipProductRenderer()
# product_renderer = _OnlyProductRenderer()