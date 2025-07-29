
# cart/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/detail.html', {
#         'cart': cart,
#         'total_price': cart.total_price()
#     })


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    if product.quantity >= quantity:
        # 加入購物車
        cart.add(
            product_id=str(product.id),
            name=product.name,
            price=product.price,
            quantity=quantity
        )
        # 扣庫存
        product.quantity -= quantity
        product.save()
        return redirect('cart:cart_detail')
    else:
        return redirect('products:product_list')



@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)  # 你需要在 Cart 類別裡實作 remove 方法
    return redirect('cart:cart_detail')

# # cart/views.py
# from django.shortcuts import render
# from .cart import Cart

# from django.shortcuts import render, redirect
# from .cart import Cart
# from django.views.decorators.http import require_POST

# # cart/views.py
# from django.shortcuts import get_object_or_404, redirect
# from django.views.decorators.http import require_POST
# from products.models import Product
# from .cart import Cart  # 假設你的 Cart 類別在 cart/cart.py 裡


# # cart/cart.py
# class Cart:
#     def __init__(self, request):
#         self.session = request.session
#         cart = self.session.get('cart')
#         if not cart:
#             cart = self.session['cart'] = {}
#         self.cart = cart

#     @require_POST
#     def add(request, product_id):
#         cart = Cart(request)
#         product = get_object_or_404(Product, id=product_id)

#         # ✅ 取得表單送來的購買數量
#         quantity = int(request.POST.get('quantity', 1))

#         # ✅ 判斷庫存是否足夠
#         if product.quantity >= quantity:
#             # 加入購物車（呼叫你提供的 cart.add）
#             cart.add(
#                 product_id=str(product.id),  # 注意：你 add() 裡是字串 key
#                 name=product.name,
#                 price=product.price,
#                 quantity=quantity
#             )

#             # ✅ 扣庫存
#             product.quantity -= quantity
#             product.save()

#             return redirect('cart:cart_detail')
#         else:
#             # ➖ 庫存不足，導回商品頁（你也可以加提示訊息）
#             return redirect('products:product_list')


#     def clear(self):
#         self.session['cart'] = {}
#         self.save()

#     def save(self):
#         self.session.modified = True

#     def __iter__(self):
#         for item in self.cart.values():
#             yield item

#     def total_price(self):
#         return sum(item['price'] * item['quantity'] for item in self.cart.values())
        

# # 假設您已經有 Product 模型

# from products.models import Product


# def cart_detail(request):
#     cart = Cart(request)
#     return render(request, 'cart/detail.html', {'cart': cart})



# @require_POST
# def cart_remove(request, product_id):
#     cart = request.session.get('cart', {})
#     if str(product_id) in cart:
#         del cart[str(product_id)]
#         request.session['cart'] = cart
#     return redirect('cart:cart_detail')

