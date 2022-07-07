import json
import random
import urllib.parse

import requests

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Product, Category

from telegram_shop.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_PROVIDER_TOKEN


def products_list(request):
    categories = Category.objects.filter(products__isnull=False).distinct()

    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products
    }

    return render(request, 'main/index.html', context)


@csrf_exempt
def make_order(request):  # return link to invoice
    if request.method == 'POST':
        order_data = json.loads(request.POST.get('order_data')) # [{'id': 4, 'count': 1}]
        comment = request.POST.get('comment') # 2414141 or null

        if comment is None:
            comment = 'Test'

        print(order_data)

        bot_token = TELEGRAM_BOT_TOKEN
        provider_token = TELEGRAM_PROVIDER_TOKEN

        invoice_title = f'Заказ (MALLECITY)'
        invoice_description = 'Оплата заказа.'
        invoice_payload = comment
        invoice_currency = 'RUB'
        invoice_prices = []

        for el in order_data:
            product_id = str(el['id'])

            product_label = Product.objects.get(id=product_id)

            product_amount = el["count"]
            product_price = Product.objects.get(id=product_id).price

            price = {
                'label': f'{product_label} x{product_amount}',
                'amount': int(float(product_price) * product_amount * 100)
            }

            invoice_prices.append(price)

        payload = {
            'title': invoice_title,
            'description': invoice_description,
            'payload': invoice_payload,
            'provider_token': provider_token,
            'currency': invoice_currency,
            'prices': json.dumps(invoice_prices)
        }

        invoice_resp = requests.post(f'https://api.telegram.org/bot{bot_token}/createInvoiceLink', data=payload)

        if invoice_resp.status_code == 200:
            return HttpResponse(invoice_resp.content)
        else:
            return HttpResponse(status=500)


