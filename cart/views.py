
# cart/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
import stripe

from products.models import Product
from .cart import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY

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

def checkout(request):
    cart = Cart(request)
    return render(request, 'cart/checkout.html', {
        'cart': cart,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def create_checkout_session(request):
    cart = Cart(request)
    if not cart:
        return redirect('products:product_list')

    line_items = []
    for item in cart:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['name'],
                },
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        })

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/cart/payment/success/'),
            cancel_url=request.build_absolute_uri('/cart/payment/cancel/'),
        )
        return JsonResponse({'id': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def payment_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'cart/payment_success.html')

def payment_cancel(request):
    return render(request, 'cart/payment_cancel.html')
