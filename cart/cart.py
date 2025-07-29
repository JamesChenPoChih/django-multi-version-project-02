# cart/cart.py


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, name, price, quantity=1):
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
        else:
            self.cart[product_id] = {
                'name': name,
                'price': price,
                'quantity': quantity,
            }
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def clear(self):
        self.session['cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    # def __iter__(self):
    #     for item in self.cart.values():
    #         yield item

    def total_price(self):
        return sum(item['price'] * item['quantity'] for item in self.cart.values())
    

    def __iter__(self):
        for product_id, item in self.cart.items():
            yield {
                'product_id': product_id,
                'name': item['name'],
                'price': item['price'],
                'quantity': item['quantity'],
            }