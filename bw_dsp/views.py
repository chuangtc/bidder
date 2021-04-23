from django.http import HttpResponse
from django.shortcuts import render

from google.protobuf import text_format

from .models import ad_settings

import random, json

# Create your views here.
def home_view(*args, **kwargs):
    return HttpResponse("<h1>Hello World! It's Bridgewell's assignment </h1>"
                        "<a href='http://127.0.0.1:8000/bw_dsp'>Location</a>")

def bidding_strategy_view(request, *args, **kwargs):
    bid_request = request.body
    bid_floor = 10
    # new_b = pickle.loads(bid_request)

    queryset = ad_settings.objects.all()
    max_creative_id = -1
    max_bid_price = -100

    for each in queryset:
        if each.status == False:
            continue
        bid_price = each.bidding_cpm * random.randrange(1, 10)
        if bid_price > max_bid_price:
            max_bid_price = bid_price
            max_creative_id = each.creative_id


    # Case :　Return HTTP 204 (No Content) if final bid price less than bid floor　
    if max_bid_price < bid_floor:
        response = HttpResponse()
        response.status_code = 204
        return response

    obj = { "creative_id": max_creative_id, "bid_price": max_bid_price }
    return HttpResponse(json.dumps(obj), content_type="application/json")