import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_strip_product(product_name, product_description):
    """Создает продукт в Stripe"""
    return stripe.Product.create(name=product_name, description=product_description)


def create_strip_price(amount, product):
    """Создает цену в Stripe"""
    return stripe.Price.create(
        currency="rub", unit_amount=amount * 100, product=product
    )


def create_strip_session(price):
    """Создает сессию на оплату в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://localhost:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
